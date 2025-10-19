# MCP Tools Setup Guide for AI Code Analyzer Project

## 🎯 Configured MCP Tools

I've set up the following MCP tools in your `~/.cursor/mcp.json` file:

### **Essential for ML/AI Projects:**

1. **🤗 Hugging Face** - Model management and dataset access
   - **API Key Location**: https://huggingface.co/settings/tokens
   - **Required Scope**: `read` (minimum), `write` (if you want to upload models)
   - **Replace**: `YOUR_HUGGINGFACE_API_KEY_HERE`

2. **🗄️ DuckDB** - Local analytics database (no API key needed)
   - **Perfect for**: Analyzing your `analyst_dataset.jsonl` file
   - **No setup required** - ready to use!

### **Development & Deployment:**

3. **🐙 GitHub** - Version control and collaboration
   - **API Key Location**: https://github.com/settings/tokens
   - **Required Scope**: `repo`, `workflow`, `read:org`
   - **Replace**: `YOUR_GITHUB_TOKEN_HERE`

4. **🚀 Vercel** - Deploy web interfaces
   - **API Key Location**: https://vercel.com/account/tokens
   - **Replace**: `YOUR_VERCEL_TOKEN_HERE`

5. **🚂 Railway** - Full-stack deployment
   - **API Key Location**: https://railway.app/account/tokens
   - **Replace**: `YOUR_RAILWAY_TOKEN_HERE`

### **Data Storage:**

6. **🍃 MongoDB** - Database for structured data
   - **Connection String**: Get from MongoDB Atlas (https://cloud.mongodb.com/)
   - **Format**: `mongodb+srv://username:password@cluster.mongodb.net/database`
   - **Replace**: `YOUR_MONGODB_CONNECTION_STRING_HERE`

### **Monitoring & Error Tracking:**

7. **🚨 Sentry** - Error tracking and performance monitoring
   - **Auth Token**: https://sentry.io/settings/account/api/auth-tokens/
   - **Organization**: Your Sentry org slug
   - **Project**: Your project slug
   - **Replace**: 
     - `YOUR_SENTRY_AUTH_TOKEN_HERE`
     - `YOUR_SENTRY_ORG_HERE`
     - `YOUR_SENTRY_PROJECT_HERE`

### **Security & Code Quality:**

8. **🔒 Snyk** - Vulnerability scanning
   - **API Key Location**: https://app.snyk.io/account
   - **Replace**: `YOUR_SNYK_TOKEN_HERE`

9. **🔍 Semgrep** - Static analysis (no API key needed)
   - **Ready to use** - no setup required!

10. **🏗️ SonarQube** - Code analysis
    - **Setup**: You need a SonarQube instance (cloud or self-hosted)
    - **Token**: Generate in your SonarQube instance
    - **Replace**: 
      - `YOUR_SONARQUBE_URL_HERE` (e.g., `https://your-org.sonarcloud.io`)
      - `YOUR_SONARQUBE_TOKEN_HERE`

## 🚀 Quick Start (Recommended Order)

### **Phase 1: Essential Tools (Start Here)**
1. **Hugging Face** - Most important for your ML project
2. **DuckDB** - Already ready, no API key needed
3. **GitHub** - For version control

### **Phase 2: Development Tools**
4. **Vercel** or **Railway** - For deployment
5. **Sentry** - For monitoring

### **Phase 3: Advanced Tools (Optional)**
6. **MongoDB** - If you need structured data storage
7. **Snyk** - For security scanning
8. **Semgrep** - For static analysis
9. **SonarQube** - For comprehensive code analysis

## 📝 How to Add API Keys

1. **Open your MCP config**: `c:\Users\arunk\.cursor\mcp.json`
2. **Find the placeholder** (e.g., `YOUR_HUGGINGFACE_API_KEY_HERE`)
3. **Replace with your actual API key/token**
4. **Save the file**
5. **Restart Cursor** for changes to take effect

## 🔧 Installation Commands

Run these commands to ensure all MCP servers are installed:

```powershell
# Install all MCP servers
npm install -g @modelcontextprotocol/server-huggingface
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-duckdb
npm install -g @modelcontextprotocol/server-sentry
npm install -g @modelcontextprotocol/server-vercel
npm install -g @modelcontextprotocol/server-mongodb
npm install -g @modelcontextprotocol/server-railway
npm install -g @modelcontextprotocol/server-snyk
npm install -g @modelcontextprotocol/server-semgrep
npm install -g @modelcontextprotocol/server-sonarqube
```

## ✅ Testing Your Setup

After adding API keys, test each tool in Cursor Composer:

- **Hugging Face**: "Search for code analysis models on Hugging Face"
- **DuckDB**: "Analyze my training dataset using DuckDB"
- **GitHub**: "Show me my recent commits"
- **Sentry**: "Check for errors in my project"

## 🛡️ Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive data
- Regularly rotate your API keys
- Use minimal required permissions for each service

## 🆘 Troubleshooting

If a tool doesn't work:
1. Check if the MCP server is installed: `npm list -g @modelcontextprotocol/server-*`
2. Verify API keys are correct and have proper permissions
3. Restart Cursor after making changes
4. Check Cursor's MCP settings in `Settings > Features > MCP`

## 📚 Useful Commands for Your Project

Once set up, you can use these commands in Cursor Composer:

- "Use Hugging Face to find the best code analysis models"
- "Analyze my analyst_dataset.jsonl with DuckDB"
- "Check my code for vulnerabilities with Snyk"
- "Deploy my analyzer to Vercel"
- "Monitor errors with Sentry"
