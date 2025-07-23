#!/usr/bin/env python3
"""
🟢 MATRIX CODE ANALYZER LAUNCHER 🟢
Enter the Matrix... if you dare.
"""

import sys
import os
import subprocess
from pathlib import Path

def matrix_banner():
    """Display Matrix-style banner."""
    print("""
🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢
   
   ███╗   ███╗ █████╗ ████████╗██████╗ ██╗██╗  ██╗    
   ████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝    
   ██╔████╔██║███████║   ██║   ██████╔╝██║ ╚███╔╝     
   ██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║ ██╔██╗     
   ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║██╔╝ ██╗    
   ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝    
                                                        
        █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗███████╗███████╗██████╗ 
       ██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝╚══███╔╝██╔════╝██╔══██╗
       ███████║██╔██╗ ██║███████║██║   ╚████╔╝   ███╔╝ █████╗  ██████╔╝
       ██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝   ███╔╝  ██╔══╝  ██╔══██╗
       ██║  ██║██║ ╚████║██║  ██║███████╗██║   ███████╗███████╗██║  ██║
       ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝
                                                                        
🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢
    """)
    print("🟢 NEURAL NETWORK INITIALIZATION SEQUENCE STARTING...")
    print("🟢 'There is no spoon... only code.'")
    print("🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢")

def check_matrix_requirements():
    """Check if the Matrix is ready."""
    print("\n🟢 SCANNING MATRIX REQUIREMENTS...")
    
    # Check Python version
    if sys.version_info < (3, 11):
        print(f"❌ INCOMPATIBLE_PYTHON_VERSION: {sys.version}")
        print("🟢 UPGRADE_TO_PYTHON_3.11+_REQUIRED")
        return False
    print(f"✅ PYTHON_VERSION: {sys.version.split()[0]} [COMPATIBLE]")
    
    # Check if we're in the right dimension
    if not Path("matrix_app.py").exists():
        print("❌ MATRIX_APP_NOT_FOUND")
        print("🟢 ENSURE_YOU_ARE_IN_THE_CORRECT_DIRECTORY")
        return False
    print("✅ MATRIX_APPLICATION: LOCATED")
    
    # Check if analyzer module is accessible
    try:
        from analyzer import CodeAnalyzer
        analyzer = CodeAnalyzer()
        models = analyzer.available_models
        print(f"✅ NEURAL_NETWORKS: ONLINE")
        print(f"🟢 AVAILABLE_AI_MODELS: {len(models)}")
        
        if not models:
            print("⚠️  NO_API_KEYS_DETECTED")
            print("🟢 CONFIGURE_NEURAL_NETWORK_ACCESS_CODES")
            print("🟢 REQUIRED: OPENAI • ANTHROPIC • GEMINI • DEEPSEEK")
        else:
            for key, name in models.items():
                print(f"   🤖 {name} [READY]")
        
    except Exception as e:
        print(f"❌ NEURAL_NETWORK_ERROR: {e}")
        return False
    
    # Check Streamlit
    try:
        import streamlit
        print(f"✅ MATRIX_INTERFACE: v{streamlit.__version__} [OPERATIONAL]")
    except ImportError:
        print("❌ MATRIX_INTERFACE_NOT_FOUND")
        print("🟢 RUN: pip install streamlit")
        return False
    
    return True

def enter_matrix():
    """Enter the Matrix."""
    print("\n🟢 INITIATING_MATRIX_SEQUENCE...")
    print("🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢")
    
    try:
        # Start the Matrix interface
        cmd = [
            sys.executable, "-m", "streamlit", "run", "matrix_app.py",
            "--server.headless", "true",
            "--server.port", "8503",
            "--server.address", "0.0.0.0"
        ]
        
        print("🟢 MATRIX_PORTAL_COORDINATES:")
        print("   🌐 LOCAL_ACCESS: http://localhost:8503")
        print("   🌐 NETWORK_ACCESS: http://0.0.0.0:8503")
        print("\n🟢 MATRIX_ACTIVATED...")
        print("🟢 'Welcome to the real world, Neo.'")
        print("🟢 [Press Ctrl+C to exit the Matrix]")
        print("🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢")
        
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n🟢 MATRIX_SESSION_TERMINATED")
        print("🟢 'Until we meet again in the Matrix...'")
    except subprocess.CalledProcessError as e:
        print(f"❌ MATRIX_INITIALIZATION_FAILED: {e}")
        return False
    except Exception as e:
        print(f"❌ UNEXPECTED_MATRIX_ERROR: {e}")
        return False
    
    return True

def main():
    """Main entry point to the Matrix."""
    matrix_banner()
    
    # Check if the Matrix is ready
    if not check_matrix_requirements():
        print("\n❌ MATRIX_REQUIREMENTS_NOT_MET")
        print("\n🟢 TROUBLESHOOTING_PROTOCOL:")
        print("1. ENSURE_PYTHON_3.11+_INSTALLED")
        print("2. RUN: pip install -r requirements.txt")
        print("3. CONFIGURE_API_KEYS_IN_.ENV_FILE")
        print("4. RETRY_MATRIX_INITIALIZATION")
        sys.exit(1)
    
    print("\n✅ ALL_MATRIX_SYSTEMS_OPERATIONAL")
    print("🟢 READY_TO_ENTER_THE_MATRIX...")
    
    # Enter the Matrix
    if not enter_matrix():
        sys.exit(1)

if __name__ == "__main__":
    main() 