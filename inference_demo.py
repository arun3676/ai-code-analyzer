#!/usr/bin/env python3
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Settings
BASE_MODEL = os.environ.get("BASE_MODEL", "gpt2")
ADAPTER_DIR = os.environ.get("ADAPTER_DIR", "./fine-tuned-analyst/lora_adapters")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def load_model_and_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float32 if DEVICE == "cpu" else torch.float16,
        device_map="cpu" if DEVICE == "cpu" else "auto",
        trust_remote_code=True,
        low_cpu_mem_usage=True,
    )
    model = PeftModel.from_pretrained(model, ADAPTER_DIR)
    model.to(DEVICE)
    model.eval()
    return model, tokenizer


def generate(prompt: str, max_new_tokens: int = 256) -> str:
    model, tokenizer = load_model_and_tokenizer()
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_p=0.9,
            temperature=0.7,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )
    text = tokenizer.decode(out[0], skip_special_tokens=True)
    return text


if __name__ == "__main__":
    # A tiny prompt using the same schema
    code = """def add_item(item, items=[]):\n    items.append(item)\n    return items\n"""
    inst = (
        "<s>[INST] Analyze this code for bugs, performance, and security issues. "
        "Give a quality score from 1-100 and provide a detailed analysis. \n\nCode:\n```" + code + "``` [/INST]"
    )
    print("Device:", DEVICE)
    print("Base model:", BASE_MODEL)
    print("Adapters:", ADAPTER_DIR)
    print("\n--- Generated Output ---\n")
    print(generate(inst, max_new_tokens=200))
