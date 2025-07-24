import streamlit as st
import os
import time
from dotenv import load_dotenv
from analyzer import CodeAnalyzer
import json

# Load environment variables - only in development
if os.path.exists('.env'):
    load_dotenv()

# Simple health check for Render
def is_health_check():
    """Check if this is a health check request"""
    try:
        # Check URL parameters
        if "health" in st.query_params or "healthz" in st.query_params:
            return True
        return False
    except:
        return False

# Handle health check
if is_health_check():
    st.json({
        "status": "healthy", 
        "service": "ai-code-analyzer",
        "timestamp": time.time(),
        "uptime": "ok"
    })
    st.stop()

# Page config
st.set_page_config(
    page_title="LLM Code Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main { padding-top: 2rem; }
    .stButton > button {
        width: 100%;
        background-color: #0e1117;
        border: 1px solid #262730;
        font-weight: 500;
    }
    .stButton > button:hover {
        border-color: #4a4b5e;
    }
    .code-editor {
        font-family: 'Monaco', 'Menlo', monospace;
    }
    .metric-card {
        background-color: #1e1e1e;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #262730;
    }
    .analysis-section {
        background-color: #1e1e1e;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 1px solid #262730;
    }
    .quality-score {
        font-size: 2rem;
        font-weight: bold;
    }
    .model-badge {
        background-color: #262730;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        display: inline-block;
        margin: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize analyzer with better error handling
@st.cache_resource
def get_analyzer():
    try:
        return CodeAnalyzer()
    except Exception as e:
        st.error(f"Failed to initialize analyzer: {str(e)}")
        st.info("Please ensure your API keys are properly configured in the environment variables.")
        return None

analyzer = get_analyzer()

# Check if analyzer is available
if analyzer is None:
    st.error("⚠️ Code Analyzer is not available. Please check your API key configuration.")
    st.info("""
    **Required Environment Variables:**
    - `OPENAI_API_KEY` - For OpenAI GPT-4 analysis
    - `ANTHROPIC_API_KEY` - For Claude analysis  
    - `GEMINI_API_KEY` - For Google Gemini analysis
    - `DEEPSEEK_API_KEY` - For DeepSeek analysis
    
    At least one API key is required for the application to work.
    """)
    st.stop()

def display_analysis_result(result: dict, model_name: str):
    """Display analysis result in a formatted way."""
    if 'error' in result:
        st.error(f"Analysis failed: {result['error']}")
        return
    
    # Quality score with color
    score = result['quality_score']
    score_color = "#00ff00" if score >= 80 else "#ffaa00" if score >= 60 else "#ff4444"
    
    st.markdown(f"""
    <div class="analysis-section">
        <h3>{model_name}</h3>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span class="quality-score" style="color: {score_color};">{score}/100</span>
                <p style="margin: 0; color: #888;">Quality Score</p>
            </div>
            <div style="text-align: right;">
                <p style="margin: 0;"><strong>Language:</strong> {result['language']}</p>
                <p style="margin: 0;"><strong>Analysis Time:</strong> {result['execution_time']}s</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary
    if result.get('summary'):
        st.markdown("#### 📋 Summary")
        st.info(result['summary'])
    
    # Create columns for different sections
    col1, col2 = st.columns(2)
    
    with col1:
        # Strengths
        if result.get('strengths'):
            st.markdown("#### ✅ Strengths")
            for strength in result['strengths']:
                st.success(f"• {strength}")
        
        # Suggestions
        if result.get('suggestions'):
            st.markdown("#### 💡 Suggestions")
            for suggestion in result['suggestions']:
                st.info(f"• {suggestion}")
    
    with col2:
        # Issues
        if result.get('issues'):
            st.markdown("#### ⚠️ Issues")
            for issue in result['issues']:
                st.warning(f"• {issue}")
        
        # Security concerns
        if result.get('security_concerns'):
            st.markdown("#### 🔒 Security")
            for concern in result['security_concerns']:
                st.error(f"• {concern}")
    
    # Performance notes
    if result.get('performance_notes'):
        st.markdown("#### ⚡ Performance")
        for note in result['performance_notes']:
            st.info(f"• {note}")
    
    # Expandable raw response
    with st.expander("View Raw Response"):
        st.code(result.get('raw_response', 'No raw response available'))

# Header
st.title("🔍 Professional Code Analyzer")
st.markdown("Analyze your code with multiple state-of-the-art LLMs")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Model status
    st.subheader("Available Models")
    available_models = analyzer.available_models
    
    if not available_models:
        st.error("No models available. Please check your API keys in .env file")
        st.stop()
    
    for model, display_name in available_models.items():
        st.success(f"✅ {display_name}")
    
    st.divider()
    
    # Analysis options
    st.subheader("Analysis Options")
    selected_model = st.selectbox(
        "Select Model",
        options=list(available_models.keys()),
        format_func=lambda x: available_models[x]
    )
    
    analyze_all = st.checkbox("Compare All Models", value=False)
    
    # Language selection
    languages = ["auto-detect", "python", "javascript", "java", "cpp", "csharp", "go", "rust"]
    selected_language = st.selectbox("Language", languages)
    
    st.divider()
    
    # Sample code
    st.subheader("Sample Code")
    if st.button("Load Python Example"):
        st.session_state.code_input = """def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Calculate fibonacci numbers
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
"""
    
    if st.button("Load JavaScript Example"):
        st.session_state.code_input = """function findDuplicates(arr) {
    let duplicates = [];
    for (let i = 0; i < arr.length; i++) {
        for (let j = i + 1; j < arr.length; j++) {
            if (arr[i] === arr[j]) {
                duplicates.push(arr[i]);
            }
        }
    }
    return duplicates;
}

console.log(findDuplicates([1, 2, 3, 2, 4, 3, 5]));
"""

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Code Input")
    code_input = st.text_area(
        "Paste your code here",
        value=st.session_state.get('code_input', ''),
        height=400,
        key="code_input",
        help="Paste the code you want to analyze"
    )
    
    # Analysis button
    analyze_button = st.button(
        "🚀 Analyze Code",
        type="primary",
        disabled=not code_input.strip()
    )

# Results column
with col2:
    st.subheader("📊 Analysis Results")
    
    if analyze_button and code_input.strip():
        with st.spinner("Analyzing code..."):
            if analyze_all:
                # Multi-model analysis
                results = analyzer.analyze_with_all_models(
                    code_input,
                    selected_language if selected_language != "auto-detect" else None
                )
                
                # Display comparison
                comparison = analyzer.compare_analyses(results)
                
                # Metrics row
                metrics_cols = st.columns(4)
                with metrics_cols[0]:
                    st.metric("Average Score", f"{comparison['average_score']}/100")
                with metrics_cols[1]:
                    st.metric("Models Used", len(results))
                with metrics_cols[2]:
                    st.metric("Best Score", f"{max(comparison['model_scores'].values())}/100")
                with metrics_cols[3]:
                    st.metric("Analysis Time", f"{comparison['analysis_time']:.1f}s")
                
                # Tabs for each model
                tabs = st.tabs(list(available_models.values()))
                for idx, (model_key, result) in enumerate(results.items()):
                    with tabs[idx]:
                        display_analysis_result(result, available_models[model_key])
                
                # Consensus findings
                if comparison['consensus_issues']:
                    st.markdown("### 🤝 Consensus Issues")
                    for issue in comparison['consensus_issues']:
                        st.warning(f"• {issue}")
                
            else:
                # Single model analysis
                result = analyzer.analyze_code(
                    code_input,
                    selected_model,
                    selected_language if selected_language != "auto-detect" else None
                )
                display_analysis_result(result, available_models[selected_model])

# Instructions for empty state
if not code_input.strip() and not analyze_button:
    st.info("""
    👋 **Welcome to the Professional Code Analyzer!**
    
    To get started:
    1. Paste your code in the left panel
    2. Select a model or choose "Compare All Models"
    3. Click "Analyze Code" to get comprehensive insights
    
    You can also load sample code from the sidebar to try it out!
    """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #888; padding: 2rem;">
    <p>Built with Streamlit • Powered by OpenAI, Anthropic, Google, and DeepSeek</p>
    <p>Professional Code Analysis Tool</p>
</div>
""", unsafe_allow_html=True) 