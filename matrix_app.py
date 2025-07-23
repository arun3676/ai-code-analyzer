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
    page_title="Matrix Code Analyzer",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Matrix CSS - Cyberpunk Theme
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
        content: "MATRIX_ANALYZER_v2.0 > ACTIVE" !important;
        position: absolute !important;
        top: -15px !important;
        left: 20px !important;
        background: #000000 !important;
        padding: 0 10px !important;
        color: #00ff41 !important;
        font-size: 12px !important;
        font-weight: bold !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #000000;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00ff41;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #00aa00;
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
@st.cache_resource
def get_analyzer():
    return CodeAnalyzer()

analyzer = get_analyzer()

def display_matrix_analysis_result(result: dict, model_name: str):
    """Display analysis result in Matrix terminal style."""
    if 'error' in result:
        st.error(f"🚨 SYSTEM ERROR: {result['error']}")
        return
    
    # Quality score with Matrix styling
    score = result['quality_score']
    if score >= 80:
        score_color = "#00ff41"
        status = "OPTIMAL"
    elif score >= 60:
        score_color = "#ffff00"
        status = "ACCEPTABLE"
    else:
        score_color = "#ff0000"
        status = "CRITICAL"
    
    st.markdown(f"""
    <div class="matrix-terminal">
        <h3 style="color: {score_color}; font-family: 'Orbitron', monospace; text-align: center;">
            [{model_name}] ANALYSIS COMPLETE
        </h3>
        <div style="display: flex; justify-content: space-between; margin: 20px 0;">
            <div>
                <span style="font-size: 2.5rem; color: {score_color}; font-weight: bold;">
                    {score}/100
                </span>
                <p style="margin: 0; color: {score_color}; font-weight: bold;">
                    STATUS: {status}
                </p>
            </div>
            <div style="text-align: right; color: #00ff41;">
                <p style="margin: 0;"><strong>LANGUAGE:</strong> {result['language'].upper()}</p>
                <p style="margin: 0;"><strong>SCAN_TIME:</strong> {result['execution_time']}s</p>
                <p style="margin: 0;"><strong>CODE_LINES:</strong> {result['line_count']}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary in terminal style
    if result.get('summary'):
        st.markdown("#### 📋 SYSTEM ANALYSIS")
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.8); border: 1px solid #00ff41; padding: 15px; border-radius: 5px; font-family: 'Share Tech Mono', monospace;">
        > {result['summary']}
        </div>
        """, unsafe_allow_html=True)
    
    # Create columns for different sections
    col1, col2 = st.columns(2)
    
    with col1:
        # Strengths
        if result.get('strengths'):
            st.markdown("#### ✅ SYSTEM STRENGTHS")
            for strength in result['strengths']:
                st.success(f"[+] {strength}")
        
        # Suggestions
        if result.get('suggestions'):
            st.markdown("#### 💡 ENHANCEMENT_PROTOCOLS")
            for suggestion in result['suggestions']:
                st.info(f"[*] {suggestion}")
    
    with col2:
        # Issues
        if result.get('issues'):
            st.markdown("#### ⚠️ SYSTEM_VULNERABILITIES")
            for issue in result['issues']:
                st.warning(f"[!] {issue}")
        
        # Security concerns
        if result.get('security_concerns'):
            st.markdown("#### 🔒 SECURITY_BREACH_DETECTED")
            for concern in result['security_concerns']:
                st.error(f"[ALERT] {concern}")
    
    # Performance notes
    if result.get('performance_notes'):
        st.markdown("#### ⚡ PERFORMANCE_OPTIMIZATION")
        for note in result['performance_notes']:
            st.info(f"[PERF] {note}")
    
    # Expandable raw response
    with st.expander("VIEW RAW_DATA_STREAM"):
        st.code(result.get('raw_response', 'NO_DATA_AVAILABLE'), language='text')

# Header with Matrix effect
st.markdown("""
<h1 style="text-align: center;">
🟢 MATRIX CODE ANALYZER 🟢
</h1>
<p style="text-align: center; color: #00ff41; font-family: 'Share Tech Mono', monospace; font-size: 18px;">
[NEURAL_NETWORK_ACTIVATED] • [MULTI_AI_ANALYSIS_ONLINE] • [SECURITY_LEVEL_9]
</p>
""", unsafe_allow_html=True)

