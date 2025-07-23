import streamlit as st
import os
import time
import random
import sys
from dotenv import load_dotenv
from analyzer import CodeAnalyzer

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Matrix Code Analyzer - Final",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Matrix CSS - Enhanced with file upload styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono:wght@400&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    /* Matrix Background */
    .stApp {
        background: linear-gradient(135deg, #0d1b0d 0%, #000000 50%, #0d1b0d 100%);
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
    }
    
    /* Matrix Code Rain Animation */
    .matrix-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: -1;
        opacity: 0.1;
    }
    
    .matrix-char {
        position: absolute;
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
        font-size: 14px;
        animation: matrix-fall linear infinite;
    }
    
    @keyframes matrix-fall {
        0% { transform: translateY(-100vh); opacity: 1; }
        100% { transform: translateY(100vh); opacity: 0; }
    }
    
    /* Main Content Styling */
    .main .block-container {
        padding-top: 2rem;
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid #00ff41;
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
    }
    
    /* Title Styling */
    h1 {
        font-family: 'Orbitron', monospace !important;
        color: #00ff41 !important;
        text-align: center !important;
        text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 30px #00ff41;
        font-weight: 900 !important;
        margin-bottom: 2rem !important;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 5px #00ff41, 0 0 10px #00ff41, 0 0 15px #00ff41; }
        to { text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 30px #00ff41; }
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: rgba(0, 0, 0, 0.9) !important;
        border: 1px solid #00ff41 !important;
        border-radius: 10px !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #003300, #006600) !important;
        color: #00ff41 !important;
        border: 2px solid #00ff41 !important;
        border-radius: 5px !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #006600, #00aa00) !important;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: rgba(0, 51, 0, 0.3) !important;
        border: 2px dashed #00ff41 !important;
        border-radius: 10px !important;
        padding: 20px !important;
    }
    
    .stFileUploader label {
        color: #00ff41 !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: bold !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: rgba(0, 51, 0, 0.8) !important;
        border: 1px solid #00ff41 !important;
        color: #00ff41 !important;
    }
    
    /* Text areas */
    .stTextArea > div > div > textarea {
        background: rgba(0, 0, 0, 0.9) !important;
        border: 1px solid #00ff41 !important;
        color: #00ff41 !important;
        font-family: 'Share Tech Mono', monospace !important;
    }
    
    /* Metrics */
    .css-1xarl3l {
        background: rgba(0, 51, 0, 0.3) !important;
        border: 1px solid #00ff41 !important;
        border-radius: 5px !important;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.2) !important;
    }
    
    /* Success/Info/Warning messages */
    .stSuccess {
        background: rgba(0, 255, 65, 0.1) !important;
        border: 1px solid #00ff41 !important;
        color: #00ff41 !important;
    }
    
    .stInfo {
        background: rgba(0, 255, 255, 0.1) !important;
        border: 1px solid #00ffff !important;
        color: #00ffff !important;
    }
    
    .stWarning {
        background: rgba(255, 255, 0, 0.1) !important;
        border: 1px solid #ffff00 !important;
        color: #ffff00 !important;
    }
    
    .stError {
        background: rgba(255, 0, 0, 0.1) !important;
        border: 1px solid #ff0000 !important;
        color: #ff0000 !important;
    }
    
    /* Code blocks */
    .stCode {
        background: rgba(0, 0, 0, 0.9) !important;
        border: 1px solid #00ff41 !important;
        color: #00ff41 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(0, 0, 0, 0.8) !important;
        border-bottom: 2px solid #00ff41 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(0, 51, 0, 0.3) !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        font-family: 'Orbitron', monospace !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(0, 255, 65, 0.2) !important;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.5) !important;
    }
    
    /* Matrix Terminal Effect */
    .matrix-terminal {
        background: rgba(0, 0, 0, 0.95) !important;
        border: 2px solid #00ff41 !important;
        border-radius: 10px !important;
        padding: 20px !important;
        font-family: 'Share Tech Mono', monospace !important;
        color: #00ff41 !important;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.4) !important;
        position: relative !important;
    }
    
    .matrix-terminal::before {
        content: "MATRIX_ANALYZER_v3.0 > OPERATIONAL" !important;
        position: absolute !important;
        top: -15px !important;
        left: 20px !important;
        background: #000000 !important;
        padding: 0 10px !important;
        color: #00ff41 !important;
        font-size: 12px !important;
        font-weight: bold !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        color: #00ff41 !important;
        font-family: 'Orbitron', monospace !important;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #00ff41 transparent #00ff41 transparent !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(0, 51, 0, 0.3) !important;
        border: 1px solid #00ff41 !important;
        color: #00ff41 !important;
    }
    
    /* File info styling */
    .file-info {
        background: rgba(0, 255, 65, 0.1);
        border: 1px solid #00ff41;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        font-family: 'Share Tech Mono', monospace;
    }
