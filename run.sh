#!/usr/bin/env bash
set -e

NETWORK_NAME=ollama-net
CONTAINER_NAME=ollama-deepseek

echo "Beginning Deepseek."

# Confirm Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "Docker is not running. Exiting."
    exit 1
fi

# Detect if an NVIDIA GPU is available
if command -v nvidia-smi &>/dev/null; then
    GPU_ARGS="--gpus=all"
    echo "NVIDIA GPU detected, using GPU acceleration."
else
    GPU_ARGS=""
    echo "No NVIDIA GPU detected, running on CPU."
fi

# Ensure the Docker network exists before running any containers
if ! docker network inspect $NETWORK_NAME >/dev/null 2>&1; then
    echo "Creating network: $NETWORK_NAME"
    docker network create $NETWORK_NAME
fi

# Run the build script in the same directory as this script
pushd $(dirname $0) >/dev/null
docker build -t $CONTAINER_NAME . -f Dockerfile.deepseek-r1.1.5b
popd >/dev/null

# Run the Ollama container, explicitly assigning it to the network
if ! docker ps | grep -q $CONTAINER_NAME; then
    echo "Starting $CONTAINER_NAME container..."
    docker run -d --name $CONTAINER_NAME --network=$NETWORK_NAME \
        -p 11434:11434 --restart always $CONTAINER_NAME
fi

# Ensure Ollama container is running
if ! docker ps | grep -q $CONTAINER_NAME; then
    echo "$CONTAINER_NAME is not running. Check logs with: docker logs $CONTAINER_NAME"
    exit 1
fi

# Run Open WebUI container, ensuring it’s on the same network
if ! docker ps | grep -q open-webui; then
    echo "Starting Open WebUI container..."
    docker run -d -p 3000:8080 \
        $GPU_ARGS \
        -v ollama:/root/.ollama \
        -v open-webui:/app/backend/data \
        --name open-webui \
        --restart always \
        -e OLLAMA_BASE_URL=http://$CONTAINER_NAME:11434 \
        --network=$NETWORK_NAME \
        ghcr.io/open-webui/open-webui:ollama
fi

# Ensure Open WebUI container is running
if ! docker ps | grep -q open-webui; then
    echo "Container open-webui is not running. Check logs with: docker logs open-webui"
    exit 1
fi

echo "$CONTAINER_NAME and Open WebUI are running. Wait for ~10 seconds, then open your browser at http://localhost:3000"
