#!/usr/bin/env python3
"""
Detailed Model Comparison Script

This script compares CodeT5+ and CodeBERT side by side
to show exactly how much better each model is for code analysis.
"""

import torch
import time
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM
import json

def analyze_code_with_model(model_id: str, model_type: str, test_code: str, test_name: str):
    """
    Analyze code with a specific model and return detailed results.
    """
    print(f"\n🧪 Testing {test_name}")
    print("=" * 80)
    
    start_time = time.time()
    
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Load model
        if model_type == "seq2seq":
            model = AutoModelForSeq2SeqLM.from_pretrained(
                model_id, 
                torch_dtype=torch.float16,
                device_map="auto"
            )
        else:
            model = AutoModelForCausalLM.from_pretrained(
                model_id,
                torch_dtype=torch.float16,
                device_map="auto"
            )
        
        # Get model info
        param_count = sum(p.numel() for p in model.parameters())
        
        # Create analysis prompt
        prompt = f"""Analyze this code for bugs, performance issues, and security concerns:

{test_code}

Analysis:"""
        
        # Tokenize
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Generate analysis
        generation_start = time.time()
        with torch.no_grad():
            if model_type == "seq2seq":
                outputs = model.generate(
                    inputs["input_ids"],
                    max_length=inputs["input_ids"].shape[1] + 300,
                    num_beams=4,
                    early_stopping=True,
                    do_sample=False,
                    temperature=0.7
                )
            else:
                outputs = model.generate(
                    inputs["input_ids"],
                    max_length=inputs["input_ids"].shape[1] + 300,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                    top_p=0.9
                )
        
        generation_time = time.time() - generation_start
        
        # Decode analysis
        analysis = tokenizer.decode(outputs[0], skip_special_tokens=True)
        analysis_text = analysis[len(prompt):].strip()
        
        total_time = time.time() - start_time
        
        # Analyze the quality of the analysis
        quality_score = analyze_analysis_quality(analysis_text, test_code)
        
        return {
            "model_id": model_id,
            "model_type": model_type,
            "test_name": test_name,
            "success": True,
            "analysis": analysis_text,
            "total_time": total_time,
            "generation_time": generation_time,
            "parameters": param_count,
            "quality_score": quality_score,
            "analysis_length": len(analysis_text)
        }
        
    except Exception as e:
        return {
            "model_id": model_id,
            "model_type": model_type,
            "test_name": test_name,
            "success": False,
            "error": str(e),
            "total_time": time.time() - start_time
        }

def analyze_analysis_quality(analysis_text: str, original_code: str):
    """
    Analyze the quality of the code analysis.
    Returns a score from 0-100 based on various factors.
    """
    score = 0
    
    # Check for different types of analysis
    analysis_lower = analysis_text.lower()
    
    # Bug detection (20 points)
    if any(word in analysis_lower for word in ['bug', 'error', 'issue', 'problem', 'flaw']):
        score += 20
    
    # Performance analysis (20 points)
    if any(word in analysis_lower for word in ['performance', 'slow', 'efficient', 'complexity', 'optimization']):
        score += 20
    
    # Security analysis (20 points)
    if any(word in analysis_lower for word in ['security', 'vulnerability', 'safe', 'unsafe', 'risk']):
        score += 20
    
    # Code structure analysis (20 points)
    if any(word in analysis_lower for word in ['structure', 'design', 'pattern', 'architecture', 'organization']):
        score += 20
    
    # Suggestions/improvements (20 points)
    if any(word in analysis_lower for word in ['suggest', 'improve', 'better', 'recommend', 'fix', 'solution']):
        score += 20
    
    # Bonus points for detailed analysis
    if len(analysis_text) > 200:
        score += 10
    if len(analysis_text) > 500:
        score += 10
    
    return min(score, 100)

