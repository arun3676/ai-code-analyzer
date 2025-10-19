from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch
import uvicorn

app = FastAPI()

# Load model once at startup
tokenizer = None
model = None

@app.on_event("startup")
async def load_model():
    global tokenizer, model
    print("🚀 Loading fine-tuned model...")
    
    tokenizer = AutoTokenizer.from_pretrained(
        "deepseek-ai/deepseek-coder-1.3b-instruct", 
        trust_remote_code=True
    )
    tokenizer.pad_token = tokenizer.eos_token
    
    base_model = AutoModelForCausalLM.from_pretrained(
        "deepseek-ai/deepseek-coder-1.3b-instruct",
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True,
    )
    
    model = PeftModel.from_pretrained(
        base_model, 
        "arun3676/fine-tuned-code-analyzer"
    )
    print("✅ Model loaded successfully!")

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
        prompt = f"<s>[INST] Analyze this code for bugs, performance, and security issues. Give a quality score from 1-100 and provide a detailed analysis.\n\nCode:\n```\n{request.code}\n``` [/INST]"
        
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=request.max_tokens,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        analysis = response.split('[/INST]')[-1].strip()
        
        return AnalysisResponse(
            analysis=analysis,
            model="fine-tuned-deepseek",
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "fine-tuned-deepseek"}

@app.get("/")
async def root():
    return {
        "message": "Fine-tuned Code Analyzer API",
        "endpoints": {
            "POST /analyze": "Analyze code for bugs, performance, and security issues",
            "GET /health": "Health check endpoint"
        },
        "model": "fine-tuned-deepseek"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
