import streamlit as st
from analyzer import CodeAnalyzer

# Simple test app
st.title("🔍 LLM Code Analyzer - Test")

try:
    analyzer = CodeAnalyzer()
    available_models = analyzer.available_models
    
    st.success(f"✅ Analyzer loaded successfully!")
    st.info(f"📊 Available models: {len(available_models)}")
    
    for model_key, model_name in available_models.items():
        st.write(f"• {model_name}")
    
    # Simple code input
    code_input = st.text_area("Enter code to analyze:", 
                             value="def hello():\n    print('Hello, World!')",
                             height=150)
    
    if st.button("Analyze"):
        if code_input.strip():
            with st.spinner("Analyzing..."):
                result = analyzer.analyze_code(code_input, list(available_models.keys())[0])
                st.json(result)
        else:
            st.warning("Please enter some code")
            
except Exception as e:
    st.error(f"Error: {str(e)}")
    st.write("Debug info:")
    st.write(f"Python version: {sys.version}")
    st.write(f"Working directory: {os.getcwd()}") 