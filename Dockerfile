# ============================================
# GeoAI Backend — Hugging Face Spaces Dockerfile
# ============================================
# SDK: docker  |  Port: 7860

FROM python:3.10-slim

# Reduce TensorFlow noise
ENV TF_CPP_MIN_LOG_LEVEL=2
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Increase pip timeout & retries to prevent download failures
ENV PIP_DEFAULT_TIMEOUT=1000
ENV PIP_RETRIES=5

WORKDIR /app

# Install dependencies first (cached layer)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir \
    --default-timeout=1000 \
    --retries 5 \
    -r requirements.txt

# Copy backend code + model
COPY backend/ .

# Expose HF Spaces default port
EXPOSE 7860

# Start FastAPI via uvicorn
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-10000}
