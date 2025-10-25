import streamlit as st
from dotenv import load_dotenv
import streamlit.components.v1 as components
from analyzer import CodeAnalyzer
from typing import Any, Iterable, List
import os
import html

# Force reload environment variables
load_dotenv(override=True)

st.set_page_config(
    page_title="Matrix Code Analyzer",
    page_icon="🧠",
    layout="wide"
)

# Debug sidebar removed for cleaner UI

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono:wght@400&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
  --matrix-green: #00ff41; /* Brighter Matrix Green */
  --matrix-blue: #0ccffa;
  --matrix-bg: #000000; /* Solid black for deeper matrix feel */
  --text-main: #e7fceb;
  --text-muted: #94a9a0;
  --panel-bg: rgba(6, 16, 28, 0.55);
  --panel-border: rgba(0, 255, 65, 0.25); /* Green border for panels */
}

    .stApp {
  background: var(--matrix-bg);
  color: var(--text-main);
  font-family: 'Share Tech Mono', monospace; /* Default text to matrix font */
}

.stApp::before {
  content: '';
        position: fixed;
  inset: 0;
  background: linear-gradient(135deg, rgba(0, 255, 130, 0.05) 0%, transparent 55%),
              linear-gradient(225deg, rgba(12, 207, 250, 0.06) 0%, transparent 60%);
  z-index: -3;
}

.stApp::after {
  content: '';
  position: fixed;
  inset: 0;
  background: radial-gradient(circle at 18% 20%, rgba(0, 255, 140, 0.08), transparent 58%),
              radial-gradient(circle at 78% 12%, rgba(12, 207, 250, 0.07), transparent 48%);
  z-index: -2;
}

[data-testid="stAppViewContainer"] {
  position: relative;
  z-index: 0;
}

html, body {
  overflow-y: auto !important;
  height: auto !important;
}

[data-testid="stAppViewContainer"] {
  overflow-y: auto !important;
  height: auto !important;
}

.stApp {
  overflow-y: auto !important;
  height: auto !important;
}

.block-container {
  overflow-y: visible !important;
}

/* Ensure main content can scroll */
[data-testid="stAppViewContainer"] > div {
  overflow-y: auto !important;
  height: auto !important;
}

/* Override any Streamlit default height constraints */
.stApp > div {
  height: auto !important;
  min-height: 100vh !important;
}

.matrix-rain {
  position: fixed;
  inset: 0;
        overflow: hidden;
  pointer-events: none;
        z-index: -1;
    }
    
.matrix-rain span {
        position: absolute;
  top: -10%;
  color: rgba(0, 255, 65, 0.45); /* Brighter matrix rain */
        font-family: 'Share Tech Mono', monospace;
        font-size: 14px;
  animation: matrixFall linear infinite;
  text-shadow: 0 0 10px rgba(0, 255, 65, 0.6); /* Stronger glow */
}

@keyframes matrixFall {
  from { transform: translateY(-10%); opacity: 0; }
  20% { opacity: 1; }
  to { transform: translateY(110vh); opacity: 0; }
}

[data-testid="stHeader"] {
  background: transparent;
  border-bottom: none;
}

.block-container {
  padding-top: 3rem;
  padding-bottom: 3.5rem;
  max-width: 1140px;
}

