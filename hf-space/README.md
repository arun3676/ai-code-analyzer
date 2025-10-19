---
title: Fine-tuned Code Analyzer API
emoji: 🤖
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---

# Fine-tuned Code Analyzer API

API endpoint for code analysis using fine-tuned DeepSeek model.

## Features

- **Quality Scores**: 1-100 rating for code quality
- **Structured Analysis**: Bugs, Performance, Security sections
- **Code Improvements**: Specific suggestions with examples
- **Professional Output**: Consistent, detailed analysis format

## Usage

### POST /analyze

Analyze code for bugs, performance, and security issues.

**Request:**
```json
{
  "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
  "max_tokens": 300
}
```

**Response:**
```json
{
  "analysis": "Quality Score: 35/100\n\nBUGS:\n- No error handling\n- Infinite recursion possible\n\nPERFORMANCE ISSUES:\n- Recursive calls cause exponential time complexity\n\nSECURITY CONCERNS:\n- No input validation\n\nIMPROVEMENTS:\n1. Use memoization to avoid recursion\n2. Add input validation\n\nExample improved code:\n[Shows working fixes]",
  "model": "fine-tuned-deepseek",
  "status": "success"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "model": "fine-tuned-deepseek"
}
```

## Model Details

- **Base Model**: DeepSeek Coder 1.3B
- **Training Method**: LoRA (Low-Rank Adaptation)
- **Dataset**: 59+ high-quality code analysis examples
- **Fine-tuned for**: Code analysis, bug detection, performance optimization