# Sidebar - The Matrix Control Panel
with st.sidebar:
    st.markdown("### 🟢 CONTROL_PANEL")
    
    # Model status
    st.markdown("#### AVAILABLE_NEURAL_NETWORKS")
    available_models = analyzer.available_models
    
    if not available_models:
        st.error("❌ NO_NETWORKS_DETECTED")
        st.info("CONFIGURE_API_KEYS_IN_ENV_FILE")
        st.stop()
    
    # Display available models with Matrix styling
    for model, display_name in available_models.items():
        st.markdown(f"""
        <div style="background: rgba(0, 255, 65, 0.1); border: 1px solid #00ff41; padding: 5px; margin: 5px 0; border-radius: 3px;">
        🟢 <strong>{display_name}</strong> [ONLINE]
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Analysis options
    st.markdown("#### ANALYSIS_PARAMETERS")
    
    # Model selector with Matrix styling
    selected_model = st.selectbox(
        "SELECT_NEURAL_NETWORK",
        options=list(available_models.keys()),
        format_func=lambda x: f"🤖 {available_models[x]}"
    )
    
    # Multi-model analysis toggle
    analyze_all = st.checkbox("🔄 MULTI_NETWORK_SCAN", value=False)
    
    # Language selection
    languages = ["auto-detect", "python", "javascript", "java", "cpp", "csharp", "go", "rust"]
    selected_language = st.selectbox(
        "TARGET_LANGUAGE", 
        languages,
        format_func=lambda x: x.upper().replace("-", "_")
    )
    
    st.markdown("---")
    
    # Sample code injection
    st.markdown("#### CODE_INJECTION_SAMPLES")
    
    if st.button("🐍 INJECT_PYTHON_SAMPLE"):
        st.session_state.code_input = """def matrix_hack():
    # The Matrix has you...
    reality = "simulation"
    if reality == "simulation":
        print("Wake up, Neo...")
        return True
    return False

# Take the red pill
choice = matrix_hack()
for i in range(10):
    print(f"Level {i}: {'🟢' if choice else '🔴'}")
"""
    
    if st.button("🟨 INJECT_JAVASCRIPT_SAMPLE"):
        st.session_state.code_input = """function followTheWhiteRabbit(choice) {
    const matrix = {
        red_pill: "truth",
        blue_pill: "ignorance"
    };
    
    if (choice === "red_pill") {
        console.log("Welcome to the real world");
        return matrix[choice];
    }
    
    return "The story ends, you wake up in your bed...";
}

// The choice is yours
const reality = followTheWhiteRabbit("red_pill");
console.log(`Reality: ${reality}`);
"""

# Main Terminal Interface
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📟 CODE_INPUT_TERMINAL")
    
    # Code input with Matrix styling
    code_input = st.text_area(
        "PASTE_TARGET_CODE",
        value=st.session_state.get('code_input', ''),
        height=400,
        key="code_input",
        help="Insert code for neural network analysis..."
    )
    
    # Matrix-styled analyze button
    analyze_button = st.button(
        "🚀 INITIATE_SCAN",
        type="primary",
        disabled=not code_input.strip(),
        help="Begin deep neural analysis of target code"
    )

# Results Terminal
with col2:
    st.markdown("### 📊 ANALYSIS_OUTPUT_TERMINAL")
    
    if analyze_button and code_input.strip():
        with st.spinner("🟢 SCANNING... NEURAL_NETWORKS_PROCESSING..."):
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
                if comparison['consensus_issues']:
                    st.markdown("### 🤝 NEURAL_CONSENSUS_DETECTED")
                    st.markdown("""
                    <div style="background: rgba(255, 0, 0, 0.1); border: 2px solid #ff0000; padding: 15px; border-radius: 10px;">
                    <strong>CRITICAL_PATTERNS_IDENTIFIED_BY_MULTIPLE_NETWORKS:</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for issue in comparison['consensus_issues']:
                        st.error(f"🚨 CONSENSUS_ALERT: {issue}")
                
            else:
                # Single model analysis
                st.markdown(f"#### 🤖 {available_models[selected_model].upper()}_ANALYSIS")
                
                result = analyzer.analyze_code(
                    code_input,
                    selected_model,
                    selected_language if selected_language != "auto-detect" else None
                )
                display_matrix_analysis_result(result, available_models[selected_model])

# Instructions for new users
if not code_input.strip() and not analyze_button:
    st.markdown("""
    <div class="matrix-terminal" style="margin: 20px 0;">
        <h3 style="color: #00ff41; text-align: center;">🟢 WELCOME TO THE MATRIX 🟢</h3>
        <p style="color: #00ff41; font-family: 'Share Tech Mono', monospace;">
        > SYSTEM_STATUS: ONLINE<br>
        > NEURAL_NETWORKS: READY<br>
        > AWAITING_CODE_INPUT...<br><br>
        
        <strong>INITIALIZATION_PROTOCOL:</strong><br>
        1. PASTE_CODE → Left terminal<br>
        2. SELECT_NEURAL_NETWORK → Control panel<br>
        3. INITIATE_SCAN → Begin analysis<br>
        4. REVIEW_RESULTS → Right terminal<br><br>
        
        <em>The Matrix has you... but now you have the power to analyze it. 🟢</em>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer with Matrix signature
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #00ff41; font-family: 'Share Tech Mono', monospace; padding: 20px;">
    <p>🟢 POWERED_BY_NEURAL_NETWORKS • OPENAI • ANTHROPIC • DEEPSEEK • GOOGLE 🟢</p>
    <p><em>"There is no spoon... only code."</em></p>
    <p style="font-size: 12px;">MATRIX_ANALYZER_v2.0 • BUILD_2024 • SECURITY_CLEARANCE_OMEGA</p>
</div>
""", unsafe_allow_html=True) 