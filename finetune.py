#!/usr/bin/env python3
"""
Fine-tuning Script for AI Code Analyzer

This script fine-tunes the DeepSeek Coder model using QLoRA (Quantized LoRA) 
technique on our custom code analysis dataset.

Features:
- 4-bit quantization for memory efficiency
- LoRA adapters for parameter-efficient fine-tuning
- Supervised Fine-Tuning (SFT) using TRL
- Automatic model saving and adapter persistence

Author: AI Code Analyzer Project
Date: 2025
"""

import os
import argparse
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType
from trl import SFTTrainer
from datasets import Dataset
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_dataset(file_path: str) -> Dataset:
    """
    Load the training dataset from JSONL file.
    
    Args:
        file_path (str): Path to the analyst_dataset.jsonl file
        
    Returns:
        Dataset: Hugging Face dataset object
    """
    logger.info(f"Loading dataset from {file_path}")
    
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    
    logger.info(f"Loaded {len(data)} training samples")
    return Dataset.from_list(data)

def create_quantization_config() -> BitsAndBytesConfig:
    """
    Create 4-bit quantization configuration for memory efficiency.
    
    Returns:
        BitsAndBytesConfig: Quantization configuration
    """
    logger.info("Creating 4-bit quantization configuration")
    
    return BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

def infer_lora_target_modules(model) -> list[str]:
    """Infer suitable LoRA target modules by inspecting model modules.

    Handles common architectures:
    - LLaMA/DeepSeek-like: q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj
    - GPT-2/OPT-like: c_attn,c_proj,c_fc (when present)
    Falls back to any module names that contain 'q_proj','k_proj','v_proj','o_proj'
    found in the model.
    """
    llama_like = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
    gpt2_like = ["c_attn", "c_proj", "c_fc"]

    module_names = set(name.split(".")[-1] for name, _ in model.named_modules())

    if any(m in module_names for m in llama_like):
        return [m for m in llama_like if m in module_names]

    if any(m in module_names for m in gpt2_like):
        return [m for m in gpt2_like if m in module_names]

    # Generic attention projection fallback
    generic = [m for m in ["q_proj", "k_proj", "v_proj", "o_proj"] if m in module_names]
    if generic:
        return generic

    # Last resort: try any modules containing 'attn' or 'proj'
    heuristic = [m for m in module_names if ("attn" in m or "proj" in m)]
    return heuristic[:4] if heuristic else []


def create_lora_config(model) -> LoraConfig:
    """
    Create LoRA configuration for parameter-efficient fine-tuning.
    
    Returns:
        LoraConfig: LoRA configuration
    """
    logger.info("Creating LoRA configuration")
    
    target_modules = infer_lora_target_modules(model)
    if not target_modules:
        logger.warning("Could not infer LoRA target modules; proceeding without explicit targets (may fail)")
        target_modules = None  # Let PEFT attempt defaults

    return LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=False,
        r=16,  # Rank of adaptation
        lora_alpha=32,  # LoRA scaling parameter
        lora_dropout=0.1,  # LoRA dropout
        target_modules=target_modules,
    )

def create_training_arguments(args: argparse.Namespace) -> TrainingArguments:
    """
    Create training arguments for the fine-tuning process.
    
    Returns:
        TrainingArguments: Training configuration
    """
    logger.info("Creating training arguments")
    
    # Defaults
    num_train_epochs = args.epochs if args.epochs is not None else 3
    per_device_train_batch_size = args.batch_size if args.batch_size is not None else 1
    logging_steps = 10
    save_steps = 500
    max_steps = args.max_steps if args.max_steps is not None else -1

    if args.dry_run:
        # Make the run extremely short and avoid frequent saving
        num_train_epochs = 1 if args.epochs is None else args.epochs
        logging_steps = 1
        save_steps = 10_000_000
        if args.max_steps is None:
            max_steps = 1

    return TrainingArguments(
        output_dir="./fine-tuned-analyst",
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=per_device_train_batch_size,
        gradient_accumulation_steps=4,
        warmup_steps=100,
        learning_rate=2e-4,
        fp16=args.fp16,
        logging_steps=logging_steps,
        save_steps=save_steps,
        save_total_limit=2,
        remove_unused_columns=False,
        push_to_hub=False,
        report_to=None,  # Disable wandb/tensorboard
        dataloader_pin_memory=False,
        max_steps=max_steps,
    )

def main():
    """
    Main function to execute the fine-tuning process.
    """
    logger.info("Starting AI Code Analyzer fine-tuning process")
    
    parser = argparse.ArgumentParser(description="Fine-tune DeepSeek Coder with QLoRA")
    parser.add_argument("--model", type=str, default="deepseek-ai/deepseek-coder-1.3b-instruct", help="Base model ID (HF Hub)")
    parser.add_argument("--subset", type=int, default=None, help="Use only the first N samples from the dataset")
    parser.add_argument("--epochs", type=int, default=None, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=None, help="Per-device train batch size")
    parser.add_argument("--max-steps", type=int, default=None, help="Override maximum training steps")
    parser.add_argument("--dry-run", action="store_true", help="Run a very short demo training")
    parser.add_argument("--no-quant", action="store_true", help="Disable 4-bit quantization (useful for CPU runs)")
    args = parser.parse_args()

    # Check if CUDA is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"Using device: {device}")
    if device == "cpu":
        logger.warning("CUDA not available. Training will be slow on CPU.")
    
    # Step 1: Load the dataset
    dataset = load_dataset("analyst_dataset.jsonl")
    if args.subset is not None and args.subset > 0:
        logger.info(f"Using only the first {args.subset} samples for this run")
        dataset = dataset.select(range(min(args.subset, len(dataset))))
    
    # Step 2: Load the base model and tokenizer
    model_name = args.model
    logger.info(f"Loading model: {model_name}")
    
    # Create quantization config if enabled and likely supported
    use_quant = (device == "cuda") and (not args.no_quant)
    quantization_config = create_quantization_config() if use_quant else None
    if not use_quant:
        logger.info("Quantization disabled (CPU or --no-quant). Using standard weights.")
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Load model with quantization
    if quantization_config is not None:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=quantization_config,
            device_map="auto",
            trust_remote_code=True,
        )
        fp16 = True
    else:
        # CPU or non-quantized path
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32 if device == "cpu" else torch.float16,
            device_map="cpu" if device == "cpu" else "auto",
            low_cpu_mem_usage=True,
            trust_remote_code=True,
        )
        fp16 = (device != "cpu")
    
    # Step 3: Configure LoRA
    lora_config = create_lora_config(model)
    model = get_peft_model(model, lora_config)
    
    # Print trainable parameters
    model.print_trainable_parameters()
    
    # Step 4: Set training arguments
    # Ensure training args match device precision
    args.fp16 = fp16
    training_args = create_training_arguments(args)
    
    # Step 5: Initialize SFT Trainer
    logger.info("Initializing SFT Trainer")
    
    # Provide the tokenizer/processor via processing_class
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
        formatting_func=lambda r: r["text"],
    )
    
    # Step 6: Start training
    logger.info("Starting training...")
    trainer.train()
    
    # Step 7: Save the model
    logger.info("Saving fine-tuned model...")
    trainer.save_model()
    tokenizer.save_pretrained(training_args.output_dir)
    
    # Save LoRA adapters separately
    model.save_pretrained(f"{training_args.output_dir}/lora_adapters")
    
    logger.info("Fine-tuning completed successfully!")
    logger.info(f"Model saved to: {training_args.output_dir}")
    logger.info("LoRA adapters saved to: {}/lora_adapters".format(training_args.output_dir))

if __name__ == "__main__":
    main()
