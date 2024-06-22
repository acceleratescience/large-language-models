FROM ubuntu:22.04
LABEL container="large-language-models"
LABEL maintainer="Ryan Daniels"
LABEL version="0.2.0"
LABEL description="Dockerfile for llm workshop run by accelerate science."

WORKDIR /workspace

COPY . /workspace

# Install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git python3 python3-pip

RUN pip3 install -r requirements.txt