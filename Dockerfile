# ==============================================================================
# Acme Corp Internal Knowledge Base Assistant — Production Dockerfile
# ==============================================================================
# Security Standards:
# 1. Base Image: Minimal official Debian-based Python slim image.
# 2. Non-Root Execution: Runs as unprivileged 'appuser' (UID 1000).
# 3. Zero Baked Secrets: Relies entirely on runtime environment variable injection.
# 4. Layer Caching: Dependencies installed prior to application code.
# ==============================================================================

FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered log output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

# Step 1: Install dependencies first (Docker caches this layer if requirements.txt is unchanged)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 2: Copy application source code and knowledge base policies
COPY src/ ./src/
COPY data/ ./data/

# Step 3: Enterprise Security Hardening (Run as non-root user)
# Create a dedicated system user and pre-create the Chroma directory with proper ownership
RUN useradd --create-home --shell /bin/bash appuser && \
    mkdir -p /app/chroma_db && \
    chown -R appuser:appuser /app

USER appuser

# Default runtime command: Launch the interactive CLI
CMD ["python", "-m", "kb_assistant.main"]
