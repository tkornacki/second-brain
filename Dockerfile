# Use an official lightweight base image
FROM ubuntu:22.04

ARG MODEL_NAME

ENV DEBIAN_FRONTEND=noninteractive
ENV MODEL_NAME=${MODEL_NAME}

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ollama.ai/install.sh | bash

EXPOSE 11434

CMD OLLAMA_HOST=0.0.0.0 ollama serve & \
    until curl -s http://localhost:11434/api/tags | grep -q 'models'; do sleep 2; done && \
    ollama pull ${MODEL_NAME} && \
    wait
