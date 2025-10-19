from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import requests
import json

app = FastAPI()

class CodeRequest(BaseModel):
    code: str
    max_tokens: int = 300

class AnalysisResponse(BaseModel):
    analysis: str
    model: str
    status: str

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_code(request: CodeRequest):
    try:
        # For now, return a mock analysis while we debug the model loading
        analysis_text = f"""
Quality Score: 75/100

BUGS:
- No error handling for edge cases
- Potential infinite recursion for large inputs

PERFORMANCE ISSUES:
- Recursive approach is inefficient for large numbers
- No memoization implemented

SECURITY CONCERNS:
- No input validation
- Could cause stack overflow with large inputs

IMPROVEMENTS:
1. Add input validation
2. Implement iterative solution or memoization
3. Add error handling for edge cases

Example improved code:
```python
def fibonacci_improved(n):
    if n < 0:
        raise ValueError("Input must be non-negative")
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```
"""
        
        return AnalysisResponse(
            analysis=analysis_text,
            model="fine-tuned-deepseek-mock",
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "fine-tuned-deepseek-mock"}

@app.get("/")
async def root():
    return {
        "message": "Fine-tuned Code Analyzer API",
        "endpoints": {
            "POST /analyze": "Analyze code for bugs, performance, and security issues",
            "GET /health": "Health check endpoint"
        },
        "model": "fine-tuned-deepseek-mock",
        "status": "running"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)