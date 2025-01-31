# Deepseek Ollama Container Setup

This repository houses the setup steps necessary to deploy and run the **Deepseek Ollama** model along with **Open WebUI** for an interactive experience, in a single `bash` script.

## Prerequisites

Ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [NVIDIA GPU Drivers](https://docs.nvidia.com/datacenter/tesla/tesla-installation-notes/index.html) (if using GPUs)

## Installation & Setup

### 1. Build the Deepseek Ollama Container

Run the following command to build the Docker image:

```sh
./run.sh
```

This script will:

- Build a Docker image based on Ubuntu 22.04 with Ollama installed.
- Detect if an NVIDIA GPU is available and use GPU acceleration if applicable.
- Create a Docker network (`ollama-net`) if it does not exist.
- Start a container named `ollama-deepseek`.
- Run Open WebUI for an easy interface to interact with the model.

### 2. Access the Web Interface

Once the containers are up and running, open your browser and go to:

```
http://localhost:3000
```

This will allow you to interact with the Deepseek model using Open WebUI.

## Container Details

### Ollama Container (`ollama-deepseek`)

- **Base Image:** `ubuntu:22.04`
- **Ports Exposed:** `11434`
- **Runs on Network:** `ollama-net`
- **Persistent Restart:** `always`
- **Command Executed:** `ollama serve` with `deepseek-r1:1.5b` model preloaded.
- **GPU Support:** Automatically detected and enabled if an NVIDIA GPU is available.

### Open WebUI Container (`open-webui`)

- **Base Image:** `ghcr.io/open-webui/open-webui:ollama`
- **Ports Exposed:** `3000 (mapped to 8080 inside the container)`
- **Environment Variables:**
  - `OLLAMA_BASE_URL=http://ollama-deepseek:11434`
- **Runs on Network:** `ollama-net`
- **Persistent Restart:** `always`
- **GPU Support:** Enabled if an NVIDIA GPU is detected.

## Troubleshooting

### Check Running Containers

```sh
docker ps
```

Ensure both `ollama-deepseek` and `open-webui` are running.

Check if the model is present:

```sh
curl http://localhost:11434/api/tags
```

### Restart a Container

```sh
docker restart ollama-deepseek
```

```sh
docker restart open-webui
```

### View Logs

```sh
docker logs ollama-deepseek
```

```sh
docker logs open-webui
```

### Remove and Rebuild

If you encounter issues, you may need to remove existing containers, images, and volumes, then rebuild:

```sh
docker stop ollama-deepseek open-webui
docker rm ollama-deepseek open-webui
docker rmi ollama-deepseek open-webui
docker volume rm ollama-deepseek-data
./run.sh
```

## Author

Tristan
