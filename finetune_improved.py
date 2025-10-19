#!/usr/bin/env python3
"""
Improved Fine-tuning Script for AI Code Analyzer

This script fine-tunes specialized code analysis models using QLoRA technique
on our custom code analysis dataset.

Key Improvements:
- Uses CodeT5+ or CodeBERT for better code understanding
- Optimized for code analysis tasks
- Better tokenization for code
- Improved training parameters

Author: AI Code Analyzer Project
Date: 2025
"""

import os
import argparse
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,  # For CodeT5 models
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

def get_model_class(model_name: str):
    """
    Determine the appropriate model class based on the model name.
    
    Args:
        model_name (str): Name of the model
        
    Returns:
        Model class: Appropriate model class for the given model
    """
    if "codet5" in model_name.lower():
        logger.info(f"Using Seq2SeqLM for CodeT5 model: {model_name}")
        return AutoModelForSeq2SeqLM
    else:
        logger.info(f"Using CausalLM for model: {model_name}")
        return AutoModelForCausalLM

def create_lora_config(model_name: str) -> LoraConfig:
    """
    Create LoRA configuration optimized for code analysis models.
    
    Args:
        model_name (str): Name of the base model
        
    Returns:
        LoraConfig: LoRA configuration
    """
    logger.info(f"Creating LoRA configuration for {model_name}")
    
    # Different target modules for different model architectures
    if "codet5" in model_name.lower():
        # CodeT5 architecture
        target_modules = ["q", "v", "k", "o", "wi_0", "wi_1", "wo"]
        task_type = TaskType.SEQ_2_SEQ_LM
    elif "codebert" in model_name.lower():
        # CodeBERT architecture
        target_modules = ["query", "key", "value", "dense"]
        task_type = TaskType.FEATURE_EXTRACTION
    else:
        # Default for most causal LM models
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
        task_type = TaskType.CAUSAL_LM
    
    return LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=target_modules,
        lora_dropout=0.1,
        bias="none",
        task_type=task_type,
    )

def create_training_arguments(args) -> TrainingArguments:
    """
    Create training arguments optimized for code analysis fine-tuning.
    
    Args:
        args: Command line arguments
        
    Returns:
        TrainingArguments: Training configuration
    """
    # Calculate training parameters
    num_train_epochs = args.epochs if args.epochs else 3
    per_device_train_batch_size = args.batch_size if args.batch_size else 2
    logging_steps = 10
    save_steps = 500
    
    # For demo runs
    if args.dry_run:
        logger.info("Running in dry-run mode with minimal training")
        num_train_epochs = 1
        per_device_train_batch_size = 1
        max_steps = 1

    return TrainingArguments(
        output_dir="./fine-tuned-analyst-improved",
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
        max_steps=1 if args.dry_run else None,
    )

def main():
    """
    Main function to execute the improved fine-tuning process.
    """
    logger.info("Starting Improved AI Code Analyzer fine-tuning process")
    
    parser = argparse.ArgumentParser(description="Fine-tune specialized code analysis models with QLoRA")
    
    # Model selection with better defaults
    parser.add_argument("--model", type=str, 
                       default="Salesforce/codet5p-220m",  # Better default for code analysis
                       help="Base model ID (HF Hub). Options: Salesforce/codet5p-220m, microsoft/CodeBERT, facebook/incoder-1B")
    
    parser.add_argument("--subset", type=int, default=None, help="Use only the first N samples from the dataset")
    parser.add_argument("--epochs", type=int, default=None, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=None, help="Per-device train batch size")
    parser.add_argument("--max-steps", type=int, default=None, help="Override maximum training steps")
    parser.add_argument("--dry-run", action="store_true", help="Run a very short demo training")
    parser.add_argument("--no-quant", action="store_true", help="Disable 4-bit quantization")
    parser.add_argument("--fp16", action="store_true", default=True, help="Use FP16 precision")
    
    args = parser.parse_args()

    # Check if CUDA is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"Using device: {device}")
    if device == "cpu":
        logger.warning("CUDA not available. Training will be slow on CPU.")
    
    # Step 1: Load the dataset
    logger.info("Step 1: Loading dataset...")
    dataset = load_dataset("analyst_dataset.jsonl")
    if args.subset is not None and args.subset > 0:
        logger.info(f"Using only the first {args.subset} samples for this run")
        dataset = dataset.select(range(min(args.subset, len(dataset))))
    
    # Step 2: Load the base model and tokenizer
    logger.info("Step 2: Loading model and tokenizer...")
    model_name = args.model
    logger.info(f"Loading model: {model_name}")
    
    # Get appropriate model class
    model_class = get_model_class(model_name)
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Add padding token if not present
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Load model with quantization if enabled
    if args.no_quant:
        logger.info("Loading model without quantization")
        model = model_class.from_pretrained(model_name)
    else:
        logger.info("Loading model with 4-bit quantization")
        quantization_config = create_quantization_config()
        model = model_class.from_pretrained(
            model_name,
            quantization_config=quantization_config,
            device_map="auto"
        )
    
    # Step 3: Create LoRA configuration
    logger.info("Step 3: Setting up LoRA configuration...")
    lora_config = create_lora_config(model_name)
    
    # Step 4: Apply LoRA to the model
    logger.info("Step 4: Applying LoRA to model...")
    model = get_peft_model(model, lora_config)
    
    # Step 5: Print trainable parameters
    model.print_trainable_parameters()
    
    # Step 6: Create training arguments
    logger.info("Step 6: Setting up training arguments...")
    training_args = create_training_arguments(args)
    
    # Step 7: Create trainer
    logger.info("Step 7: Creating trainer...")
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer,
        dataset_text_field="text",
        max_seq_length=2048,
        packing=False,
    )
    
    # Step 8: Start training
    logger.info("Step 8: Starting training...")
    logger.info(f"Training with {len(dataset)} samples")
    logger.info(f"Model: {model_name}")
    logger.info(f"Device: {device}")
    
    trainer.train()
    
    # Step 9: Save the model
    logger.info("Step 9: Saving model...")
    trainer.save_model()
    tokenizer.save_pretrained(training_args.output_dir)
    
    logger.info("Training completed successfully!")
    logger.info(f"Model saved to: {training_args.output_dir}")

if __name__ == "__main__":
    main()
