#!/usr/bin/env python3
"""
Optimized Matrix Code Analyzer with CodeT5+

This integrates the optimized CodeT5+ analyzer into your existing
Matrix-themed Streamlit application with speed optimizations.

Author: AI Code Analyzer Project
Date: 2025
"""

import streamlit as st
import time
import torch
from optimized_code_analyzer import OptimizedCodeAnalyzer

# Page configuration
st.set_page_config(
    page_title="AI Code Analyzer - Optimized",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Matrix theme
st.markdown("""
<style>
    .main {
        background-color: #0a0a0a;
        color: #00ff00;
    }
    
    .stApp {
        background-color: #0a0a0a;
    }
    
    .matrix-header {
        background: linear-gradient(90deg, #00ff00, #008800);
        color: #000000;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 30px;
        font-family: 'Courier New', monospace;
    }
    
    .analysis-box {
        background-color: #001100;
        border: 2px solid #00ff00;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .speed-indicator {
        background-color: #002200;
        border: 1px solid #00ff00;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    
    .cache-info {
        background-color: #000800;
        border: 1px solid #008800;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_analyzer():
    """
    Load the optimized analyzer (cached for performance).
    """
    return OptimizedCodeAnalyzer()

def main():
    """
    Main Streamlit application.
    """
    # Header
    st.markdown("""
    <div class="matrix-header">
        <h1>🤖 AI Code Analyzer - Optimized</h1>
        <p>Powered by CodeT5+ with Speed Optimizations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load analyzer
    with st.spinner("🚀 Loading optimized CodeT5+ model..."):
        analyzer = load_analyzer()
    
    # Sidebar
    st.sidebar.markdown("## ⚙️ Analysis Options")
    
    analysis_mode = st.sidebar.selectbox(
        "Analysis Mode",
        ["Streaming (Interactive)", "Fast (Batch)"],
        help="Streaming shows progress, Fast is optimized for speed"
    )
    
    show_progress = st.sidebar.checkbox(
        "Show Progress Indicators",
        value=True,
        help="Display progress bars and timing information"
    )
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("## 📝 Code Input")
        
        # Code input
        code_input = st.text_area(
            "Enter your code:",
            height=300,
            placeholder="def hello():\n    print('Hello, World!')",
            help="Paste your code here for analysis"
        )
        
        # Analysis button
        analyze_button = st.button(
            "🔍 Analyze Code",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        st.markdown("## 📊 Analysis Results")
        
        if analyze_button and code_input.strip():
            # Perform analysis
            start_time = time.time()
            
            if analysis_mode == "Streaming (Interactive)":
                # Streaming analysis
                st.markdown("### 🔄 Streaming Analysis")
                
                # Create placeholder for streaming results
                result_placeholder = st.empty()
                progress_placeholder = st.empty()
                
                # Show progress
                if show_progress:
                    progress_bar = progress_placeholder.progress(0)
                    status_text = st.empty()
                
                try:
                    # Stream analysis
                    analysis_text = ""
                    for partial_result in analyzer.analyze_code_streaming(code_input, show_progress):
                        analysis_text = partial_result
                        
                        # Update progress
                        if show_progress:
                            progress_bar.progress(50)
                            status_text.text("🔍 Analyzing code...")
                    
                    # Complete analysis
                    if show_progress:
                        progress_bar.progress(100)
                        status_text.text("✅ Analysis complete!")
                    
                    # Display results
                    result_placeholder.markdown(f"""
                    <div class="analysis-box">
                        <h4>📄 Analysis Results:</h4>
                        <p>{analysis_text}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
            
            else:
                # Fast analysis
                st.markdown("### ⚡ Fast Analysis")
                
                if show_progress:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    progress_bar.progress(25)
                    status_text.text("🚀 Loading model...")
                
                try:
                    # Perform fast analysis
                    result = analyzer.analyze_code_fast(code_input)
                    
                    if show_progress:
                        progress_bar.progress(100)
                        status_text.text("✅ Analysis complete!")
                    
                    # Display results
                    st.markdown(f"""
                    <div class="analysis-box">
                        <h4>📄 Analysis Results:</h4>
                        <p>{result['analysis']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
            
            # Show performance metrics
            total_time = time.time() - start_time
            
            st.markdown(f"""
            <div class="speed-indicator">
                <h4>⚡ Performance Metrics:</h4>
                <p><strong>Total Time:</strong> {total_time:.2f}s</p>
                <p><strong>Analysis Mode:</strong> {analysis_mode}</p>
                <p><strong>Model:</strong> CodeT5+ (Optimized)</p>
            </div>
            """, unsafe_allow_html=True)
        
        elif analyze_button and not code_input.strip():
            st.warning("⚠️ Please enter some code to analyze!")
        
        else:
            st.info("👆 Enter code and click 'Analyze Code' to get started!")
    
    # Model information
    st.markdown("## 📊 Model Information")
    
    model_info = analyzer.get_model_info()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Model Parameters", f"{model_info['parameters']:,}")
    
    with col2:
        st.metric("Cache Size", f"{model_info['cache_size']} analyses")
    
    with col3:
        st.metric("Device", str(model_info['device']))
    
    # Cache information
    st.markdown("""
    <div class="cache-info">
        <h4>💾 Cache Information:</h4>
        <p>• Cached analyses are reused for identical code</p>
        <p>• Cache improves speed for repeated analyses</p>
        <p>• Cache is automatically managed</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #008800;">
        <p>🚀 Optimized AI Code Analyzer | Powered by CodeT5+ | Matrix Theme</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
