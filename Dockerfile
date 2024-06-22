FROM ubuntu:22.04
LABEL container="large-language-models"
LABEL maintainer="Ryan Daniels"
LABEL version="0.1.0"
LABEL description="Dockerfile for llm workshop run by accelerate science."

WORKDIR /workspace

COPY . /workspace
# Install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git python3 python3-pip && \
    pip install --no-cache-dir -r requirements.txt