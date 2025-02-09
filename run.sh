#!/usr/bin/env bash
set -eo pipefail
set +x

# Set the current working directory to the directory of the script
pushd "$(dirname "$0")" >/dev/null || exit

# The Dockerfiles folder contains the possible models.
# Read the dirs, and split the names on 'Dockerfile'
# to get the model names.
MODELS=($(ls -1 Dockerfiles | sed 's/Dockerfile\.//'))

MODEL=""
DISABLE_WEB_CHAT=true
NETWORK_NAME="second-brain-net"
CONTAINER_PORT=11434

print_help() {
    cat <<EOF
Usage: $0 -m <model> [--disable-web-chat]

Options:
    -m, --model         (required) Specify the model name, options: ${MODELS[@]}
    --disable-web-chat  Disable web chat (optional, default: enabled)

    -h, --help          Show this help message
EOF
    exit 1
}

[[ "$#" -eq 0 ]] && print_help
while [[ "$#" -gt 0 ]]; do
    case "$1" in
    -m | --model)
        if [[ -n "$2" && ! "$2" =~ ^- ]]; then
            [[ " ${MODELS[@]} " =~ " $2 " ]] || {
                echo "Error: Invalid model name: $2"
                print_help
            }
            MODEL="$2"
            shift
        else
            echo "Error: --model requires a value."
            print_help
        fi
        ;;
    --disable-web-chat)
        DISABLE_WEB_CHAT=true
        ;;
    -h | --help)
        print_help
        ;;
    *)
        echo "Unknown option: $1"
        print_help
        ;;
    esac
    shift
done

# Required arguments
[[ -z "$MODEL" ]] && echo "Missing required argument: --model" && print_help

cat <<EOF

##################################################
Input Parameters
##################################################

Model: ${MODEL}
Web Chat Enabled: ${DISABLE_WEB_CHAT}

EOF

popd >/dev/null || exit

OS=$(uname)
OS_VERSION=$(uname -r)
OS_ARCH=$(uname -m)
PROCESSOR=$(uname -p)
MEMORY=
cat <<EOF

##################################################
System Configuration
##################################################

OS: ${OS}
OS Version: ${OS_VERSION}
OS Architecture: ${OS_ARCH}
Processor: ${PROCESSOR}

EOF

# Detect if an NVIDIA GPU is available
if command -v nvidia-smi &>/dev/null; then
    GPU_ARGS="--gpus=all"
    echo "NVIDIA GPU detected, using GPU acceleration."
else
    GPU_ARGS=""
    echo "No NVIDIA GPU detected, running on CPU."
fi

# Replace any periods in the model name with hyphens
CONTAINER_NAME="second-brain-$MODEL"
OLLAMA_BASE_URL="http://localhost:$CONTAINER_PORT"

cat <<EOF

##################################################
Container Setup
##################################################
Container Name:     ${CONTAINER_NAME}
Container Port:     ${CONTAINER_PORT}
Ollama Base URL:    ${OLLAMA_BASE_URL}
EOF

# Confirm Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "Docker is not running. Exiting."
    exit 1
fi

# Ensure the Docker network exists before running any containers
if ! docker network inspect $NETWORK_NAME >/dev/null 2>&1; then
    echo "Creating network: $NETWORK_NAME"
    docker network create $NETWORK_NAME
fi

# If the image already exists, skip the build step
if docker images | grep -q $CONTAINER_NAME; then
    echo "$CONTAINER_NAME image already exists."
else
    # Build the Docker image, silently, unless there are errors
    pushd Dockerfiles >/dev/null || exit
    echo "Building Docker image: $MODEL"
    docker build -t $CONTAINER_NAME -f Dockerfile.$MODEL . 2>/dev/null
    popd >/dev/null || exit
fi

#TODO: Add ability to delete the container and recreate it. Use an input arg
if docker ps | grep -q $CONTAINER_NAME; then
    echo "$CONTAINER_NAME container is already running."
else
    echo "Starting $CONTAINER_NAME container..."
    docker run -d --name $CONTAINER_NAME \
        --network=$NETWORK_NAME \
        -p $CONTAINER_PORT:$CONTAINER_PORT \
        --restart always \
        $CONTAINER_NAME
fi

if [[ "$DISABLE_WEB_CHAT" == false ]]; then
    echo "Web Chat is enabled."
    if ! docker ps | grep -q open-webui; then
        echo "Starting Open WebUI container..."
        docker run -d -p 3000:8080 \
            $GPU_ARGS \
            -v ollama:/root/.ollama \
            -v open-webui:/app/backend/data \
            --name open-webui \
            --restart always \
            -e OLLAMA_BASE_URL=$OLLAMA_BASE_URL \
            --network=$NETWORK_NAME \
            ghcr.io/open-webui/open-webui:ollama
    fi
else
    # If the Open WebUI container is running, stop it
    if docker ps | grep -q open-webui; then
        echo "Stopping Open WebUI container..."
        docker stop open-webui
        docker rm open-webui
    fi
fi

# Perform a health check by requesting the root endpoint of the Ollama service
OLLAMA_HEALTH_CHECK=$(curl -s "$OLLAMA_BASE_URL")

# Check if the response contains "Ollama is running"
if ! echo "$OLLAMA_HEALTH_CHECK" | grep -q "Ollama is running"; then
    echo "ERROR: Ollama is not running."
    exit 1
else
    echo "Ollama is running successfully."
fi

# Get the list of models from the Ollama service
MODELS=$(curl -s "$OLLAMA_BASE_URL/api/tags" | jq -r '.models[].name')
if ! echo "$MODELS" | grep -q "$MODEL"; then
    echo "ERROR: Model $MODEL not found in Ollama."
    exit 1
fi
