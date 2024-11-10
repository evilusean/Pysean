FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set working directory
WORKDIR /app

# Set NVIDIA environment variables
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,video,utility

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-distutils \
    python3-pip \
    python3-dev \
    ffmpeg \
    portaudio19-dev \
    python3-pyaudio \
    git \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/data/audio/temp \
    /app/data/audio/saved \
    /app/data/output/transcripts \
    /app/data/output/translations

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Volume mounting points
VOLUME ["/app/src", "/app/data/audio", "/app/data/output"]

# Default command (can be overridden)
CMD ["python3", "-u", "/app/src/main.py"]