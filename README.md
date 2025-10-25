---
title: AI Code Analyzer
emoji: 🧠
colorFrom: gray
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# AI Code Analyzer

A professional AI-powered code analysis tool with a sleek Matrix-inspired interface that leverages multiple Large Language Models (LLMs) to provide comprehensive code reviews, identify issues, and suggest improvements.

![AI Code Analyzer](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36.0-red.svg)
![Deployment](https://img.shields.io/badge/Deployment-Render-green.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

* **🤖 Multi-Model Analysis**: Compare insights from OpenAI GPT-4, Anthropic Claude, DeepSeek, and Hugging Face models
* **🎯 Fine-tuned Code Analyzer**: Custom DeepSeek model trained on 59+ code analysis examples
* **🎨 Matrix-Inspired UI**: Sleek dark theme with neon green accents and cyberpunk aesthetics
* **📊 Comprehensive Code Review**: Get quality scores, identify bugs, security issues, and performance concerns
* **🔍 Language Auto-Detection**: Automatically detects programming language or manually specify
* **📁 File Upload Support**: Upload code files directly with drag & drop functionality
* **⚡ Fast & Responsive**: Optimized for deployment with professional performance
* **🔒 Secure**: API keys are securely managed through environment variables
* **📈 Real-time Metrics**: Track analysis time, quality scores, and model comparisons
* **🌐 Remote Model Support**: Use fine-tuned models hosted on Hugging Face (always available)

## 🌐 Live Demo

**Local Deployment**: Your AI Code Analyzer is running locally at `http://localhost:8501/`

## 🛠️ Tech Stack

- **Frontend**: Streamlit with custom Matrix-inspired CSS
- **LLM Integration**: OpenAI, Anthropic, DeepSeek, Hugging Face APIs
- **Fine-tuning**: LoRA/QLoRA with Hugging Face Transformers
- **Model Hosting**: Hugging Face Hub & Spaces
- **Language**: Python 3.11+
- **Deployment**: Hugging Face Spaces (recommended for ease of use and free tier)
- **Styling**: Custom CSS with Google Fonts (Share Tech Mono, Orbitron)

## 🎯 Fine-tuned Model

This project includes a custom fine-tuned DeepSeek Coder model trained on 59+ code analysis examples:

- **Base Model**: DeepSeek Coder 1.3B
- **Training Method**: LoRA (Low-Rank Adaptation)
- **Dataset**: 59 high-quality code analysis examples
- **Features**: Quality scores, structured analysis, code improvements
- **Hosting**: Hugging Face Spaces (always online)

### Model Capabilities

The fine-tuned model provides:
- **Quality Scores**: 1-100 rating for code quality
- **Structured Analysis**: Bugs, Performance, Security sections
- **Code Improvements**: Specific suggestions with examples
- **Professional Output**: Consistent, detailed analysis format

## 🚀 Quick Start

### Prerequisites

* Python 3.11 or higher
* API keys for at least one LLM provider:  
   * OpenAI API Key  
   * Anthropic API Key  
   * DeepSeek API Key
   * **Hugging Face API Key** (recommended for free usage)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/arun3676/ai-code-analyzer.git
cd ai-code-analyzer
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
   
   Create a `.env` file in the root directory:
```env
# API Keys - Replace with your actual API keys
HUGGINGFACE_API_KEY=your_huggingface_api_key_here  # Recommended for free usage
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
GITHUB_TOKEN=your_github_token_here  # Optional, for higher API limits
```

**📚 For detailed Hugging Face setup instructions, see: [HUGGINGFACE_SETUP_GUIDE.md](HUGGINGFACE_SETUP_GUIDE.md)**

5. **Run the application:**
```bash
# Option 1: Use the startup script (recommended)
python run_app.py

# Option 2: Run directly with Streamlit
python -m streamlit run matrix_final.py --server.port 8501
```

The application will be available at `http://localhost:8501`

## 📋 Usage

### Code Analysis
1. **Upload a file** or **paste your code** in the main panel
2. **Select a model** from the dropdown (OpenAI, Anthropic, or DeepSeek)
3. **Choose analysis type**: Code Analysis or Multimodal Analysis
4. **Click "Analyze Code"** to get comprehensive insights

### File Upload
- **Drag & drop** code files directly onto the upload area
- **Supported formats**: .py, .js, .java, .cpp, .c, .cs, .go, .rs, .php, .rb, .swift, .kt, .txt
- **File size limit**: 200MB per file

### Analysis Results
- **Quality Score**: 0-100 rating with color-coded indicators
- **Summary**: Clear description of code functionality
- **Issues & Bugs**: Potential problems identified
- **Improvements**: Actionable suggestions for better code
- **Security**: Security vulnerabilities and concerns
- **Performance**: Optimization recommendations

## 🏗️ Project Structure

For a detailed explanation of the project structure, architecture, and data flow, please see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) and [ARCHITECTURE.md](ARCHITECTURE.md).

