# API Setup Guide

## Setting up DeepSeek API Key

1. **Get your DeepSeek API Key**:
   - Go to [DeepSeek Console](https://platform.deepseek.com/)
   - Sign up or log in
   - Navigate to API Keys section
   - Create a new API key

2. **Add the key to your environment**:
   - Create a `.env` file in your project root
   - Add: `DEEPSEEK_API_KEY=your_actual_api_key_here`
   - **Important**: Use your real API key, not placeholder text like `****`

3. **Other supported APIs**:
   ```
   OPENAI_API_KEY=your_openai_key_here
   ANTHROPIC_API_KEY=your_claude_key_here
   GEMINI_API_KEY=your_gemini_key_here
   ```

## Common Issues & Solutions

### DeepSeek Authentication Error (401)
- **Problem**: Error message "Authentication Fails, Your api key: ****here is invalid"
- **Solution**: 
  1. Double-check your API key is correct
  2. Make sure there are no extra spaces or quotes
  3. Verify the key is active in DeepSeek console
  4. Try regenerating the API key

### Button Not Clickable
- **Fixed**: The "Analyze Code" button is now always clickable
- **Usage**: Just paste your code and click "Analyze Code"
- No need to wait for any delays

## Running the Application

```bash
python -m streamlit run matrix_final.py --server.port 8500
```

Access at: http://localhost:8500 