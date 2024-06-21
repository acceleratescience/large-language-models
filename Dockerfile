FROM ubuntu:22.04
LABEL container="website-pages"
LABEL maintainer="Ryan Daniels"
LABEL version="0.3.0"
LABEL description="Dockerfile template for mkdocs material theme site for accelerate."

WORKDIR /workspace

COPY . /workspace

# Install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git python3 python3-pip

RUN pip3 install -r requirements.txt

EXPOSE 8080
CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8080"]