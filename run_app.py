#!/usr/bin/env python3
"""
AI Code Analyzer - Local Startup Script

This script starts the Matrix Code Analyzer application locally.
The app will be available at http://localhost:8501/

Usage:
    python run_app.py

Or directly with Streamlit:
    streamlit run matrix_final.py
"""

import subprocess
import sys
import os

def main():
    """Start the AI Code Analyzer application."""
    print("Starting AI Code Analyzer...")
    print("The app will be available at: http://localhost:8501/")
    print("Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        # Check if streamlit is installed
        subprocess.run([sys.executable, "-c", "import streamlit"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Streamlit is not installed. Please install it with:")
        print("   pip install streamlit")
        sys.exit(1)
    
    # Start the Streamlit app
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "matrix_final.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ], check=True)
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"Error starting application: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
