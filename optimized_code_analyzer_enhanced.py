#!/usr/bin/env python3
"""
Enhanced Code Analyzer with Fine-tuned Model Support

This version supports:
- Base CodeT5+ model (original)
- Fine-tuned DeepSeek Coder model (new)
- Easy toggle between models
- All existing optimizations (caching, streaming, etc.)

Author: AI Code Analyzer Project
Date: 2025
"""

import torch
import time
import hashlib
import json
import os
from typing import Dict, Any, Optional, Generator, Literal
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
from tqdm import tqdm
import streamlit as st

ModelType = Literal["codet5", "deepseek-finetuned"]

class EnhancedCodeAnalyzer:
    """
    Enhanced analyzer supporting multiple model types including fine-tuned models.
    """
    
    def __init__(
        self,
        model_type: ModelType = "codet5",
        model_id: Optional[str] = None,
        adapter_path: Optional[str] = None,
        cache_dir: str = "./cache",
        precision: str = "fp16",
        quick_max_new_tokens: int = 180,
        detailed_max_new_tokens: int = 300,
        remote_api_url: Optional[str] = None,
    ):
        """
        Initialize the enhanced analyzer.
        
        Args:
            model_type: Type of model to use ("codet5" or "deepseek-finetuned")
            model_id: Hugging Face model ID (auto-selected if None)
            adapter_path: Path to LoRA adapters for fine-tuned models
            cache_dir: Directory to store cached results
            precision: Model precision (fp16, int8, int4)
            quick_max_new_tokens: Max tokens for quick analysis
            detailed_max_new_tokens: Max tokens for detailed analysis
        """
        self.model_type = model_type
        self.cache_dir = cache_dir
        self.precision = precision.lower().strip()
        self.quick_max_new_tokens = quick_max_new_tokens
        self.detailed_max_new_tokens = detailed_max_new_tokens
        
        # Auto-select model_id based on type
        if model_id is None:
            if model_type == "codet5":
                self.model_id = "Salesforce/codet5p-220m"
            elif model_type == "deepseek-finetuned":
                self.model_id = "deepseek-ai/deepseek-coder-1.3b-instruct"
            else:
                raise ValueError(f"Unknown model_type: {model_type}")
        else:
            self.model_id = model_id
        
        # Set adapter path
        self.adapter_path = adapter_path
        if model_type == "deepseek-finetuned" and adapter_path is None:
            self.adapter_path = "./fine-tuned-analyst"
        
        self.model = None
        self.tokenizer = None
        self.cache = {}
        self.remote_api_url = remote_api_url
        
        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)
        
        # Load cache if exists
        self._load_cache()
    
    def _create_quantization_config(self) -> BitsAndBytesConfig:
        """Create quantization configuration."""
        return BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
    
    def _load_model(self):
        """Load the model with optimizations."""
        if self.model is not None:
            return
        
        print(f"🚀 Loading {self.model_type} model...")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, trust_remote_code=True)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Configure precision
        quantization_config = None
        dtype = None
        banner = ""

        if self.precision == "fp16":
            dtype = torch.float16
            banner = "FP16 precision"
        elif self.precision == "int8":
            quantization_config = BitsAndBytesConfig(load_in_8bit=True)
            banner = "INT8 quantization"
        elif self.precision == "int4":
            quantization_config = self._create_quantization_config()
            banner = "INT4 (nf4) quantization"
        else:
            dtype = torch.float16
            banner = f"Unknown precision '{self.precision}', defaulting to FP16"
        
        # Load base model based on type
        if self.model_type == "codet5":
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                self.model_id,
                device_map="auto",
                torch_dtype=dtype,
                quantization_config=quantization_config,
                trust_remote_code=True,
            )
            print(f"✅ CodeT5+ loaded with {banner}!")
            
        elif self.model_type == "deepseek-finetuned":
            # Load base DeepSeek model
            base_model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                device_map="auto",
                torch_dtype=dtype,
                quantization_config=quantization_config,
                trust_remote_code=True,
            )
            
            # Load LoRA adapters if path exists
            if self.adapter_path and os.path.exists(self.adapter_path):
                print(f"🔗 Loading LoRA adapters from {self.adapter_path}...")
                self.model = PeftModel.from_pretrained(base_model, self.adapter_path)
                print(f"✅ Fine-tuned DeepSeek loaded with {banner}!")
            else:
                print(f"⚠️  Adapter path not found: {self.adapter_path}")
                print(f"✅ Using base DeepSeek model with {banner}")
                self.model = base_model
    
    def _create_prompt(self, code: str) -> str:
        """Create prompt based on model type."""
        if self.model_type == "codet5":
            return f"""Analyze this code for bugs, performance issues, and security concerns:

{code}

Analysis:"""
        
        elif self.model_type == "deepseek-finetuned":
            return f"""<s>[INST] Analyze this code for bugs, performance, and security issues. Give a quality score from 1-100 and provide a detailed analysis.

Code:
```
{code}
``` [/INST]"""
        
        return code
    
    def _extract_response(self, full_text: str, prompt: str) -> str:
        """Extract the actual response from generated text."""
        if self.model_type == "codet5":
            # Remove prompt from response
            return full_text[len(prompt):].strip()
        
        elif self.model_type == "deepseek-finetuned":
            # Extract response after [/INST]
            if '[/INST]' in full_text:
                return full_text.split('[/INST]')[-1].strip()
            return full_text.strip()
        
        return full_text.strip()
    
    def _get_cache_key(self, code: str) -> str:
        """Generate cache key for code."""
        # Include model type in cache key
        combined = f"{self.model_type}:{code}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _load_cache(self):
        """Load cached results from disk."""
        cache_file = os.path.join(self.cache_dir, "analysis_cache_enhanced.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    self.cache = json.load(f)
                print(f"📁 Loaded {len(self.cache)} cached analyses")
            except:
                self.cache = {}
    
    def _save_cache(self):
        """Save cache to disk."""
        cache_file = os.path.join(self.cache_dir, "analysis_cache_enhanced.json")
        with open(cache_file, 'w') as f:
            json.dump(self.cache, f)
    
    def _check_cache(self, code: str) -> Optional[Dict[str, Any]]:
        """Check if analysis is cached."""
        cache_key = self._get_cache_key(code)
        return self.cache.get(cache_key)
    
    def _save_to_cache(self, code: str, result: Dict[str, Any]):
        """Save analysis result to cache."""
        cache_key = self._get_cache_key(code)
        self.cache[cache_key] = result
        self._save_cache()
    
    def analyze_code_streaming(
        self,
        code: str,
        show_progress: bool = True,
        mode: str = "detailed",
    ) -> Generator[str, None, Dict[str, Any]]:
        """
        Analyze code with streaming response and progress indicators.
        
        Args:
            code: Code to analyze
            show_progress: Whether to show progress indicators
            mode: Analysis mode ("quick" or "detailed")
            
        Yields:
            str: Partial analysis results
        """
        # Check cache first
        cached_result = self._check_cache(code)
        if cached_result:
            print("⚡ Using cached result!")
            yield cached_result["analysis"]
            return cached_result
        
        # Load model if not loaded
        self._load_model()
        
        # Create prompt
        prompt = self._create_prompt(code)
        
        # Tokenize input
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024 if self.model_type == "deepseek-finetuned" else 512,
            padding=True,
        )
        device = next(self.model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Generate analysis
        start_time = time.time()
        
        if show_progress:
            print(f"🔍 Analyzing code with {self.model_type}...")
            progress_bar = tqdm(total=100, desc="Analysis Progress")
        
        try:
            with torch.no_grad():
                max_new = self.detailed_max_new_tokens if mode == "detailed" else self.quick_max_new_tokens
                
                # Generation parameters based on model type
                if self.model_type == "codet5":
                    num_beams = 2 if mode == "detailed" else 1
                    outputs = self.model.generate(
                        inputs["input_ids"],
                        attention_mask=inputs.get("attention_mask"),
                        max_new_tokens=max_new,
                        num_beams=num_beams,
                        do_sample=False,
                        pad_token_id=self.tokenizer.eos_token_id,
                        use_cache=True,
                    )
                else:  # deepseek-finetuned
                    outputs = self.model.generate(
                        **inputs,
                        max_new_tokens=max_new,
                        temperature=0.7,
                        do_sample=True,
                        pad_token_id=self.tokenizer.eos_token_id,
                        eos_token_id=self.tokenizer.eos_token_id,
                    )
            
            if show_progress:
                progress_bar.update(50)
            
            # Decode analysis
            full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            analysis_text = self._extract_response(full_text, prompt)
            
            if show_progress:
                progress_bar.update(50)
                progress_bar.close()
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(analysis_text)
            
            total_time = time.time() - start_time
            
            # Create result
            result = {
                "analysis": analysis_text,
                "quality_score": quality_score,
                "execution_time": total_time,
                "model": self.model_id,
                "model_type": self.model_type,
                "cached": False
            }
            
            # Save to cache
            self._save_to_cache(code, result)
            
            # Yield the analysis
            yield analysis_text
            
            return result
            
        except Exception as e:
            if show_progress:
                progress_bar.close()
            raise e
    
    def analyze_code_fast(self, code: str, mode: str = "quick") -> Dict[str, Any]:
        """
        Fast analysis without streaming (for batch processing).
        
        Args:
            code: Code to analyze
            mode: Analysis mode ("quick" or "detailed")
            
        Returns:
            Dict: Analysis result
        """
        # Check if using remote model
        if self.remote_api_url:
            return self.analyze_code_remote(code, mode)
        
        # Check cache first
        cached_result = self._check_cache(code)
        if cached_result:
            cached_result["cached"] = True
            return cached_result
        
        # Load model if not loaded
        self._load_model()
        
        # Create prompt
        prompt = self._create_prompt(code)
        
        # Tokenize input
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024 if self.model_type == "deepseek-finetuned" else 512,
            padding=True,
        )
        device = next(self.model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Generate analysis
        start_time = time.time()
        
        with torch.no_grad():
            max_new = self.quick_max_new_tokens if mode == "quick" else self.detailed_max_new_tokens
            
            if self.model_type == "codet5":
                num_beams = 1 if mode == "quick" else 2
                outputs = self.model.generate(
                    inputs["input_ids"],
                    attention_mask=inputs.get("attention_mask"),
                    max_new_tokens=max_new,
                    num_beams=num_beams,
                    do_sample=False,
                    pad_token_id=self.tokenizer.eos_token_id,
                    use_cache=True,
                )
            else:  # deepseek-finetuned
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )
        
        # Decode analysis
        full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        analysis_text = self._extract_response(full_text, prompt)
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(analysis_text)
        
        total_time = time.time() - start_time
        
        # Create result
        result = {
            "analysis": analysis_text,
            "quality_score": quality_score,
            "execution_time": total_time,
            "model": self.model_id,
            "model_type": self.model_type,
            "cached": False
        }
        
        # Save to cache
        self._save_to_cache(code, result)
        
        return result
    
    def _calculate_quality_score(self, analysis_text: str) -> int:
        """
        Calculate quality score for analysis.
        
        Args:
            analysis_text: Analysis text
            
        Returns:
            int: Quality score (0-100)
        """
        # Try to extract score from DeepSeek output first
        if "Quality Score:" in analysis_text or "quality score" in analysis_text.lower():
            import re
            score_match = re.search(r'(?:Quality Score:|quality score:?)\s*(\d+)', analysis_text, re.IGNORECASE)
            if score_match:
                return int(score_match.group(1))
        
        # Fallback to heuristic calculation
        score = 0
        analysis_lower = analysis_text.lower()
        
        if any(word in analysis_lower for word in ['bug', 'error', 'issue', 'problem', 'flaw']):
            score += 20
        
        if any(word in analysis_lower for word in ['performance', 'slow', 'efficient', 'complexity', 'optimization']):
            score += 20
        
        if any(word in analysis_lower for word in ['security', 'vulnerability', 'safe', 'unsafe', 'risk']):
            score += 20
        
        if any(word in analysis_lower for word in ['suggest', 'improve', 'better', 'recommend', 'fix', 'solution']):
            score += 20
        
        if len(analysis_text) > 200:
            score += 10
        if len(analysis_text) > 500:
            score += 10
        
        return min(score, 100)
    
    def analyze_code_remote(self, code: str, mode: str = "quick") -> Dict[str, Any]:
        """Analyze code using remote Hugging Face API."""
        import requests
        
        if not self.remote_api_url:
            raise ValueError("No remote API URL configured")
        
        cached_result = self._check_cache(code)
        if cached_result:
            cached_result["cached"] = True
            return cached_result
        
        start_time = time.time()
        
        try:
            max_tokens = self.quick_max_new_tokens if mode == "quick" else self.detailed_max_new_tokens
            
            response = requests.post(
                f"{self.remote_api_url}/analyze",
                json={"code": code, "max_tokens": max_tokens},
                timeout=60
            )
            response.raise_for_status()
            
            data = response.json()
            analysis_text = data["analysis"]
            
            quality_score = self._calculate_quality_score(analysis_text)
            total_time = time.time() - start_time
            
            result = {
                "analysis": analysis_text,
                "quality_score": quality_score,
                "execution_time": total_time,
                "model": "fine-tuned-deepseek-remote",
                "model_type": "deepseek-finetuned-remote",
                "cached": False
            }
            
            self._save_to_cache(code, result)
            return result
            
        except Exception as e:
            raise Exception(f"Remote analysis failed: {e}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        if self.model is None:
            return {"status": "Model not loaded"}
        
        param_count = sum(p.numel() for p in self.model.parameters())
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        device = next(self.model.parameters()).device
        
        info = {
            "model_id": self.model_id,
            "model_type": self.model_type,
            "parameters": param_count,
            "trainable_parameters": trainable_params,
            "device": str(device),
            "precision": self.precision,
            "quick_max_new_tokens": self.quick_max_new_tokens,
            "detailed_max_new_tokens": self.detailed_max_new_tokens,
            "cache_size": len(self.cache)
        }
        
        if self.adapter_path:
            info["adapter_path"] = self.adapter_path
            info["using_adapters"] = os.path.exists(self.adapter_path) if self.adapter_path else False
        
        return info


def main():
    """Demo of the enhanced analyzer."""
    print("🚀 Enhanced Code Analyzer Demo")
    print("=" * 60)
    
    # Test code
    test_code = """
def calculate_fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

result = calculate_fibonacci(35)
print(result)
"""
    
    print(f"Test Code:\n{test_code}")
    print("=" * 60)
    
    # Test with CodeT5+
    print("\n🔵 Testing with CodeT5+ (Base Model):")
    print("-" * 60)
    analyzer_codet5 = EnhancedCodeAnalyzer(model_type="codet5")
    result_codet5 = analyzer_codet5.analyze_code_fast(test_code)
    print(f"Analysis: {result_codet5['analysis'][:300]}...")
    print(f"Quality Score: {result_codet5['quality_score']}/100")
    print(f"Execution Time: {result_codet5['execution_time']:.2f}s")
    
    # Test with Fine-tuned DeepSeek
    print("\n🟢 Testing with Fine-tuned DeepSeek:")
    print("-" * 60)
    analyzer_deepseek = EnhancedCodeAnalyzer(
        model_type="deepseek-finetuned",
        adapter_path="./fine-tuned-analyst"
    )
    result_deepseek = analyzer_deepseek.analyze_code_fast(test_code)
    print(f"Analysis: {result_deepseek['analysis'][:300]}...")
    print(f"Quality Score: {result_deepseek['quality_score']}/100")
    print(f"Execution Time: {result_deepseek['execution_time']:.2f}s")
    
    # Show model comparison
    print("\n📊 Model Comparison:")
    print("-" * 60)
    print(f"CodeT5+ Info: {analyzer_codet5.get_model_info()}")
    print(f"DeepSeek Info: {analyzer_deepseek.get_model_info()}")


if __name__ == "__main__":
    main()