</style>

<div class="matrix-bg" id="matrix-bg"></div>

<script>
function createMatrixRain() {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()_+-=[]{}|;:,.<>?";
    const container = document.getElementById('matrix-bg');
    
    for (let i = 0; i < 50; i++) {
        const char = document.createElement('div');
        char.className = 'matrix-char';
        char.textContent = chars[Math.floor(Math.random() * chars.length)];
        char.style.left = Math.random() * 100 + '%';
        char.style.animationDuration = (Math.random() * 3 + 2) + 's';
        char.style.animationDelay = Math.random() * 2 + 's';
        container.appendChild(char);
    }
}

// Create matrix rain effect
setTimeout(createMatrixRain, 100);
</script>
""", unsafe_allow_html=True)

# Initialize analyzer
def get_analyzer():
    # Force reimport to ensure latest code
    import importlib
    import analyzer.code_analyzer
    importlib.reload(analyzer.code_analyzer)
    from analyzer.code_analyzer import CodeAnalyzer
    return CodeAnalyzer()

analyzer = get_analyzer()

def display_matrix_analysis_result(result: dict, model_name: str):
    """Display analysis result in clean, readable horizontal blocks."""
    if 'error' in result:
        st.error(f"🚨 SYSTEM ERROR: {result['error']}")
        return
    
    # Quality score with modern styling
    score = result['quality_score']
    if score >= 80:
        score_color = "#00ff41"
        status = "EXCELLENT"
    elif score >= 60:
        score_color = "#ffff00"
        status = "ACCEPTABLE"
    else:
        score_color = "#ff0000"
        status = "NEEDS_WORK"
    
    # Header with score
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(0,255,65,0.15), rgba(0,255,65,0.05)); 
               border: 2px solid #00ff41; border-radius: 15px; padding: 25px; margin: 20px 0; 
               text-align: center;">
        <h2 style="color: {score_color}; margin-bottom: 15px; font-size: 1.8rem;">
            {model_name} Analysis
        </h2>
        <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; color: #ffffff;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; color: {score_color}; font-weight: bold;">{score}/100</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">{status}</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.2rem; color: #00ff41; font-weight: bold;">{result['language'].upper()}</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Language</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.2rem; color: #00ff41; font-weight: bold;">{result['line_count']}</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Lines</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary
    if result.get('summary'):
        st.markdown("### 📋 Code Overview")
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.6); border: 1px solid #00ff41; border-radius: 10px; 
                   padding: 20px; margin: 20px 0;">
            <p style="color: #ffffff; font-size: 18px; line-height: 1.6; text-align: center; margin: 0;">
                {result['summary']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Analysis results in horizontal blocks
    st.markdown("### 📊 Analysis Results")
    
    # Bug Detection Block (Full width)
    bug_items = result.get('bugs', [])
    if bug_items:
        bug_text = " • ".join(bug_items[:3])  # Join with bullets for horizontal reading
    else:
        bug_text = "No critical bugs detected • Code logic appears sound • Edge cases handled well"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(255,100,100,0.1), rgba(150,0,0,0.1)); 
               border: 2px solid #ff6b6b; border-radius: 15px; padding: 25px; margin: 15px 0;">
        <h3 style="color: #ff6b6b; margin-bottom: 15px; text-align: center; font-size: 1.4rem;">
            🐛 Bug Detection
        </h3>
        <p style="color: #ffffff; font-size: 16px; line-height: 1.6; text-align: center; margin: 0;">
            {bug_text}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Security Vulnerabilities Block (Full width)
    security_items = result.get('security_vulnerabilities', [])
    if security_items:
        security_text = " • ".join(security_items[:3])  # Join with bullets for horizontal reading
    else:
        security_text = "No security vulnerabilities found • Follows security best practices • Input validation looks good"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(200,0,200,0.1), rgba(100,0,100,0.1)); 
               border: 2px solid #ff00ff; border-radius: 15px; padding: 25px; margin: 15px 0;">
        <h3 style="color: #ff00ff; margin-bottom: 15px; text-align: center; font-size: 1.4rem;">
            🔒 Security Check
        </h3>
        <p style="color: #ffffff; font-size: 16px; line-height: 1.6; text-align: center; margin: 0;">
            {security_text}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Code Quality & Quick Fixes Block (Full width)
    quality_items = result.get('quality_issues', []) + result.get('quick_fixes', [])
    if quality_items:
        quality_text = " • ".join(quality_items[:3])  # Join with bullets for horizontal reading
    else:
        quality_text = "Code is well-structured • Good naming conventions • Easy to read and maintain"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(0,200,255,0.1), rgba(0,100,150,0.1)); 
               border: 2px solid #00ccff; border-radius: 15px; padding: 25px; margin: 15px 0;">
        <h3 style="color: #00ccff; margin-bottom: 15px; text-align: center; font-size: 1.4rem;">
            📝 Code Quality
        </h3>
        <p style="color: #ffffff; font-size: 16px; line-height: 1.6; text-align: center; margin: 0;">
            {quality_text}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Legacy sections (only if new sections are empty)
    if not result.get('bugs') and not result.get('security_vulnerabilities') and not result.get('quality_issues'):
        legacy_col1, legacy_col2 = st.columns(2)
        
        with legacy_col1:
            # Legacy strengths
            if result.get('strengths'):
                st.markdown("#### ✅ Strengths")
                for strength in result['strengths'][:3]:
                    st.success(f"✓ {strength}")
            
            # Legacy issues
        if result.get('issues'):
                st.markdown("#### ⚠️ Issues")
                for issue in result['issues'][:3]:
                    st.warning(f"! {issue}")
        
        with legacy_col2:
            # Legacy suggestions
            if result.get('suggestions'):
                st.markdown("#### 💡 Suggestions")
                for suggestion in result['suggestions'][:3]:
                    st.info(f"→ {suggestion}")
            
            # Legacy security concerns
        if result.get('security_concerns'):
                st.markdown("#### 🔒 Security Concerns")
                for concern in result['security_concerns'][:3]:
                    st.error(f"⚠ {concern}")
    
    # Expandable raw response (moved to bottom and less prominent)
    with st.expander("🔍 View Detailed Analysis", expanded=False):
        st.code(result.get('raw_response', 'NO_DATA_AVAILABLE'), language='text')

def display_github_analysis_result(result: dict, model_name: str):
    """Display GitHub repository analysis result in clean, readable horizontal blocks."""
    if 'error' in result:
        st.error(f"🚨 GITHUB ANALYSIS ERROR: {result['error']}")
        return
    
    # Repository info in a clean header
    if result.get('repository_info'):
        repo_info = result['repository_info']
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(0,255,65,0.15), rgba(0,255,65,0.05)); 
                   border: 2px solid #00ff41; border-radius: 15px; padding: 25px; margin: 20px 0; 
                   text-align: center;">
            <h2 style="color: #00ff41; margin-bottom: 20px; font-size: 1.8rem;">
                📦 {repo_info['name']}
            </h2>
            <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; color: #ffffff;">
                <div style="text-align: center;">
                    <div style="font-size: 1.5rem; color: #00ff41; font-weight: bold;">{repo_info['language']}</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">Language</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.5rem; color: #00ff41; font-weight: bold;">⭐ {repo_info['stars']}</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">Stars</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.5rem; color: #00ff41; font-weight: bold;">🔀 {repo_info['forks']}</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">Forks</div>
                </div>
            </div>
            <p style="color: #ffffff; margin-top: 15px; font-style: italic;">
                "{repo_info['description']}"
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Analysis results in horizontal blocks
    st.markdown("### 📊 Analysis Results")
    
    # Architecture Quality Block (Full width)
    arch_items = result.get('architecture_quality', [])
    if arch_items:
        arch_text = " • ".join(arch_items[:3])  # Join with bullets for horizontal reading
    else:
        arch_text = "Well-structured repository • Good organization • Follows best practices"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(0,255,65,0.1), rgba(0,100,30,0.1)); 
               border: 2px solid #00ff41; border-radius: 15px; padding: 25px; margin: 15px 0;">
        <h3 style="color: #00ff41; margin-bottom: 15px; text-align: center; font-size: 1.4rem;">
            🏗️ Code Architecture
        </h3>
        <p style="color: #ffffff; font-size: 16px; line-height: 1.6; text-align: center; margin: 0;">
            {arch_text}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Critical Issues Block (Full width)
    critical_items = result.get('critical_issues', [])
    if critical_items:
        critical_text = " • ".join(critical_items[:3])  # Join with bullets for horizontal reading
    else:
        critical_text = "No major security vulnerabilities found • Code appears well-maintained • No critical bugs detected"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(255,100,100,0.1), rgba(150,0,0,0.1)); 
               border: 2px solid #ff6b6b; border-radius: 15px; padding: 25px; margin: 15px 0;">
        <h3 style="color: #ff6b6b; margin-bottom: 15px; text-align: center; font-size: 1.4rem;">
            🚨 Critical Issues
        </h3>
        <p style="color: #ffffff; font-size: 16px; line-height: 1.6; text-align: center; margin: 0;">
            {critical_text}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Improvement Priorities Block (Full width)
    improvement_items = result.get('improvement_priorities', [])
    if improvement_items:
        improvement_text = " • ".join(improvement_items[:3])  # Join with bullets for horizontal reading
    else:
        improvement_text = "Add more comprehensive documentation • Consider adding automated tests • Enhance error handling"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(255,200,0,0.1), rgba(150,100,0,0.1)); 
               border: 2px solid #ffd700; border-radius: 15px; padding: 25px; margin: 15px 0;">
        <h3 style="color: #ffd700; margin-bottom: 15px; text-align: center; font-size: 1.4rem;">
            🎯 Priority Improvements
        </h3>
        <p style="color: #ffffff; font-size: 16px; line-height: 1.6; text-align: center; margin: 0;">
            {improvement_text}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary section at the bottom (if available)
    if result.get('project_overview'):
        st.markdown("### 💡 Key Insights")
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.6); border: 1px solid #00ff41; border-radius: 10px; 
                   padding: 20px; margin: 20px 0;">
            <p style="color: #ffffff; font-size: 18px; line-height: 1.6; text-align: center; margin: 0;">
                {result['project_overview']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Expandable raw response (moved to bottom and less prominent)
    with st.expander("🔍 View Detailed Analysis", expanded=False):
        st.code(result.get('raw_response', 'NO_DATA_AVAILABLE'), language='text')

# Header with Matrix effect
st.markdown("""
<h1 style="text-align: center;">
🤖 AI Code Analyzer
</h1>
<div style="text-align: center; margin-bottom: 30px;">
    <p style="color: #00ff41; font-family: 'Orbitron', monospace; font-size: 20px; margin-bottom: 10px;">
        <strong>Powered by Advanced AI Models</strong>
    </p>
    <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
        <span style="background: rgba(0,255,65,0.2); border: 1px solid #00ff41; padding: 8px 16px; 
                    border-radius: 25px; font-size: 14px; color: #00ff41;">
            ✨ Bug Detection
        </span>
        <span style="background: rgba(0,255,65,0.2); border: 1px solid #00ff41; padding: 8px 16px; 
                    border-radius: 25px; font-size: 14px; color: #00ff41;">
            🔒 Security Analysis
        </span>
        <span style="background: rgba(0,255,65,0.2); border: 1px solid #00ff41; padding: 8px 16px; 
                    border-radius: 25px; font-size: 14px; color: #00ff41;">
            📦 GitHub Integration
        </span>
        <span style="background: rgba(0,255,65,0.2); border: 1px solid #00ff41; padding: 8px 16px; 
                    border-radius: 25px; font-size: 14px; color: #00ff41;">
            ⚡ Instant Results
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar - The Matrix Control Panel
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    
    # Model status
    st.markdown("#### Available AI Models")
    available_models = analyzer.available_models
    
    if not available_models:
        st.error("❌ No AI models detected")
        st.info("Please configure API keys in .env file")
        st.stop()
    
    # Display available models with modern styling
    for model, display_name in available_models.items():
        st.markdown(f"""
        <div style="background: rgba(0, 255, 65, 0.1); border: 1px solid #00ff41; padding: 10px; margin: 8px 0; border-radius: 8px;">
        ✅ <strong>{display_name}</strong> <span style="color: #00ff41; font-size: 12px;">[Ready]</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Analysis Mode Selection
    st.markdown("#### Analysis Mode")
    analysis_mode = st.radio(
        "Choose what to analyze",
        ["Code Analysis", "GitHub Repository"],
        format_func=lambda x: f"📝 {x}" if x == "Code Analysis" else f"📦 {x}"
    )
    
    if analysis_mode == "GitHub Repository":
        st.markdown("#### Repository Analysis")
        github_url = st.text_input(
            "GitHub URL",
            placeholder="https://github.com/owner/repo",
            help="Enter a GitHub repository URL for analysis"
        )
        
        analyze_github_button = st.button(
            "🔍 Analyze Repository",
            type="primary",
            help="Analyze GitHub repository structure and code"
        )
    
    st.markdown("---")
    
    # Analysis options
    st.markdown("#### Analysis Settings")
    
    # Model selector with modern styling
    selected_model = st.selectbox(
        "Choose AI Model",
        options=list(available_models.keys()),
        format_func=lambda x: f"🤖 {available_models[x]}"
    )
    
    # Multi-model analysis toggle
    analyze_all = st.checkbox("🔄 Compare Multiple Models", value=False)
    
    # Language selection
    languages = ["auto-detect", "python", "javascript", "java", "cpp", "csharp", "go", "rust", "php", "ruby", "swift", "kotlin"]
    selected_language = st.selectbox(
        "Programming Language", 
        languages,
        format_func=lambda x: "🔍 Auto-Detect" if x == "auto-detect" else f"💻 {x.upper()}"
    )
    
    st.markdown("---")
    
    # Sample code injection
    st.markdown("#### Quick Start Examples")
    
    if st.button("🐍 Try Python Example"):
        st.session_state.code_input = """def calculate_total(items):
    total = 0
    for item in items:
        total += item.price  # Potential AttributeError
    return total

# Missing validation
items = None
result = calculate_total(items)  # This will crash
print(f"Total: {result}")
"""
    
    if st.button("🌐 Try JavaScript Example"):
        st.session_state.code_input = """function processUser(user) {
    // Security issue: no input validation
    document.innerHTML = user.name;  // XSS vulnerability
    
    // Logic error: undefined check
    if (user.age > 18) {
        return user.permissions.admin;  // Potential TypeError
    }
    
    return false;
}

// Missing error handling
const userData = getUser();  // Could be undefined
processUser(userData);
"""

# Main Terminal Interface
col1, col2 = st.columns([1, 1])

with col1:
    if analysis_mode == "Code Analysis":
        st.markdown("### 📝 Code Input")
    
    # File upload section
        st.markdown("#### 📁 Upload File")
    uploaded_file = st.file_uploader(
            "Choose a code file",
        type=['py', 'js', 'java', 'cpp', 'c', 'cs', 'go', 'rs', 'php', 'rb', 'swift', 'kt', 'txt'],
            help="Upload code files for AI analysis"
    )
    
    code_from_file = ""
    if uploaded_file is not None:
        # Read file content
        try:
            code_from_file = str(uploaded_file.read(), "utf-8")
            file_size = len(code_from_file)
            file_lines = len(code_from_file.splitlines())
            
            st.markdown(f"""
            <div class="file-info">
                ✅ <strong>File Uploaded Successfully</strong><br>
                📄 <strong>Name:</strong> {uploaded_file.name}<br>
                📏 <strong>Size:</strong> {file_size} bytes<br>
                📊 <strong>Lines:</strong> {file_lines}<br>
                🔍 <strong>Status:</strong> Ready for analysis
            </div>
            """, unsafe_allow_html=True)
            
            # Auto-populate the text area
            st.session_state.code_input = code_from_file
            
        except UnicodeDecodeError:
                st.error("🚨 File encoding error: Please use UTF-8 encoded files")
        except Exception as e:
                st.error(f"🚨 File read error: {str(e)}")
    
    # Code input with modern styling
    code_input = st.text_area(
            "Or paste your code here",
        value=st.session_state.get('code_input', ''),
        height=350,
        key="code_input",
        help="Paste code directly or upload file above"
    )
    
    # Modern analyze button
    analyze_button = st.button(
        "🚀 Analyze Code",
        type="primary",
        help="Analyze your code with AI"
    )
    
    else:  # GitHub Repository mode
        st.markdown("### 📦 GitHub Analysis")
        
        if 'github_url' in locals():
            if github_url:
                st.markdown(f"""
                <div class="file-info">
                ✅ <strong>Repository Detected</strong><br>
                📦 <strong>URL:</strong> {github_url}<br>
                🔍 <strong>Status:</strong> Ready for analysis
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            #### 📋 What We'll Analyze
            
            **Repository Analysis includes:**
            - 🏗️ Project structure and organization
            - 📄 Key files (README, package.json, main source files)
            - 🎯 Code quality and architecture assessment
            - 🔒 Security vulnerabilities across the codebase
            - 💡 Best practices and improvement suggestions
            
            **Note:** Only public repositories can be analyzed.
            """)
        
        # Show sample repos
        st.markdown("#### 📚 Try These Sample Repositories")
        sample_repos = [
            "https://github.com/microsoft/vscode",
            "https://github.com/facebook/react",
            "https://github.com/python/cpython"
        ]
        
        for repo in sample_repos:
            if st.button(f"📦 {repo.split('/')[-1]}", key=repo):
                st.session_state.github_url_input = repo

# Results Terminal
with col2:
    st.markdown("### 📊 Analysis Results")
    
    # Code Analysis Results
    if analysis_mode == "Code Analysis":
        if analyze_button:
            if not code_input.strip():
                st.error("🚨 Please enter some code to analyze or upload a file!")
            else:
                with st.spinner("🟢 Analyzing your code... Please wait..."):
                    if analyze_all:
                        # Multi-model analysis
                        st.markdown("#### 🔄 MULTI_NETWORK_ANALYSIS_INITIATED")
                        
                        results = analyzer.analyze_with_all_models(
                            code_input,
                            selected_language if selected_language != "auto-detect" else None
                        )
                        
                        # Display comparison metrics
                        comparison = analyzer.compare_analyses(results)
                        
                        # Matrix-styled metrics
                        metrics_cols = st.columns(4)
                        with metrics_cols[0]:
                            st.metric("AVG_SCORE", f"{comparison['average_score']}/100")
                        with metrics_cols[1]:
                            st.metric("NETWORKS", len(results))
                        with metrics_cols[2]:
                            st.metric("PEAK_SCORE", f"{max(comparison['model_scores'].values())}/100")
                        with metrics_cols[3]:
                            st.metric("SCAN_TIME", f"{comparison['analysis_time']:.1f}s")
                        
                        # Create tabs for each neural network
                        tab_names = [f"🤖 {available_models[key]}" for key in results.keys()]
                        tabs = st.tabs(tab_names)
                        
                        for idx, (model_key, result) in enumerate(results.items()):
                            with tabs[idx]:
                                display_matrix_analysis_result(result, available_models[model_key])
                        
                        # Consensus findings with Matrix styling
                        if comparison.get('consensus_bugs') or comparison.get('consensus_security'):
                            st.markdown("### 🤝 NEURAL_CONSENSUS_DETECTED")
                            st.markdown("""
                            <div style="background: rgba(255, 0, 0, 0.1); border: 2px solid #ff0000; padding: 15px; border-radius: 10px;">
                            <strong>CRITICAL_PATTERNS_IDENTIFIED_BY_MULTIPLE_NETWORKS:</strong>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if comparison.get('consensus_bugs'):
                                st.markdown("#### 🐛 CONSENSUS_BUGS")
                                for bug in comparison['consensus_bugs']:
                                    st.error(f"🚨 MULTIPLE_MODELS: {bug}")
                            
                            if comparison.get('consensus_security'):
                                st.markdown("#### 🔒 CONSENSUS_SECURITY")
                                for vuln in comparison['consensus_security']:
                                    st.error(f"🚨 SECURITY_ALERT: {vuln}")
                
            else:
                # Single model analysis
                st.markdown(f"#### 🤖 {available_models[selected_model].upper()}_ANALYSIS")
                
                result = analyzer.analyze_code(
                    code_input,
                    selected_model,
                    selected_language if selected_language != "auto-detect" else None
                )
                display_matrix_analysis_result(result, available_models[selected_model])
    
    # GitHub Analysis Results
    else:  # GitHub Repository mode
        if 'analyze_github_button' in locals() and analyze_github_button:
            if not github_url.strip():
                st.error("🚨 Please enter a GitHub repository URL!")
            else:
                with st.spinner("🟢 Analyzing GitHub repository... Please wait..."):
                    result = analyzer.analyze_github_repo(github_url, selected_model)
                    display_github_analysis_result(result, available_models[selected_model])

# Instructions for new users
if (analysis_mode == "Code Analysis" and not code_input.strip() and not analyze_button) or \
   (analysis_mode == "GitHub Repository" and ('github_url' not in locals() or not github_url.strip()) and ('analyze_github_button' not in locals() or not analyze_github_button)):
    
    st.markdown("""
    <div class="matrix-terminal" style="margin: 20px 0; text-align: center;">
        <h2 style="color: #00ff41; margin-bottom: 30px; font-size: 2.5rem;">
            🤖 AI Code Analyzer
        </h2>
        <p style="color: #00ff41; font-size: 1.3rem; margin-bottom: 30px;">
            <strong>What can I do for you?</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards in columns
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0,255,65,0.1), rgba(0,255,65,0.05)); 
                   border: 2px solid #00ff41; border-radius: 15px; padding: 25px; margin: 10px 0; 
                   box-shadow: 0 0 20px rgba(0,255,65,0.3);">
            <h3 style="color: #00ff41; margin-bottom: 15px;">🐛 Find Bugs Instantly</h3>
            <p style="color: #ffffff; font-size: 16px; line-height: 1.6;">
                Spot crashes, logical errors, and edge cases before they hit production.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0,255,65,0.1), rgba(0,255,65,0.05)); 
                   border: 2px solid #00ff41; border-radius: 15px; padding: 25px; margin: 10px 0; 
                   box-shadow: 0 0 20px rgba(0,255,65,0.3);">
            <h3 style="color: #00ff41; margin-bottom: 15px;">🔒 Security Scanner</h3>
            <p style="color: #ffffff; font-size: 16px; line-height: 1.6;">
                Detect vulnerabilities like SQL injection, XSS, and insecure data handling.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0,255,65,0.1), rgba(0,255,65,0.05)); 
                   border: 2px solid #00ff41; border-radius: 15px; padding: 25px; margin: 10px 0; 
                   box-shadow: 0 0 20px rgba(0,255,65,0.3);">
            <h3 style="color: #00ff41; margin-bottom: 15px;">📝 Code Quality Check</h3>
            <p style="color: #ffffff; font-size: 16px; line-height: 1.6;">
                Improve readability, maintainability, and follow best practices.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0,255,65,0.1), rgba(0,255,65,0.05)); 
                   border: 2px solid #00ff41; border-radius: 15px; padding: 25px; margin: 10px 0; 
                   box-shadow: 0 0 20px rgba(0,255,65,0.3);">
            <h3 style="color: #00ff41; margin-bottom: 15px;">📦 Repository Analysis</h3>
            <p style="color: #ffffff; font-size: 16px; line-height: 1.6;">
                Analyze entire GitHub repos for structure, issues, and improvements.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # How to get started section
    st.markdown("""
    <div style="background: rgba(0,0,0,0.7); border: 1px solid #00ff41; border-radius: 10px; 
               padding: 20px; margin: 30px 0; text-align: center;">
        <h3 style="color: #00ff41; margin-bottom: 20px;">🚀 Get Started in 3 Steps</h3>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
            <div style="margin: 10px; color: #ffffff;">
                <div style="background: #00ff41; color: #000; border-radius: 50%; width: 40px; height: 40px; 
                           display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; 
                           font-weight: bold; font-size: 20px;">1</div>
                <p><strong>Upload</strong><br>Paste code or GitHub URL</p>
            </div>
            <div style="margin: 10px; color: #ffffff;">
                <div style="background: #00ff41; color: #000; border-radius: 50%; width: 40px; height: 40px; 
                           display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; 
                           font-weight: bold; font-size: 20px;">2</div>
                <p><strong>Choose AI</strong><br>Pick your preferred model</p>
            </div>
            <div style="margin: 10px; color: #ffffff;">
                <div style="background: #00ff41; color: #000; border-radius: 50%; width: 40px; height: 40px; 
                           display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; 
                           font-weight: bold; font-size: 20px;">3</div>
                <p><strong>Analyze</strong><br>Get instant results</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Supported languages as badges
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <p style="color: #00ff41; font-size: 18px; margin-bottom: 15px;"><strong>Supported Languages:</strong></p>
        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 10px;">
            <span style="background: linear-gradient(45deg, #00ff41, #00cc33); color: #000; padding: 8px 15px; 
                        border-radius: 20px; font-weight: bold; font-size: 14px;">Python</span>
            <span style="background: linear-gradient(45deg, #00ff41, #00cc33); color: #000; padding: 8px 15px; 
                        border-radius: 20px; font-weight: bold; font-size: 14px;">JavaScript</span>
            <span style="background: linear-gradient(45deg, #00ff41, #00cc33); color: #000; padding: 8px 15px; 
                        border-radius: 20px; font-weight: bold; font-size: 14px;">Java</span>
            <span style="background: linear-gradient(45deg, #00ff41, #00cc33); color: #000; padding: 8px 15px; 
                        border-radius: 20px; font-weight: bold; font-size: 14px;">C++</span>
            <span style="background: linear-gradient(45deg, #00ff41, #00cc33); color: #000; padding: 8px 15px; 
                        border-radius: 20px; font-weight: bold; font-size: 14px;">Go</span>
            <span style="background: linear-gradient(45deg, #00ff41, #00cc33); color: #000; padding: 8px 15px; 
                        border-radius: 20px; font-weight: bold; font-size: 14px;">Rust</span>
            <span style="background: linear-gradient(45deg, #00ff41, #00cc33); color: #000; padding: 8px 15px; 
                        border-radius: 20px; font-weight: bold; font-size: 14px;">+ More</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer with Matrix signature
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #00ff41; font-family: 'Share Tech Mono', monospace; padding: 20px;">
    <p>🟢 POWERED_BY_NEURAL_NETWORKS • OPENAI • ANTHROPIC • DEEPSEEK • GOOGLE 🟢</p>
    <p><em>"There is no spoon... only code to analyze."</em></p>
    <p style="font-size: 12px;">MATRIX_ANALYZER_v3.0 • BUILD_2024 • SECURITY_CLEARANCE_OMEGA • FILE_UPLOAD_ENABLED</p>
</div>
""", unsafe_allow_html=True) 