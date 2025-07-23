#!/usr/bin/env python3
"""
Launch script for LLM Code Analyzer
Checks system requirements and starts the Streamlit app
"""

import sys
import os
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all requirements are met."""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    if sys.version_info < (3, 11):
        print(f"❌ Python 3.11+ required, found {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]}")
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ app.py not found. Please run from project root directory.")
        return False
    print("✅ Project structure verified")
    
    # Check if analyzer module can be imported
    try:
        from analyzer import CodeAnalyzer
        analyzer = CodeAnalyzer()
        models = analyzer.available_models
        print(f"✅ Analyzer module loaded successfully")
        print(f"📊 Available models: {len(models)}")
        
        if not models:
            print("⚠️  No API keys configured in .env file")
            print("   Add at least one API key to use the analyzer")
        else:
            for key, name in models.items():
                print(f"   • {name}")
        
    except Exception as e:
        print(f"❌ Failed to load analyzer: {e}")
        return False
    
    # Check Streamlit
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit not installed")
        return False
    
    return True

def launch_app():
    """Launch the Streamlit application."""
    print("\n🚀 Starting LLM Code Analyzer...")
    print("=" * 50)
    
    try:
        # Start Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "true",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ]
        
        print("📱 Application will be available at:")
        print("   • Local: http://localhost:8501")
        print("   • Network: http://0.0.0.0:8501")
        print("\n💡 Press Ctrl+C to stop the application")
        print("=" * 50)
        
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start application: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

def main():
    """Main entry point."""
    print("🔍 LLM Code Analyzer - Launcher")
    print("=" * 40)
    
    # Check requirements first
    if not check_requirements():
        print("\n❌ Requirements check failed")
        print("\nTo fix issues:")
        print("1. Ensure Python 3.11+ is installed")
        print("2. Run: pip install -r requirements.txt")
        print("3. Configure API keys in .env file")
        sys.exit(1)
    
    print("\n✅ All requirements satisfied!")
    
    # Launch the app
    if not launch_app():
        sys.exit(1)

if __name__ == "__main__":
    main() 