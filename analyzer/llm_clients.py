import os
from typing import Optional, Dict, Any
from dataclasses import dataclass
import openai
import anthropic
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Force reload environment variables
load_dotenv(override=True)

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
        # Debug: Print available API keys
        print("🔍 Initializing LLM clients...")
        
        # OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            print(f"✅ OpenAI API key found: {openai_key[:8]}...{openai_key[-4:]}")
            self.clients["openai"] = openai.OpenAI(api_key=openai_key)
        else:
            print("❌ OpenAI API key not found")
        
        # Anthropic
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            print(f"✅ Anthropic API key found: {anthropic_key[:8]}...{anthropic_key[-4:]}")
            self.clients["anthropic"] = anthropic.Anthropic(api_key=anthropic_key)
        else:
            print("❌ Anthropic API key not found")
        
        # DeepSeek (uses OpenAI-compatible API)
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        if deepseek_key:
            print(f"✅ DeepSeek API key found: {deepseek_key[:8]}...{deepseek_key[-4:]}")
            self.clients["deepseek"] = openai.OpenAI(
                api_key=deepseek_key,
                base_url="https://api.deepseek.com/v1"
            )
        else:
            print("❌ DeepSeek API key not found")

        # Mercury API (OpenAI-compatible via Inception Labs)
        # Support both MERCURY_API_KEY and INCEPTION_API_KEY
        mercury_key = os.getenv("MERCURY_API_KEY") or os.getenv("INCEPTION_API_KEY")
        if mercury_key:
            print(f"✅ Mercury API key found: {mercury_key[:8]}...{mercury_key[-4:]}")
            try:
                # Prefer explicit base URL envs; default to Inception Labs documented endpoint
                base_url = (
                    os.getenv("MERCURY_BASE_URL")
                    or os.getenv("INCEPTION_BASE_URL")
                    or "https://api.inceptionlabs.ai/v1"
                )
                self.clients["mercury"] = openai.OpenAI(api_key=mercury_key, base_url=base_url)
                print("✅ Mercury client initialized successfully")
            except Exception as e:
                print(f"⚠️  Mercury client initialization failed: {e}")
                # Still add to clients so it appears in UI, but will show error when used
                self.clients["mercury"] = None
        else:
            print("❌ Mercury API key not found")

        # Check for Hugging Face API key with multiple possible names
        hf_token = os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv("HF_TOKEN")
        if hf_token:
            self.clients["huggingface"] = InferenceClient(token=hf_token)
    
    def get_available_models(self) -> Dict[str, str]:
        """Return available models with display names."""
        models = {}
        if "openai" in self.clients:
            models["openai"] = "OpenAI GPT-4o-mini"
        if "anthropic" in self.clients:
            models["anthropic"] = "Claude 4.5 Haiku"
        if "deepseek" in self.clients:
            models["deepseek"] = "DeepSeek Coder V2"
        if "mercury" in self.clients:
            models["mercury"] = "Mercury Fast LLM"
        if "huggingface" in self.clients:
            models["huggingface"] = "Hugging Face (Mixtral)"
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
                    model="OpenAI GPT-4o-mini",
                    success=True
                )
            
            elif model == "anthropic" and "anthropic" in self.clients:
                response = self.clients["anthropic"].messages.create(
                    model="claude-3-5-haiku-20241022",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=temperature
                )
                return LLMResponse(
                    content=response.content[0].text,
                    model="Claude 4.5 Haiku",
                    success=True
                )
            
            elif model == "deepseek" and "deepseek" in self.clients:
                try:
                    response = self.clients["deepseek"].chat.completions.create(
                        model="deepseek-coder-v2",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=temperature
                    )
                    return LLMResponse(
                        content=response.choices[0].message.content,
                        model="DeepSeek Coder V2",
                        success=True
                    )
                except Exception as deepseek_error:
                    # Try with alternative model name if the first one fails
                    try:
                        response = self.clients["deepseek"].chat.completions.create(
                            model="deepseek-coder",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=temperature
                        )
                        return LLMResponse(
                            content=response.choices[0].message.content,
                            model="DeepSeek Coder V2",
                            success=True
                        )
                    except Exception as second_error:
                        return LLMResponse(
                            content="",
                            model="DeepSeek Coder V2",
                            success=False,
                            error=f"DeepSeek API Error: {str(deepseek_error)}. Also tried alternative model: {str(second_error)}"
                        )

            elif model == "mercury" and "mercury" in self.clients:
                # Check if Mercury client is properly initialized
                if self.clients["mercury"] is None:
                    return LLMResponse(
                        content="",
                        model="Mercury Fast LLM",
                        success=False,
                        error="Mercury API client not properly initialized. Check your API key and endpoint configuration."
                    )

                # Build candidate base URLs (env first, then known defaults)
                candidate_base_urls = []
                if os.getenv("MERCURY_BASE_URL"):
                    candidate_base_urls.append(os.getenv("MERCURY_BASE_URL"))
                if os.getenv("INCEPTION_BASE_URL"):
                    candidate_base_urls.append(os.getenv("INCEPTION_BASE_URL"))
                candidate_base_urls.extend([
                    "https://api.inceptionlabs.ai/v1",
                    "https://api.mercury.ai/v1",
                    "https://api.mercury.ai",
                ])

                # Candidate model names (env first, then fallbacks)
                candidate_models = []
                env_model = os.getenv("MERCURY_MODEL_NAME") or os.getenv("INCEPTION_MODEL_NAME")
                if env_model:
                    candidate_models.append(env_model)
                candidate_models.extend(["mercury", "mercury-fast", "mercury-pro", "gpt-4", "gpt-3.5-turbo"])

                last_error: Optional[str] = None

                for base_url in candidate_base_urls:
                    try:
                        client = openai.OpenAI(
                            api_key=(os.getenv("MERCURY_API_KEY") or os.getenv("INCEPTION_API_KEY")),
                            base_url=base_url,
                        )
                        for mercury_model in candidate_models:
                            try:
                                response = client.chat.completions.create(
                                    model=mercury_model,
                                    messages=[{"role": "user", "content": prompt}],
                                    temperature=temperature,
                                    max_tokens=2000,
                                )
                                return LLMResponse(
                                    content=response.choices[0].message.content,
                                    model="Mercury Fast LLM",
                                    success=True,
                                )
                            except Exception as model_error:
                                last_error = f"{type(model_error).__name__}: {str(model_error)}"
                                continue
                    except Exception as client_error:
                        last_error = f"{type(client_error).__name__}: {str(client_error)}"
                        continue

                # If all attempts failed, provide a consolidated error
                if last_error and "503" in last_error:
                    return LLMResponse(
                        content="",
                        model="Mercury Fast LLM",
                        success=False,
                        error=(
                            "Mercury/Inception API returned 503 across endpoints. Service may be down. "
                            "Tried endpoints: " + ", ".join(candidate_base_urls)
                        ),
                    )
                return LLMResponse(
                    content="",
                    model="Mercury Fast LLM",
                    success=False,
                    error=(
                        "Mercury API request failed after trying multiple endpoints and models. "
                        f"Last error: {last_error or 'unknown error'}"
                    ),
                )

            elif model == "huggingface" and "huggingface" in self.clients:
                try:
                    # Use chat completion API for Mixtral model (most compatible)
                    response = self.clients["huggingface"].chat_completion(
                        messages=[{"role": "user", "content": prompt}],
                        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                        max_tokens=2000,
                        temperature=temperature if temperature > 0 else 0.1,
                    )
                    return LLMResponse(
                        content=response.choices[0].message.content,
                        model="Hugging Face (Mixtral)",
                        success=True
                    )
                except Exception as hf_error:
                    # Fallback to text generation with a simpler model
                    try:
                        response = self.clients["huggingface"].text_generation(
                            prompt,
                            model="microsoft/DialoGPT-medium",
                            max_new_tokens=2000,
                            temperature=temperature if temperature > 0 else 0.1,
                        )
                        return LLMResponse(
                            content=response,
                            model="Hugging Face (DialoGPT)",
                            success=True
                        )
                    except Exception as fallback_error:
                        return LLMResponse(
                            content="",
                            model="Hugging Face (Mixtral)",
                            success=False,
                            error=f"Hugging Face API Error: {str(hf_error)}. Fallback also failed: {str(fallback_error)}"
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