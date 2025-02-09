# Deepseek Ollama Container Setup

This repository provides setup instructions to deploy and run the **Deepseek Ollama** model with **Open WebUI** using a single `bash` script.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [NVIDIA GPU Drivers](https://docs.nvidia.com/datacenter/tesla/tesla-installation-notes/index.html) (for GPU acceleration)

## Quick Start

Run the following command to set up and start the container:

```sh
./run.sh -m <model>[:tag]
```

Supported models:

- `deepseek-r1`
- `llama3.1`

Optionally specify a model tag using `:` notation, e.g., `deepseek-r1:1.5b`.

### WebUI (Optional)

Enable WebUI by omitting `--disable-web-chat`:

```sh
./run.sh -m <model>
```

Disable WebUI:

```sh
./run.sh -m <model> --disable-web-chat
```

### Access Web Interface

Visit:

```
http://localhost:3000
```

## Container Overview

### Ollama Container (`second-brain-<model>`)

- **Base:** `ubuntu:22.04`
- **Port:** `11434`
- **Network:** `second-brain-net`
- **Restart Policy:** `always`
- **GPU Support:** Auto-detected

### Open WebUI Container (`open-webui`)

- **Base:** `ghcr.io/open-webui/open-webui:ollama`
- **Port:** `3000 (mapped to 8080 inside container)`
- **Env:** `OLLAMA_BASE_URL=http://localhost:11434`
- **Network:** `second-brain-net`
- **GPU Support:** Auto-detected

## Troubleshooting

### Check Running Containers

```sh
docker ps
```

Ensure `second-brain-<model>` and `open-webui` (if enabled) are running.

### Restart a Container

```sh
docker restart second-brain-<model> open-webui
```

### View Logs

```sh
docker logs second-brain-<model>
docker logs open-webui
```

### Remove and Rebuild

```sh
docker stop second-brain-<model> open-webui
docker rm second-brain-<model> open-webui
docker rmi second-brain-<model> open-webui
docker volume rm ollama open-webui
./run.sh -m <model>
```

## Author

Tristan
