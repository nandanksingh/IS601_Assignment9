# ----------------------------------------------------------
# Author: Nandan Kumar
# Date: 11/03/2025
# Assignment-9: Working with Raw SQL in pgAdmin
# File: Dockerfile
# ----------------------------------------------------------
# Description:
# Production-grade Dockerfile for FastAPI + PostgreSQL integration.
# Optimized for Docker Compose and CI/CD pipelines.
# ----------------------------------------------------------

FROM python:3.12-slim

# ----------------------------------------------------------
# Environment configuration
# ----------------------------------------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:$PATH"

WORKDIR /app

# ----------------------------------------------------------
# Install minimal system dependencies
# Includes curl (for healthcheck) and libpq for psycopg2
# ----------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl && \
    rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------------
# Create a non-root user for security
# ----------------------------------------------------------
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# ----------------------------------------------------------
# Install Python dependencies
# ----------------------------------------------------------
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------------
# Copy application code
# ----------------------------------------------------------
COPY . .

# ----------------------------------------------------------
# Set ownership and switch user
# ----------------------------------------------------------
RUN chown -R appuser:appgroup /app
USER appuser

# ----------------------------------------------------------
# Expose port and add healthcheck
# ----------------------------------------------------------
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# ----------------------------------------------------------
# Default run command
# ----------------------------------------------------------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