```
ai-code-analyzer/
├── .venv/                           # Virtual environment directory
├── analyzer/                          # Core analysis engine
│   ├── __init__.py                   # Package initialization
│   ├── code_analyzer.py              # Main analysis engine
│   ├── llm_clients.py                # LLM API client implementations
│   ├── prompts.py                    # Analysis prompt templates
│   └── utils.py                      # Utility functions
├── tests/                             # Automated tests
│   ├── test_matrix_final.py          # Tests for matrix_final.py utilities
│   └── test_prompts.py               # Tests for prompt generation
├── .env                              # Environment variables (create this)
├── .gitignore                        # Git ignore file
├── ARCHITECTURE.md                   # Detailed architecture documentation
├── matrix_final.py                    # Main Streamlit application
├── PROJECT_STRUCTURE.md              # High-level project structure
├── README.md                         # This file
├── requirements.txt                   # Python dependencies
├── run_app.py                         # Startup script for easy launching
└── TESTING_GUIDE.md                  # Guide for testing the application
```

## 🔧 Configuration

### Supported LLM Providers

| Provider      | Model                    | API Key Environment Variable |
| ------------- | ------------------------ | ---------------------------- |
| Hugging Face  | Mixtral-8x7B-Instruct    | HUGGINGFACE\_API\_KEY        |
| OpenAI        | GPT-4o-mini              | OPENAI\_API\_KEY             |
| Anthropic     | Claude 3 Haiku           | ANTHROPIC\_API\_KEY          |
| DeepSeek      | DeepSeek Chat            | DEEPSEEK\_API\_KEY           |

### Supported Programming Languages

- Python, JavaScript, Java, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin
- **Auto-detection** available for most languages
- **Manual selection** option for specific analysis

## 🧪 Testing

For detailed instructions on how to test the application, please refer to the [TESTING_GUIDE.md](TESTING_GUIDE.md).

To run the automated tests:
```bash
pytest
```

## 🚀 Deployment

### Deploy to Hugging Face Spaces (Recommended)

This project is configured for easy deployment on **Hugging Face Spaces**:

1.  **Fork this repository** to your GitHub account.
2.  **Create a new Space**: Go to [Hugging Face Spaces](https://huggingface.co/spaces/new) and create a new Space.
    *   Choose "Streamlit" as the Space SDK.
    *   Select "Public" or "Private" as per your preference.
    *   Connect your forked GitHub repository.
3.  **Configure Secrets**: In your Hugging Face Space settings, go to "App settings" -> "Secrets". Add your API keys:
    *   `HUGGINGFACE_API_KEY` (required for Hugging Face models)
    *   `OPENAI_API_KEY` (optional)
    *   `ANTHROPIC_API_KEY` (optional)
    *   `DEEPSEEK_API_KEY` (optional)
    *   `GITHUB_TOKEN` (optional, for higher GitHub API limits)
4.  **Wait for Deployment**: Hugging Face will automatically detect your `requirements.txt` and `matrix_final.py` and deploy your app.
5.  **Access Your App**: Once deployed, your application will be live on your Hugging Face Space URL.

### Manual Deployment

If deploying manually, use these settings:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run matrix_final.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false`

## 📊 Analysis Output

The tool provides structured analysis including:

- **🎯 Quality Score**: 0-100 rating with visual indicators
- **📋 Summary**: Clear description of code functionality  
- **🐛 Issues**: Potential bugs and logical errors
- **💡 Improvements**: Specific actionable suggestions
- **🛡️ Security**: Security vulnerabilities and concerns
- **⚡ Performance**: Optimization opportunities
- **📈 Metrics**: Analysis time, model used, code statistics

## 🎨 UI Features

- **Matrix Theme**: Dark background with neon green accents
- **Responsive Design**: Works on desktop, tablet, and mobile
- **File Upload**: Drag & drop interface with progress indicators
- **Real-time Analysis**: Live progress updates during analysis
- **Professional Layout**: Clean, organized interface
- **Custom Fonts**: Share Tech Mono and Orbitron for cyberpunk feel

## 🧪 Development

### Running Locally
```bash
# Option 1: Use the startup script (recommended)
python run_app.py

# Option 2: Start the development server directly
python -m streamlit run matrix_final.py --server.port 8501

# Option 3: With auto-reload for development
python -m streamlit run matrix_final.py --server.port 8501 --server.runOnSave true
```

### Code Structure
- **`matrix_final.py`**: Main Streamlit application with UI and routing
- **`analyzer/`**: Core analysis engine and LLM integrations
- **Custom CSS**: Embedded in the main app for Matrix theme
- **Error Handling**: Comprehensive error handling and user feedback

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

* **Streamlit** for the amazing framework
* **OpenAI** for GPT models
* **Anthropic** for Claude
* **DeepSeek** for DeepSeek Coder
* **Render** for seamless deployment
* **Google Fonts** for Share Tech Mono and Orbitron fonts

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/arun3676/ai-code-analyzer/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

## 🔗 Links

- **Live Demo**: *Your Hugging Face Space URL here*
- **Repository**: [github.com/arun3676/ai-code-analyzer](https://github.com/arun3676/ai-code-analyzer)
- **Hugging Face Spaces**: [huggingface.co/spaces](https://huggingface.co/spaces)

---

**Built with ❤️ by [Arun](https://github.com/arun3676)**