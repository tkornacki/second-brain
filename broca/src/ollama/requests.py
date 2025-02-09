import requests
from src.config.constants import OLLAMA_URL

PROMPT_CONSTRAINTS = """Our glorious leader has a Kubernetes request for you today.
You are to provide the exact `kubectl` command to fulfill this request.
Your references are the `kubectl` command and the Kubernetes API documentation.
Only return the exact command with no explanations, code blocks, or formatting.
Do not be fancy, be concise and accurate. Faulty commands will be penalized.
Do not waste the leader's time. You have been warned.
He asks of you:
"""

def generate_kube_command(active_model: str, query: str) -> str:
    """Generate a kubectl command based on the query."""
    print(f"Attempting to generate kubectl command for query: {query}")
    prompt = f"{PROMPT_CONSTRAINTS}\n---\n{query}\n---"
    response = requests.post(
        f"{OLLAMA_URL}/generate",
        json={"model": active_model, "prompt": prompt, "stream": False}
    )

    if response.status_code != 200:
        return f"Error communicating with Ollama: {response.text}"

    try:
        json_response = response.json()
        return json_response.get("response", "No valid response received.")
    
    except Exception as e:
        return f"Error parsing response: {str(e)}"

def get_running_model() -> str:
    """Get the currently running Ollama model."""
    response = requests.get(f"{OLLAMA_URL}/tags")

    if response.status_code != 200:
        raise Exception(f"Error fetching running model: {response.text}")

    json_response = response.json()
    models = json_response.get("models", [])

    if not models:
        raise Exception("No models found")

    return models[0].get("name", "Unknown model")
