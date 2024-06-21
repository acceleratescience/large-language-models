FROM python:latest
LABEL container="large-language-models"
LABEL maintainer="Ryan Daniels"
LABEL version="0.1.0"
LABEL description="Dockerfile for llm workshop run by accelerate science."

WORKDIR /workspace

COPY . /workspace

# Install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    pip install --no-cache-dir -r requirements.txt