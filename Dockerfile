# ─────────────────────────────────────────────────────────────────
#  Stage 1: Build dependencies (cached layer)
# ─────────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build tools needed for psycopg2 (if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ─────────────────────────────────────────────────────────────────
#  Stage 2: Runtime image (lean)
# ─────────────────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Runtime postgres client library only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy only the API source
COPY api/ ./api/

# Non-root user for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"

CMD ["uvicorn", "api.index:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