def compare_models():
    """
    Compare CodeT5+ and CodeBERT on multiple test cases.
    """
    
    # Test cases with different types of code issues
    test_cases = [
        {
            "name": "Performance Issue (Recursive Fibonacci)",
            "code": """
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
        },
        {
            "name": "Security Issue (SQL Injection)",
            "code": """
import sqlite3

def get_user(email):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    # vulnerable string interpolation
    q = f"SELECT id, email, role FROM users WHERE email = '{email}'"
    rows = cur.execute(q).fetchall()
    conn.close()
    return rows[0] if rows else None

# Usage
user = get_user("admin@example.com")
"""
        },
        {
            "name": "Bug Issue (Division by Zero)",
            "code": """
def divide_numbers(a, b):
    return a / b

def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    return divide_numbers(total, count)

# This will crash with empty list
result = calculate_average([])
print(result)
"""
        }
    ]
    
    # Models to compare
    models = [
        {
            "id": "Salesforce/codet5p-220m",
            "type": "seq2seq",
            "name": "CodeT5+ (Recommended)"
        },
        {
            "id": "microsoft/CodeBERT-base",
            "type": "causal",
            "name": "CodeBERT (Alternative)"
        }
    ]
    
    print("🚀 DETAILED MODEL COMPARISON")
    print("=" * 100)
    print("Testing both models on multiple code analysis scenarios...")
    
    all_results = []
    
    for test_case in test_cases:
        print(f"\n📋 TEST CASE: {test_case['name']}")
        print("=" * 100)
        print(f"Code to analyze:\n{test_case['code']}")
        print("=" * 100)
        
        test_results = []
        
        for model in models:
            result = analyze_code_with_model(
                model["id"], 
                model["type"], 
                test_case["code"], 
                model["name"]
            )
            test_results.append(result)
            all_results.append(result)
        
        # Show side-by-side comparison for this test case
        print(f"\n📊 SIDE-BY-SIDE COMPARISON:")
        print("-" * 100)
        
        for result in test_results:
            if result["success"]:
                print(f"\n🤖 {result['test_name']}:")
                print(f"   ⏱️  Time: {result['total_time']:.2f}s")
                print(f"   📊 Parameters: {result['parameters']:,}")
                print(f"   🎯 Quality Score: {result['quality_score']}/100")
                print(f"   📝 Analysis Length: {result['analysis_length']} chars")
                print(f"   📄 Analysis:")
                print(f"   {result['analysis'][:200]}{'...' if len(result['analysis']) > 200 else ''}")
            else:
                print(f"\n❌ {result['test_name']}: FAILED - {result['error']}")
    
    # Overall comparison
    print(f"\n🏆 OVERALL COMPARISON SUMMARY")
    print("=" * 100)
    
    # Group results by model
    codet5_results = [r for r in all_results if r.get("model_id") == "Salesforce/codet5p-220m" and r["success"]]
    codebert_results = [r for r in all_results if r.get("model_id") == "microsoft/CodeBERT-base" and r["success"]]
    
    if codet5_results and codebert_results:
        # Calculate averages
        codet5_avg_time = sum(r["total_time"] for r in codet5_results) / len(codet5_results)
        codet5_avg_quality = sum(r["quality_score"] for r in codet5_results) / len(codet5_results)
        codet5_avg_length = sum(r["analysis_length"] for r in codet5_results) / len(codet5_results)
        
        codebert_avg_time = sum(r["total_time"] for r in codebert_results) / len(codebert_results)
        codebert_avg_quality = sum(r["quality_score"] for r in codebert_results) / len(codebert_results)
        codebert_avg_length = sum(r["analysis_length"] for r in codebert_results) / len(codebert_results)
        
        print(f"\n📈 AVERAGE PERFORMANCE:")
        print(f"CodeT5+:")
        print(f"   ⏱️  Time: {codet5_avg_time:.2f}s")
        print(f"   🎯 Quality: {codet5_avg_quality:.1f}/100")
        print(f"   📝 Length: {codet5_avg_length:.0f} chars")
        
        print(f"\nCodeBERT:")
        print(f"   ⏱️  Time: {codebert_avg_time:.2f}s")
        print(f"   🎯 Quality: {codebert_avg_quality:.1f}/100")
        print(f"   📝 Length: {codebert_avg_length:.0f} chars")
        
        # Calculate improvements
        time_ratio = codebert_avg_time / codet5_avg_time
        quality_diff = codet5_avg_quality - codebert_avg_quality
        length_ratio = codet5_avg_length / codebert_avg_length
        
        print(f"\n🎯 IMPROVEMENT ANALYSIS:")
        print(f"Speed: CodeBERT is {time_ratio:.1f}x faster than CodeT5+")
        print(f"Quality: CodeT5+ is {quality_diff:.1f} points better than CodeBERT")
        print(f"Detail: CodeT5+ gives {length_ratio:.1f}x more detailed analysis")
        
        # Final recommendation
        print(f"\n🏆 FINAL RECOMMENDATION:")
        if quality_diff > 10:
            print(f"✅ Use CodeT5+ - Significantly better analysis quality ({quality_diff:.1f} points better)")
            print(f"   Trade-off: {time_ratio:.1f}x slower, but much better results")
        elif quality_diff > 5:
            print(f"✅ Use CodeT5+ - Better analysis quality ({quality_diff:.1f} points better)")
            print(f"   Trade-off: {time_ratio:.1f}x slower, but better results")
        else:
            print(f"🤔 Both models are similar in quality")
            print(f"   Choose CodeBERT for speed, CodeT5+ for slightly better quality")

def main():
    """
    Main function to run the detailed comparison.
    """
    compare_models()

if __name__ == "__main__":
    main()