a {
  color: var(--matrix-green);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.glass-panel {
  background: rgba(0, 0, 0, 0.7);
  border: 1px solid var(--panel-border);
  border-radius: 12px; /* Slightly less rounded for matrix look */
  padding: 28px;
  backdrop-filter: blur(8px); /* Softer blur */
  box-shadow: 0 0 25px rgba(0, 255, 65, 0.2); /* Green glow for panels */
  margin-bottom: 1.6rem;
}

.hero {
  text-align: center;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  opacity: 0.3;
  background: linear-gradient(130deg, rgba(0, 255, 65, 0.15), rgba(0, 200, 255, 0.08));
  pointer-events: none;
}

.hero-label {
  font-family: 'Orbitron', sans-serif; /* Use Orbitron for hero label */
  font-size: 0.9rem;
  letter-spacing: 0.4em;
  text-transform: uppercase;
  color: var(--matrix-green);
  margin-bottom: 0.6rem;
  text-shadow: 0 0 8px rgba(0, 255, 65, 0.5);
}

.hero h1 {
  font-family: 'Orbitron', sans-serif; /* Use Orbitron for hero title */
  margin-bottom: 0.6rem;
  font-size: clamp(2.5rem, 4vw, 3.8rem);
  font-weight: 700;
  letter-spacing: -0.05em;
  position: relative;
  z-index: 1;
  color: var(--matrix-green);
  text-shadow: 0 0 15px rgba(0, 255, 65, 0.8), 0 0 25px rgba(0, 255, 65, 0.6);
}

.hero .subline {
  font-family: 'Share Tech Mono', monospace; /* Use Share Tech Mono for subline */
  color: rgba(231, 252, 235, 0.8);
  font-size: 1.1rem;
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.7;
  position: relative;
  z-index: 1;
}

.hero-badges {
  display: flex;
  gap: 0.85rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 2rem;
  position: relative;
  z-index: 1;
}

.hero-badge {
  padding: 0.4rem 1rem;
  border-radius: 999px;
  background: rgba(0, 255, 65, 0.15);
  border: 1px solid rgba(0, 255, 65, 0.4);
  color: var(--matrix-green);
  font-size: 0.9rem;
  font-weight: 500;
  text-shadow: 0 0 5px rgba(0, 255, 65, 0.4);
}

.body-text {
  color: var(--text-main);
  font-family: 'Share Tech Mono', monospace;
  font-size: 1rem;
  line-height: 1.7;
  margin: 0;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.2rem;
}

    .stSelectbox > div > div {
  background: rgba(0, 0, 0, 0.8);
  border-radius: 10px;
  border: 1px solid rgba(0, 255, 65, 0.3);
  color: var(--text-main);
  font-family: 'Share Tech Mono', monospace;
}

.stSelectbox label, .stTextInput label, .stFileUploader label {
  font-family: 'Orbitron', sans-serif;
  font-weight: 600;
  color: var(--matrix-green);
  text-shadow: 0 0 5px rgba(0, 255, 65, 0.3);
}

.stTextInput > div > div > input {
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid rgba(0, 255, 65, 0.25);
  color: var(--text-main);
  font-family: 'Share Tech Mono', monospace;
}

textarea {
  border-radius: 12px !important;
  background: rgba(0, 0, 0, 0.85) !important;
  border: 1px solid rgba(0, 255, 65, 0.3) !important;
  color: var(--text-main) !important;
  font-family: 'Share Tech Mono', monospace !important;
  resize: vertical;
}

textarea::placeholder,
.stTextInput > div > div > input::placeholder {
  color: rgba(0, 255, 65, 0.5) !important;
}

.stFileUploader > div {
  border-radius: 12px !important;
  border: 2px dashed rgba(0, 255, 65, 0.5) !important;
  background: rgba(0, 0, 0, 0.7) !important;
  padding: 1.5rem 2rem !important;
}

.stButton > button {
  height: 50px;
  border-radius: 12px;
  font-weight: 700;
  letter-spacing: 0.05em;
  background: linear-gradient(120deg, var(--matrix-green), rgba(0, 200, 255, 0.8));
  color: #000;
  border: none;
  box-shadow: 0 0 20px rgba(0, 255, 65, 0.6);
  text-transform: uppercase;
  transition: all 0.3s ease;
}

.stButton > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 35px rgba(0, 255, 65, 0.9);
  background: linear-gradient(120deg, rgba(0, 255, 65, 0.95), rgba(0, 220, 255, 0.95));
}

    .stTabs [data-baseweb="tab-list"] {
  background: rgba(0, 0, 0, 0.6);
  border-radius: 12px;
  padding: 0.5rem;
  border: 1px solid rgba(0, 255, 65, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
  border-radius: 8px;
  font-weight: 500;
  color: rgba(0, 255, 65, 0.7);
  font-family: 'Orbitron', sans-serif;
  padding: 0.75rem 1.2rem;
    }
    
    .stTabs [aria-selected="true"] {
  background: rgba(0, 255, 65, 0.1);
  color: var(--matrix-green);
  text-shadow: 0 0 5px rgba(0, 255, 65, 0.5);
}

.stTabs [data-baseweb="tab-panel"] {
  background: rgba(0, 0, 0, 0.75);
  border: 1px solid rgba(0, 255, 65, 0.2);
  border-radius: 12px;
  padding: 28px;
  margin-top: 1.5rem;
  backdrop-filter: blur(8px);
  box-shadow: 0 0 25px rgba(0, 255, 65, 0.2);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1.2rem;
}

.stats-card {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(0, 255, 65, 0.15);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  box-shadow: 0 0 15px rgba(0, 255, 65, 0.1);
}

.stats-card .label {
  color: rgba(0, 255, 65, 0.8);
  font-size: 0.8rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-family: 'Share Tech Mono', monospace;
}

.stats-card .value {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.9rem;
  font-weight: 700;
  color: var(--matrix-green);
  text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
}

.stats-card .status {
  font-size: 0.95rem;
  color: rgba(0, 255, 65, 0.7);
}

.list-card {
  background: rgba(0, 0, 0, 0.65);
  border: 1px solid rgba(0, 255, 65, 0.18);
  border-radius: 12px;
  padding: 1.5rem 1.8rem;
  margin-bottom: 1.2rem;
  box-shadow: 0 0 18px rgba(0, 255, 65, 0.15);
}

.list-card h3 {
  font-family: 'Orbitron', sans-serif;
  margin-bottom: 1rem;
  font-size: 1.2rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.7rem;
  color: var(--matrix-green);
  text-shadow: 0 0 8px rgba(0, 255, 65, 0.4);
}

.list-card ul {
  margin: 0;
  padding-left: 1.2rem;
  color: rgba(231, 252, 235, 0.9);
  font-family: 'Share Tech Mono', monospace;
  display: grid;
  gap: 0.6rem;
}

.list-card li {
  line-height: 1.5;
  position: relative;
}

.list-card li::before {
  content: '•'; /* Use a bullet point for simple list styling */
  position: absolute;
  left: -1rem;
  color: var(--matrix-green);
  font-size: 1.2em;
  line-height: 1;
  text-shadow: 0 0 5px rgba(0, 255, 65, 0.7);
}

.model-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.6rem 1rem;
  border-radius: 999px;
  background: rgba(0, 255, 65, 0.1);
  border: 1px solid rgba(0, 255, 65, 0.3);
  font-size: 0.95rem;
  color: var(--matrix-green);
  margin-bottom: 1.5rem;
  font-family: 'Orbitron', sans-serif;
  text-shadow: 0 0 6px rgba(0, 255, 65, 0.4);
}

