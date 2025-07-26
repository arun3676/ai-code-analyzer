import os
from typing import Optional, Dict, Any
from dataclasses import dataclass
import openai
import anthropic
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

@dataclass
class LLMResponse:
    content: str
    model: str
    success: bool
    error: Optional[str] = None

class LLMClientManager:
    """Manages connections to different LLM providers."""
    
    def __init__(self):
        self.clients = {}
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize available LLM clients based on API keys."""
        # OpenAI
        if os.getenv("OPENAI_API_KEY"):
            self.clients["openai"] = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Anthropic
        if os.getenv("ANTHROPIC_API_KEY"):
            self.clients["anthropic"] = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # DeepSeek (uses OpenAI-compatible API)
        if os.getenv("DEEPSEEK_API_KEY"):
            self.clients["deepseek"] = openai.OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com/v1"
            )
    
    def get_available_models(self) -> Dict[str, str]:
        """Return available models with display names."""
        models = {}
        if "openai" in self.clients:
            models["openai"] = "OpenAI GPT-4"
        if "anthropic" in self.clients:
            models["anthropic"] = "Claude 3"
        if "deepseek" in self.clients:
            models["deepseek"] = "DeepSeek Coder"
        return models
    
    def query(self, model: str, prompt: str, temperature: float = 0.1) -> LLMResponse:
        """Query a specific LLM model."""
        try:
            if model == "openai" and "openai" in self.clients:
                response = self.clients["openai"].chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature
                )
                return LLMResponse(
                    content=response.choices[0].message.content,
                    model="OpenAI GPT-4",
                    success=True
                )
            
            elif model == "anthropic" and "anthropic" in self.clients:
                response = self.clients["anthropic"].messages.create(
                    model="claude-3-haiku-20240307",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=temperature
                )
                return LLMResponse(
                    content=response.content[0].text,
                    model="Claude 3 Haiku",
                    success=True
                )
            
            elif model == "deepseek" and "deepseek" in self.clients:
                try:
                    response = self.clients["deepseek"].chat.completions.create(
                        model="deepseek-coder",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=temperature
                    )
                    return LLMResponse(
                        content=response.choices[0].message.content,
                        model="DeepSeek Coder",
                        success=True
                    )
                except Exception as deepseek_error:
                    # Try with alternative model name if the first one fails
                    try:
                        response = self.clients["deepseek"].chat.completions.create(
                            model="deepseek-chat",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=temperature
                        )
                        return LLMResponse(
                            content=response.choices[0].message.content,
                            model="DeepSeek Coder",
                            success=True
                        )
                    except Exception as second_error:
                        return LLMResponse(
                            content="",
                            model="DeepSeek Coder",
                            success=False,
                            error=f"DeepSeek API Error: {str(deepseek_error)}. Also tried alternative model: {str(second_error)}"
                        )
            
            else:
                return LLMResponse(
                    content="",
                    model=model,
                    success=False,
                    error=f"Model {model} not available or not configured"
                )
                
        except Exception as e:
            return LLMResponse(
                content="",
                model=model,
                success=False,
                error=str(e)
            ) 