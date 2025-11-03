# ----------------------------------------------------------
# Author: Nandan Kumar
# Date: 10/27/2025
# Assignment-8: FastAPI Calculator
# File: Dockerfile
# ----------------------------------------------------------
# Description:
# Production-grade Dockerfile for FastAPI Calculator.
# Optimized for CI/CD pipelines (GitHub Actions + Trivy + Playwright).
# ----------------------------------------------------------

FROM python:3.12-slim

# Environment configuration
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# ----------------------------------------------------------
# Install system dependencies
# Includes build tools, curl (for healthcheck), and minimal fonts for Playwright
# ----------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libnss3 \
        fonts-liberation \
        libxkbcommon0 \
        libasound2 \
        libxss1 \
        libatk1.0-0 \
        libgtk-3-0 \
        libdrm2 \
        libgbm1 && \
    rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------------
# Create a non-root user for security
# ----------------------------------------------------------
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# ----------------------------------------------------------
# Copy dependency list first (for better build caching)
# ----------------------------------------------------------
COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------------
# Copy the rest of the application code
# ----------------------------------------------------------
COPY . .

# ----------------------------------------------------------
# Set permissions
# ----------------------------------------------------------
RUN chown -R appuser:appgroup /app
USER appuser

# ----------------------------------------------------------
# Expose app port and add health check
# ----------------------------------------------------------
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# ----------------------------------------------------------
# Default run command
# ----------------------------------------------------------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
