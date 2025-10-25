FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Force rebuild from this point - Fix permission error (2025-10-25)
# Copy application code (matrix_final.py uses /tmp for cache - no permission issues)
COPY analyzer/ ./analyzer/
COPY matrix_final.py .
COPY run_app.py .
COPY evaluation_samples/ ./evaluation_samples/

# Expose HuggingFace Spaces default port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:7860/_stcore/health || exit 1

# Run Streamlit with HF Spaces compatible settings
CMD ["streamlit", "run", "matrix_final.py", \
     "--server.port=7860", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false", \
     "--browser.gatherUsageStats=false"]

