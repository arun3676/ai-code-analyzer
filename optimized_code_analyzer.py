#!/usr/bin/env python3
"""
Optimized CodeT5+ Code Analyzer

This script implements CodeT5+ with multiple speed optimizations:
- FP16 by default (fastest on your GPU); optional INT8/INT4
- Response streaming for better UX
- Progress indicators
- Result caching
- Optimized generation parameters

Author: AI Code Analyzer Project
Date: 2025
"""

import torch
import time
import hashlib
import json
import os
from typing import Dict, Any, Optional, Generator
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, BitsAndBytesConfig
from tqdm import tqdm
import streamlit as st

class OptimizedCodeAnalyzer:
    """
    Optimized CodeT5+ analyzer with speed improvements.
    """
    
    def __init__(
        self,
        model_id: str = "Salesforce/codet5p-220m",
        cache_dir: str = "./cache",
        precision: str = "fp16",  # one of: fp16 | int8 | int4
        quick_max_new_tokens: int = 180,
        detailed_max_new_tokens: int = 240,
    ):
        """
        Initialize the optimized analyzer.
        
        Args:
            model_id: Hugging Face model ID
            cache_dir: Directory to store cached results
        """
        self.model_id = model_id
        self.cache_dir = cache_dir
        self.model = None
        self.tokenizer = None
        self.cache = {}
        self.precision = precision.lower().strip()
        self.quick_max_new_tokens = quick_max_new_tokens
        self.detailed_max_new_tokens = detailed_max_new_tokens
        
        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)
        
        # Load cache if exists
        self._load_cache()
    
    def _create_quantization_config(self) -> BitsAndBytesConfig:
        """
        Create 4-bit quantization configuration for faster inference.
        
        Returns:
            BitsAndBytesConfig: Quantization configuration
        """
        # Default to INT4 nf4 when precision==int4; callers should not use this
        return BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
    
    def _load_model(self):
        """
        Load the model with optimizations.
        """
        if self.model is not None:
            return
        
        print("🚀 Loading optimized CodeT5+ model...")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Decide precision based on config
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
            # Fallback to fp16
            dtype = torch.float16
            banner = f"Unknown precision '{self.precision}', defaulting to FP16"

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.model_id,
            device_map="auto",
            dtype=dtype,
            quantization_config=quantization_config,
        )

        print(f"✅ Model loaded with {banner}!")
    
    def _get_cache_key(self, code: str) -> str:
        """
        Generate cache key for code.
        
        Args:
            code: Code to analyze
            
        Returns:
            str: Cache key
        """
        return hashlib.md5(code.encode()).hexdigest()
    
    def _load_cache(self):
        """
        Load cached results from disk.
        """
        cache_file = os.path.join(self.cache_dir, "analysis_cache.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    self.cache = json.load(f)
                print(f"📁 Loaded {len(self.cache)} cached analyses")
            except:
                self.cache = {}
    
    def _save_cache(self):
        """
        Save cache to disk.
        """
        cache_file = os.path.join(self.cache_dir, "analysis_cache.json")
        with open(cache_file, 'w') as f:
            json.dump(self.cache, f)
    
    def _check_cache(self, code: str) -> Optional[Dict[str, Any]]:
        """
        Check if analysis is cached.
        
        Args:
            code: Code to analyze
            
        Returns:
            Optional[Dict]: Cached result or None
        """
        cache_key = self._get_cache_key(code)
        return self.cache.get(cache_key)
    
    def _save_to_cache(self, code: str, result: Dict[str, Any]):
        """
        Save analysis result to cache.
        
        Args:
            code: Code that was analyzed
            result: Analysis result
        """
        cache_key = self._get_cache_key(code)
        self.cache[cache_key] = result
        self._save_cache()
    
    def analyze_code_streaming(
        self,
        code: str,
        show_progress: bool = True,
        mode: str = "detailed",  # "quick" | "detailed"
    ) -> Generator[str, None, Dict[str, Any]]:
        """
        Analyze code with streaming response and progress indicators.
        
        Args:
            code: Code to analyze
            show_progress: Whether to show progress indicators
            
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
        
        # Create analysis prompt
        prompt = f"""Analyze this code for bugs, performance issues, and security concerns:

{code}

Analysis:"""
        
        # Tokenize input
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True,
        )
        device = next(self.model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Generate analysis with optimized parameters
        start_time = time.time()
        
        if show_progress:
            print("🔍 Analyzing code...")
            progress_bar = tqdm(total=100, desc="Analysis Progress")
        
        try:
            with torch.no_grad():
                # Use optimized generation parameters for speed
                max_new = self.detailed_max_new_tokens if mode == "detailed" else self.quick_max_new_tokens
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
            
            if show_progress:
                progress_bar.update(50)
            
            # Decode analysis
            analysis = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            analysis_text = analysis[len(prompt):].strip()
            
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
            
        Returns:
            Dict: Analysis result
        """
        # Check cache first
        cached_result = self._check_cache(code)
        if cached_result:
            cached_result["cached"] = True
            return cached_result
        
        # Load model if not loaded
        self._load_model()
        
        # Create analysis prompt
        prompt = f"""Analyze this code for bugs, performance issues, and security concerns:

{code}

Analysis:"""
        
        # Tokenize input
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True,
        )
        device = next(self.model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Generate analysis with speed optimizations
        start_time = time.time()
        
        with torch.no_grad():
            max_new = self.quick_max_new_tokens if mode == "quick" else self.detailed_max_new_tokens
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
        
        # Decode analysis
        analysis = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        analysis_text = analysis[len(prompt):].strip()
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(analysis_text)
        
        total_time = time.time() - start_time
        
        # Create result
        result = {
            "analysis": analysis_text,
            "quality_score": quality_score,
            "execution_time": total_time,
            "model": self.model_id,
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
        score = 0
        analysis_lower = analysis_text.lower()
        
        # Check for different types of analysis (20 points each)
        if any(word in analysis_lower for word in ['bug', 'error', 'issue', 'problem', 'flaw']):
            score += 20
        
        if any(word in analysis_lower for word in ['performance', 'slow', 'efficient', 'complexity', 'optimization']):
            score += 20
        
        if any(word in analysis_lower for word in ['security', 'vulnerability', 'safe', 'unsafe', 'risk']):
            score += 20
        
        if any(word in analysis_lower for word in ['suggest', 'improve', 'better', 'recommend', 'fix', 'solution']):
            score += 20
        
        # Bonus for detailed analysis
        if len(analysis_text) > 200:
            score += 10
        if len(analysis_text) > 500:
            score += 10
        
        return min(score, 100)
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dict: Model information
        """
        if self.model is None:
            return {"status": "Model not loaded"}
        
        param_count = sum(p.numel() for p in self.model.parameters())
        device = next(self.model.parameters()).device
        
        return {
            "model_id": self.model_id,
            "parameters": param_count,
            "device": str(device),
            "precision": self.precision,
            "quick_max_new_tokens": self.quick_max_new_tokens,
            "detailed_max_new_tokens": self.detailed_max_new_tokens,
            "cache_size": len(self.cache)
        }

def main():
    """
    Demo of the optimized analyzer.
    """
    print("🚀 Optimized CodeT5+ Analyzer Demo")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = OptimizedCodeAnalyzer()
    
    # Test code
    test_code = """
def calculate_fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

# This will be slow for large numbers
result = calculate_fibonacci(35)
print(result)
"""
    
    print(f"Test Code:\n{test_code}")
    print("=" * 60)
    
    # Test streaming analysis
    print("\n🔍 Streaming Analysis:")
    print("-" * 40)
    
    for partial_result in analyzer.analyze_code_streaming(test_code):
        print(partial_result)
    
    # Test fast analysis
    print("\n⚡ Fast Analysis:")
    print("-" * 40)
    
    result = analyzer.analyze_code_fast(test_code)
    print(f"Analysis: {result['analysis']}")
    print(f"Quality Score: {result['quality_score']}/100")
    print(f"Execution Time: {result['execution_time']:.2f}s")
    print(f"Cached: {result['cached']}")
    
    # Show model info
    print("\n📊 Model Information:")
    print("-" * 40)
    model_info = analyzer.get_model_info()
    for key, value in model_info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
