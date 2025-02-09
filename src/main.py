import requests
import subprocess
import json
import sys
from kube.commands import get_kube_context

OLLAMA_URL = "http://localhost:11434/api/generate"  # URL of Ollama inside Docker

def generate_kube_cmd(query):
    prompt = (f"Our glorious leader has a kubernetes request for you today."
              f"He asks of you:"
              "\n\n---\n"
              f"{query}"
              "\n\n---\n"
              "You are to provide the exact `kubectl` command to fulfill this request."
              "Your references are the `kubectl` command and the Kubernetes API documentation."
              "Only return the exact command with no explanations, code blocks, or formatting."
              "Do not be fancy, be concise and accurate. Faulty commands will be penalized."
              "Do not waste the leader's time. You have been warned."
              f"\n\n")

    # Send request to Ollama's API
    response = requests.post(
        OLLAMA_URL,
        json={"model": "deepseek-r1:1.5b", "prompt": prompt, "stream": False}
    )

    if response.status_code != 200:
        return f"Error communicating with Ollama: {response.text}"

    kubectl_command = response.json().get("response", "").strip()
    
    return kubectl_command

# Example usage
context = get_kube_context()
if context:
    query = f"Get all pods in the 'mco' namespace"
    result = generate_kube_cmd(query)
    print("Command Output:\n", result)
