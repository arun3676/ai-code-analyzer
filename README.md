# AI Code Analyzer

A professional AI-powered code analysis tool with a sleek Matrix-inspired interface that leverages multiple Large Language Models (LLMs) to provide comprehensive code reviews, identify issues, and suggest improvements.

![AI Code Analyzer](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36.0-red.svg)
![Deployment](https://img.shields.io/badge/Deployment-Render-green.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

* **🤖 Multi-Model Analysis**: Compare insights from OpenAI GPT-4, Anthropic Claude, DeepSeek, and fine-tuned models
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

[🚀 Try it live on Render](https://ai-code-analyzer-tcl8.onrender.com)

## 🛠️ Tech Stack

- **Frontend**: Streamlit with custom Matrix-inspired CSS
- **LLM Integration**: OpenAI, Anthropic, DeepSeek APIs
- **Fine-tuning**: LoRA/QLoRA with Hugging Face Transformers
- **Model Hosting**: Hugging Face Hub & Spaces
- **Language**: Python 3.11+
- **Deployment**: Render (configured with render.yaml)
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
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
GITHUB_TOKEN=your_github_token_here  # Optional, for higher API limits
```

5. **Run the application:**
```bash
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

```
ai-code-analyzer/
├── matrix_final.py        # Main Streamlit application (deployed version)
├── analyzer/              # Core analysis engine
│   ├── __init__.py       # Package initialization
│   ├── code_analyzer.py  # Main analysis engine
│   ├── llm_clients.py    # LLM API client implementations
│   ├── prompts.py        # Analysis prompt templates
│   └── utils.py          # Utility functions
├── requirements.txt       # Python dependencies
├── render.yaml           # Render deployment configuration
├── Procfile             # Alternative deployment configuration
├── runtime.txt          # Python version specification
├── README.md            # This file
└── .env                 # Environment variables (create this)
```

## 🔧 Configuration

### Supported LLM Providers

| Provider  | Model          | API Key Environment Variable |
| --------- | -------------- | ---------------------------- |
| OpenAI    | GPT-4o-mini    | OPENAI\_API\_KEY             |
| Anthropic | Claude 3 Haiku | ANTHROPIC\_API\_KEY          |
| DeepSeek  | DeepSeek Chat  | DEEPSEEK\_API\_KEY           |

### Supported Programming Languages

- Python, JavaScript, Java, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin
- **Auto-detection** available for most languages
- **Manual selection** option for specific analysis

## 🚀 Deployment

### Deploy to Render (Recommended)

The project is configured for **one-click deployment** on Render:

1. **Fork this repository** to your GitHub account
2. **Connect to Render**: Go to [Render Dashboard](https://dashboard.render.com)
3. **Create New Web Service**: Select "Build and deploy from a Git repository"
4. **Connect Repository**: Link your forked repository
5. **Configure Environment Variables** in Render dashboard:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY` 
   - `DEEPSEEK_API_KEY`
   - `GITHUB_TOKEN` (optional)
6. **Deploy**: Render automatically detects `render.yaml` and deploys

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
# Start the development server
python -m streamlit run matrix_final.py --server.port 8501

# With auto-reload for development
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

- **Live Demo**: [ai-code-analyzer-tcl8.onrender.com](https://ai-code-analyzer-tcl8.onrender.com)
- **Repository**: [github.com/arun3676/ai-code-analyzer](https://github.com/arun3676/ai-code-analyzer)
- **Render Dashboard**: [dashboard.render.com](https://dashboard.render.com)

---

**Built with ❤️ by [Arun](https://github.com/arun3676)**