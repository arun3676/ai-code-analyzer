# LLM Code Analyzer

A professional code analysis tool that leverages multiple Large Language Models (LLMs) to provide comprehensive code reviews, identify issues, and suggest improvements.

![LLM Code Analyzer](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- **🤖 Multi-Model Analysis**: Compare insights from OpenAI GPT-4, Anthropic Claude, Google Gemini, and DeepSeek
- **📊 Comprehensive Code Review**: Get quality scores, identify bugs, security issues, and performance concerns
- **🔍 Language Auto-Detection**: Automatically detects programming language or manually specify
- **🎨 Clean Professional UI**: Built with Streamlit for a modern, responsive interface
- **⚡ Lightweight & Fast**: Optimized for deployment on platforms like Render
- **🔒 Secure**: API keys are securely managed through environment variables
- **📈 Real-time Metrics**: Track analysis time, quality scores, and model comparisons
- **🤝 Consensus Analysis**: Identify issues that multiple models agree on

## 🌐 Live Demo

[Try it on Render](https://your-app-name.onrender.com) *(Coming Soon)*

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM Integration**: OpenAI, Anthropic, Google Gemini, DeepSeek APIs
- **Language**: Python 3.11+
- **Deployment**: Render (or any Python hosting platform)

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- API keys for at least one LLM provider:
  - OpenAI API Key
  - Anthropic API Key
  - Google Gemini API Key
  - DeepSeek API Key

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/llm-code-analyzer.git
cd llm-code-analyzer
```

2. **Create a virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
   
   Copy the `.env` file and add your API keys:
```bash
cp .env .env.local
```

Edit `.env.local` with your actual API keys:
```env
# API Keys - Replace with your actual API keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GEMINI_API_KEY=your_google_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

5. **Run the application:**
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 📋 Usage

### Single Model Analysis
1. Paste your code in the left panel
2. Select a specific LLM model from the dropdown
3. Choose the programming language (or use auto-detect)
4. Click "🚀 Analyze Code"

### Multi-Model Comparison
1. Paste your code in the left panel
2. Check "Compare All Models"
3. Click "🚀 Analyze Code"
4. View results in separate tabs for each model
5. See consensus issues identified by multiple models

### Sample Code
Use the "Sample Code" section in the sidebar to quickly load example Python or JavaScript code for testing.

## 🏗️ Project Structure

```
llm-code-analyzer/
├── .env                    # Environment variables template
├── .gitignore             # Git ignore patterns
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── app.py                # Main Streamlit application
└── analyzer/
    ├── __init__.py       # Package initialization
    ├── llm_clients.py    # LLM API client implementations
    ├── code_analyzer.py  # Main analysis engine
    ├── prompts.py        # Analysis prompt templates
    └── utils.py          # Utility functions
```

## 🔧 Configuration

### Supported LLM Providers

| Provider | Model | API Key Environment Variable |
|----------|-------|------------------------------|
| OpenAI | GPT-4o-mini | `OPENAI_API_KEY` |
| Anthropic | Claude 3 Haiku | `ANTHROPIC_API_KEY` |
| Google | Gemini Pro | `GEMINI_API_KEY` |
| DeepSeek | DeepSeek Chat | `DEEPSEEK_API_KEY` |

### Supported Programming Languages

- Python
- JavaScript
- Java
- C++
- C#
- Go
- Rust
- And more (auto-detection available)

## 🚀 Deployment

### Deploy to Render

1. Fork this repository
2. Create a new Web Service on [Render](https://render.com)
3. Connect your GitHub repository
4. Configure environment variables in Render dashboard
5. Deploy with these settings:  
   * **Build Command**: `pip install -r requirements.txt`  
   * **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false`

### Deploy to Heroku

1. Install the Heroku CLI
2. Create a `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```
3. Deploy:
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key_here
heroku config:set ANTHROPIC_API_KEY=your_key_here
# ... add other API keys
git push heroku main
```

### Deploy to Railway

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on push

## 🧪 Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Formatting
```bash
black analyzer/ app.py
```

### Type Checking
```bash
mypy analyzer/
```

## 📊 Analysis Output

The tool provides structured analysis including:

- **Quality Score**: 0-100 rating of code quality
- **Summary**: Brief description of the code's purpose
- **Strengths**: What the code does well
- **Issues**: Potential bugs and problems
- **Suggestions**: Specific improvement recommendations
- **Security Concerns**: Potential security vulnerabilities
- **Performance Notes**: Performance optimization opportunities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing framework
- [OpenAI](https://openai.com/) for GPT models
- [Anthropic](https://anthropic.com/) for Claude
- [Google](https://ai.google.dev/) for Gemini
- [DeepSeek](https://www.deepseek.com/) for DeepSeek Coder

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/llm-code-analyzer/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

---

**Built with ❤️ by [Your Name](https://github.com/yourusername)** 