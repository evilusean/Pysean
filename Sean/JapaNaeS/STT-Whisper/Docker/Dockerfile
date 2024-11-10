# Use NVIDIA CUDA base image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3.9-distutils \
    python3-pip \
    ffmpeg \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --no-cache-dir \
    torch==2.0.1 \
    torchaudio==2.0.2 \
    numpy==1.24.3 \
    openai-whisper==20230918 \
    pykakasi==2.2.1 \
    transformers==4.31.0 \
    sentencepiece==0.1.99 \
    fugashi==1.2.1 \
    ipadic==1.0.0 \
    unidic-lite==1.0.8

# Create necessary directories
RUN mkdir -p /app/recordings /app/output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Volume mounting points
VOLUME ["/app/src", "/app/recordings", "/app/output"]

# Default command (can be overridden)
CMD ["python3", "-u", "/app/src/main.py"]