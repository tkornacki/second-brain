import requests
import subprocess
import json

OLLAMA_URL = "http://localhost:11434/api/generate"  # URL of Ollama inside Docker
# config.load_kube_config()
# v1 = client.CoreV1Api()

def run_kubectl_command(cmd):
    try:
        # security_comment: internal script for dev deployments.
        result = subprocess.run( # nosec
            cmd,
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e.stderr}", file=sys.stderr)
        sys.exit(e.returncode)
        
def get_kube_context():
    try:
        context = run_kubectl_command(["kubectl", "config", "current-context"])
        return context.strip()
    except subprocess.CalledProcessError as e:
        print("Error retrieving Kubernetes context:", e)
        return None


def ask_kubernetes(query):
    prompt = f"Can you run this command for me:\n\n{query}"

    # Send request to Ollama's API
    response = requests.post(
        OLLAMA_URL,
        json={"model": "deepseek-r1:1.5b", "prompt": prompt, "stream": False}
    )

    if response.status_code != 200:
        return f"Error communicating with Ollama: {response.text}"

    kubectl_command = response.json().get("response", "").strip()
    print(f"Generated Command: {kubectl_command}")

    try:
        output = subprocess.check_output(kubectl_command, shell=True, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e}"

# Example usage
context = get_kube_context()
# query = f"List all pods in the {context} context mco namespace"
query = "ls -lta"
result = ask_kubernetes(query)
# print("Command Output:\n", result)