.file-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 0.6rem;
  font-size: 0.9rem;
  color: rgba(231, 252, 235, 0.7);
  font-family: 'Share Tech Mono', monospace;
}

.file-meta span {
  padding: 0.4rem 0.9rem;
  border-radius: 999px;
  background: rgba(0, 255, 65, 0.08);
  border: 1px solid rgba(0, 255, 65, 0.2);
  text-shadow: 0 0 4px rgba(0, 255, 65, 0.2);
}

.stAlert {
  border-radius: 12px;
  border: 1px solid rgba(0, 255, 65, 0.3);
  background: rgba(0, 0, 0, 0.75);
  color: var(--text-main);
  font-family: 'Share Tech Mono', monospace;
  box-shadow: 0 0 15px rgba(0, 255, 65, 0.25);
}

.streamlit-expanderHeader {
  background: rgba(0, 0, 0, 0.6);
  border-radius: 12px;
  border: 1px solid rgba(0, 255, 65, 0.2);
  color: var(--matrix-green);
  font-family: 'Orbitron', sans-serif;
  text-shadow: 0 0 5px rgba(0, 255, 65, 0.3);
}

.stSpinner > div {
  border-top-color: var(--matrix-green) !important;
  border-right-color: var(--matrix-blue) !important;
}

@media (max-width: 768px) {
  .block-container {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  .glass-panel, .stTabs [data-baseweb="tab-panel"] {
    padding: 18px;
  }
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .hero h1 {
    font-size: 2.5rem;
  }
  .hero-badges {
    gap: 0.6rem;
  }
  .hero-badge {
    font-size: 0.8rem;
    padding: 0.3rem 0.7rem;
  }
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown(
    """
    <div class="matrix-rain" id="matrix-rain"></div>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_analyzer():
    # Use /tmp for cache in Docker/HF Spaces (always writable)
    # Use .analyzer_cache for local development
    cache_dir = "/tmp/.analyzer_cache" if os.path.exists("/app") else ".analyzer_cache"
    return CodeAnalyzer(cache_dir=cache_dir)


analyzer = get_analyzer()
AVAILABLE_MODELS = analyzer.available_models

if not AVAILABLE_MODELS:
    st.error("No AI models configured. Add API keys to your .env file and restart the app.")
    st.stop()


LANGUAGE_DISPLAY = {
    "auto": "Auto Detect",
    "python": "Python",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "html": "HTML",
    "css": "CSS",
    "java": "Java",
    "cpp": "C++",
    "c": "C",
    "csharp": "C#",
    "go": "Go",
    "rust": "Rust",
    "php": "PHP",
    "ruby": "Ruby",
    "swift": "Swift",
    "kotlin": "Kotlin",
}
LANGUAGE_OPTIONS = list(LANGUAGE_DISPLAY.keys())


def ensure_list(items: Any) -> List[str]:
    if not items:
        return []
    if isinstance(items, str):
        clean = items.strip()
        return [clean] if clean else []
    if isinstance(items, dict):
        return [f"{key}: {value}" for key, value in items.items() if str(value).strip()]
    if isinstance(items, Iterable):
        values = []
        for entry in items:
            if entry is None:
                continue
            text = str(entry).strip()
            if text:
                values.append(text)
        return values
    return [str(items)]


def parse_score(raw: Any) -> float:
    try:
        return float(raw)
    except (TypeError, ValueError):
        return 0.0


def score_badge(score: float) -> tuple[str, str]:
    if score >= 80:
        return "Excellent", "#00fba4"
    if score >= 60:
        return "Review Suggested", "#ffd76a"
    return "Needs Attention", "#ff6b6b"


def render_list_section(title: str, icon: str, content: Any, fallback: str | None = None) -> None:
    entries = ensure_list(content)
    if entries:
        items_html = "".join(f"<li>{html.escape(entry)}</li>" for entry in entries[:6])
        st.markdown(
            f"""
            <div class="list-card">
                <h3>{icon} {title}</h3>
                <ul>{items_html}</ul>
    </div>
            """,
            unsafe_allow_html=True,
        )
    elif fallback:
        st.markdown(
            f"""
            <div class="list-card">
                <h3>{icon} {title}</h3>
                <p class="body-text">{html.escape(fallback)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_code_result(result: dict[str, Any], model_label: str) -> None:
    if result.get("error"):
        st.error(f"Analysis failed: {result['error']}")
        return

    score = parse_score(result.get("quality_score", 0))
    status_label, status_color = score_badge(score)
    language = (result.get("language") or "auto").upper()
    line_count = result.get("line_count", "-")
    exec_time = parse_score(result.get("execution_time", 0.0))
    cached_text = "Hit" if result.get("cached") else "Fresh"

    stats = [
        {"label": "Quality Score", "value": f"{int(round(score))}/100", "sub": status_label, "color": status_color},
        {"label": "Language", "value": language, "sub": "Detected" if language != "AUTO" else "Auto"},
        {"label": "Lines", "value": line_count, "sub": "Analyzed"},
        {"label": "Latency", "value": f"{exec_time:.1f}s", "sub": "Runtime"},
        {"label": "Cache", "value": cached_text, "sub": "Result Store"},
    ]

    # Render stats using native Streamlit components to avoid raw HTML showing
    st.markdown(
        f"""
        <div class="glass-panel">
            <div class="model-chip">🤖 {model_label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(len(stats))
    for idx, stat in enumerate(stats):
        with cols[idx]:
            st.metric(label=stat["label"], value=stat["value"], delta=stat["sub"])

    summary = result.get("summary")
    if summary:
        st.markdown(
            f"""
            <div class="glass-panel">
                <h3>📋 Overview</h3>
                <p class="body-text">{html.escape(summary)}</p>
        </div>
            """,
            unsafe_allow_html=True,
        )

    render_list_section("Highlights", "✨", result.get("strengths"))
    render_list_section("Bug Detection", "🐞", result.get("bugs") or result.get("issues"), "No critical bugs were flagged.")
    render_list_section("Security", "🔒", result.get("security_vulnerabilities") or result.get("security_concerns"), "No security vulnerabilities detected.")
    render_list_section("Code Quality", "🧩", result.get("quality_issues"), "Structure looks solid and maintainable.")
    render_list_section("Quick Fixes", "⚡", result.get("quick_fixes"), "No urgent fixes suggested.")
    render_list_section("Suggestions", "💡", result.get("suggestions"))

    raw = result.get("raw_response")
    if raw:
        with st.expander("View full model response", expanded=False):
            st.code(raw, language="text")


def render_repo_result(result: dict[str, Any], model_label: str) -> None:
    if result.get("error"):
        st.error(f"Repository analysis failed: {result['error']}")
        return

    info = result.get("repository_info", {})
    repo_name = info.get("name", "Repository")
    repo_desc = info.get("description") or "No description provided."
    repo_url = result.get("repo_url") or st.session_state.get("repo_analysis_url")

    repo_stats = [
        {"label": "Primary Language", "value": info.get("language", "Unknown"), "sub": "Detected"},
        {"label": "Stars", "value": info.get("stars", 0), "sub": "Community"},
        {"label": "Forks", "value": info.get("forks", 0), "sub": "Collaboration"},
        {"label": "Size", "value": f"{info.get('size', 0)} KB", "sub": "Repo Size"},
        {"label": "Latency", "value": f"{parse_score(result.get('execution_time', 0.0)):.1f}s", "sub": "Runtime"},
    ]

    link_html = f'<p class="body-text"><a href="{repo_url}" target="_blank">View repository ↗</a></p>' if repo_url else ""

    # Header card
    st.markdown(
        f"""
        <div class="glass-panel">
            <div class="model-chip">🤖 {html.escape(model_label)}</div>
            <h2 style="margin-bottom:0.35rem;">{html.escape(repo_name)}</h2>
            <p class="body-text" style="color: var(--text-muted); margin-bottom:1.2rem;">{html.escape(repo_desc)}</p>
            {link_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Metrics row
    cols = st.columns(len(repo_stats))
    for idx, stat in enumerate(repo_stats):
        with cols[idx]:
            st.metric(label=stat["label"], value=stat["value"], delta=stat["sub"])

    overview = result.get("project_overview")
    if overview:
        st.markdown(
            f"""
            <div class="glass-panel">
                <h3>📋 Project Overview</h3>
                <p class="body-text">{html.escape(overview)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_list_section("Architecture Quality", "🏗️", result.get("architecture_quality"), "Project structure looks well organized.")
    render_list_section("Critical Issues", "🚨", result.get("critical_issues"), "No critical issues were highlighted.")
    render_list_section("Priority Improvements", "🎯", result.get("improvement_priorities"), "No immediate improvements suggested.")
    render_list_section("Onboarding Guide", "🚀", result.get("onboarding_guide"), "No specific onboarding steps identified.")
    render_list_section("Tech Stack", "🛠️", result.get("tech_stack_rationale"), "Tech stack details were not identified.")
    render_list_section("API Endpoints", "🔌", result.get("api_endpoint_summary"), "No API endpoints were identified.")

    raw = result.get("raw_response")
    if raw:
        with st.expander("View full model response", expanded=False):
            st.code(raw, language="text")


if "code_input" not in st.session_state:
    st.session_state.code_input = ""
if "code_file_meta" not in st.session_state:
    st.session_state.code_file_meta = None
if "code_analysis_result" not in st.session_state:
    st.session_state.code_analysis_result = None
if "code_analysis_model" not in st.session_state:
    st.session_state.code_analysis_model = ""
if "repo_analysis_result" not in st.session_state:
    st.session_state.repo_analysis_result = None
if "repo_analysis_model" not in st.session_state:
    st.session_state.repo_analysis_model = ""
if "repo_analysis_url" not in st.session_state:
    st.session_state.repo_analysis_url = ""

st.markdown(
    """
    <div class="glass-panel hero">
        <div class="hero-label">CODE ANALYZER</div>
        <h1>AI Code Analyzer</h1>
        <p class="subline">Inspect bugs, surface security gaps, and review repositories with instant feedback.</p>
        <div class="hero-badges">
            <span class="hero-badge">🧠 Multi-model</span>
            <span class="hero-badge">🔍 Bug & Security Scan</span>
            <span class="hero-badge">⚡ Instant Results</span>
            <span class="hero-badge">📦 GitHub Ready</span>
        </div>
    </div>
    <script>
    (function drizzle() {
      const container = document.getElementById('matrix-rain');
      if (!container || container.dataset.initialized) return;
      container.dataset.initialized = 'true';
      const glyphs = "01ΛΣΞ∑¥$#@*&%=+";
      const nodeCount = 80;
      for (let i = 0; i < nodeCount; i++) {
        const drop = document.createElement('span');
        drop.textContent = glyphs[Math.floor(Math.random() * glyphs.length)];
        drop.style.left = Math.random() * 100 + '%';
        drop.style.animationDuration = (Math.random() * 4 + 3) + 's';
        drop.style.animationDelay = (Math.random() * 4) + 's';
        container.appendChild(drop);
      }
    })();
    </script>
    """,
    unsafe_allow_html=True,
)

code_tab, repo_tab = st.tabs(["Code Analysis", "Repository Insights"])

with code_tab:
    model_keys = list(AVAILABLE_MODELS.keys())
    selected_model_code = st.selectbox(
        "AI Model",
        options=model_keys,
        format_func=lambda key: AVAILABLE_MODELS[key],
        key="code_model_select",
    )

    selected_language = st.selectbox(
        "Language",
        LANGUAGE_OPTIONS,
        format_func=lambda code: LANGUAGE_DISPLAY[code],
        key="language_select",
    )

    uploaded_file = st.file_uploader(
        "Upload a code file",
        type=["py", "js", "java", "cpp", "c", "cs", "go", "rs", "php", "rb", "swift", "kt", "txt"],
        key="code_file_uploader",
    )

    if uploaded_file is not None:
        raw_bytes = uploaded_file.read()
        try:
            decoded = raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            st.error("Only UTF-8 encoded files are supported.")
        else:
            st.session_state.code_input = decoded
            st.session_state.code_file_meta = {
                "name": uploaded_file.name,
                "size": len(raw_bytes),
                "lines": len(decoded.splitlines()),
            }

    st.text_area(
        "Or paste code below",
        key="code_input",
        height=320,
        placeholder="Paste any code snippet to inspect bugs, security gaps, and quality issues.",
    )

    meta = st.session_state.get("code_file_meta")
    if meta:
        st.markdown(
            f"""
            <div class="list-card">
                <h3> Active File</h3>
                <div class="file-meta">
                    <span>{meta['name']}</span>
                    <span>{meta['lines']} lines</span>
                    <span>{meta['size']} bytes</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    analyze_code_clicked = st.button("Run Code Analysis", key="code_analyze_button", use_container_width=True)

    if analyze_code_clicked:
        snippet = st.session_state.get("code_input", "").strip()
        if not snippet:
            st.error("Please upload a file or paste some code to analyze.")
        else:
            with st.spinner("Analyzing code..."):
                language_arg = None if selected_language == "auto" else selected_language
                result = analyzer.analyze_code(snippet, selected_model_code, language_arg)
            st.session_state.code_analysis_result = result
            st.session_state.code_analysis_model = AVAILABLE_MODELS[selected_model_code]

    if st.session_state.get("code_analysis_result"):
        render_code_result(st.session_state.code_analysis_result, st.session_state.get("code_analysis_model", ""))
    else:
        st.info("Upload a file or paste code to generate an analysis.")

with repo_tab:
    model_keys = list(AVAILABLE_MODELS.keys())
    selected_model_repo = st.selectbox(
        "AI Model",
        options=model_keys,
        format_func=lambda key: AVAILABLE_MODELS[key],
        key="repo_model_select",
    )

    st.text_input(
        "GitHub repository URL",
        placeholder="https://github.com/owner/repo",
        key="repo_analysis_url",
    )

    analyze_repo_clicked = st.button("Analyze Repository", key="repo_analyze_button", use_container_width=True)

    if analyze_repo_clicked:
        repo_url = st.session_state.get("repo_analysis_url", "").strip()
        if not repo_url:
            st.error("Enter a GitHub repository URL.")
        else:
            with st.spinner("Inspecting repository..."):
                result = analyzer.analyze_github_repo(repo_url, selected_model_repo)
            st.session_state.repo_analysis_result = result
            st.session_state.repo_analysis_model = AVAILABLE_MODELS[selected_model_repo]

    if st.session_state.get("repo_analysis_result"):
        render_repo_result(
            st.session_state.repo_analysis_result,
            st.session_state.get("repo_analysis_model", ""),
        )
    else:
        st.info("Provide a public GitHub repository URL to review its structure, issues, and improvements.")
