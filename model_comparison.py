#!/usr/bin/env python3
"""
Model Comparison Script for AI Code Analyzer

This script helps you compare different code analysis models
and understand their capabilities before fine-tuning.

Author: AI Code Analyzer Project
Date: 2025
"""

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    BitsAndBytesConfig
)

def compare_models():
    """
    Compare different code analysis models available on Hugging Face.
    """
    
    models_to_compare = {
        "Current Model (GPT-2)": {
            "model_id": "gpt2",
            "type": "CausalLM",
            "size": "124M",
            "code_specialized": False,
            "description": "General-purpose text model, not optimized for code"
        },
        "CodeT5+ (Recommended)": {
            "model_id": "Salesforce/codet5p-220m",
            "type": "Seq2SeqLM", 
            "size": "220M",
            "code_specialized": True,
            "description": "Specialized for code understanding and generation"
        },
        "CodeBERT": {
            "model_id": "microsoft/CodeBERT-base",
            "type": "FeatureExtraction",
            "size": "125M", 
            "code_specialized": True,
            "description": "Pre-trained on code for understanding programming languages"
        },
        "GraphCodeBERT": {
            "model_id": "microsoft/GraphCodeBERT-base",
            "type": "FeatureExtraction",
            "size": "125M",
            "code_specialized": True,
            "description": "Understands code structure and dependencies"
        },
        "InCoder": {
            "model_id": "facebook/incoder-1B",
            "type": "CausalLM",
            "size": "1B",
            "code_specialized": True,
            "description": "Code completion and analysis with large context"
        }
    }
    
    print("🤖 Code Analysis Models Comparison")
    print("=" * 80)
    
    for name, info in models_to_compare.items():
        print(f"\n📊 {name}")
        print(f"   Model ID: {info['model_id']}")
        print(f"   Type: {info['type']}")
        print(f"   Size: {info['size']}")
        print(f"   Code Specialized: {'✅ Yes' if info['code_specialized'] else '❌ No'}")
        print(f"   Description: {info['description']}")
    
    print("\n" + "=" * 80)
    print("🎯 RECOMMENDATIONS:")
    print("=" * 80)
    
    print("\n🥇 BEST CHOICE: Salesforce/codet5p-220m")
    print("   ✅ Specialized for code analysis")
    print("   ✅ Good balance of size and performance")
    print("   ✅ Works well with your training data format")
    print("   ✅ Seq2Seq architecture perfect for code analysis")
    
    print("\n🥈 ALTERNATIVE: facebook/incoder-1B")
    print("   ✅ Excellent code understanding")
    print("   ✅ Large context window")
    print("   ⚠️  Larger model (requires more resources)")
    
    print("\n🥉 FOR EXPERIMENTATION: microsoft/CodeBERT-base")
    print("   ✅ Proven for code understanding")
    print("   ✅ Good for feature extraction")
    print("   ⚠️  Different architecture (might need data format changes)")

def test_model_loading(model_id: str, model_type: str = "auto"):
    """
    Test loading a specific model to ensure it works.
    
    Args:
        model_id (str): Hugging Face model ID
        model_type (str): Model type ("auto", "causal", "seq2seq")
    """
    print(f"\n🧪 Testing model: {model_id}")
    print("-" * 50)
    
    try:
        # Load tokenizer
        print("Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            print("✅ Added padding token")
        
        # Load model
        print("Loading model...")
        if model_type == "seq2seq" or "codet5" in model_id.lower():
            model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
        else:
            model = AutoModelForCausalLM.from_pretrained(model_id)
        
        print(f"✅ Model loaded successfully!")
        print(f"   Model type: {type(model).__name__}")
        print(f"   Parameters: {sum(p.numel() for p in model.parameters()):,}")
        
        # Test with a simple code snippet
        test_code = "def add(a, b):\n    return a + b"
        inputs = tokenizer(test_code, return_tensors="pt", truncation=True, max_length=512)
        
        print(f"✅ Tokenization test passed")
        print(f"   Input tokens: {inputs['input_ids'].shape[1]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return False

def main():
    """
    Main function to run model comparison and testing.
    """
    print("🚀 AI Code Analyzer - Model Comparison Tool")
    print("=" * 80)
    
    # Show comparison
    compare_models()
    
    # Test recommended models
    print("\n\n🧪 TESTING RECOMMENDED MODELS:")
    print("=" * 80)
    
    models_to_test = [
        ("Salesforce/codet5p-220m", "seq2seq"),
        ("microsoft/CodeBERT-base", "causal"),
        ("facebook/incoder-1B", "causal")
    ]
    
    working_models = []
    
    for model_id, model_type in models_to_test:
        if test_model_loading(model_id, model_type):
            working_models.append(model_id)
    
    print(f"\n🎉 SUCCESS: {len(working_models)} models loaded successfully!")
    
    if working_models:
        print("\n📋 NEXT STEPS:")
        print("1. Choose your preferred model from the working models above")
        print("2. Run: python finetune_improved.py --model <model_id> --dry-run")
        print("3. Test the fine-tuned model with your code analyzer")
        print("\n💡 RECOMMENDED COMMAND:")
        print(f"   python finetune_improved.py --model {working_models[0]} --dry-run")

if __name__ == "__main__":
    main()
