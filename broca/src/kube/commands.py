from utils.shell_commands import run_cmd
import subprocess
import json

def get_current_context():
    """Retrieve the current Kubernetes context."""
    try:
        context = run_cmd(["kubectl", "config", "current-context"])
        return context.strip()
    except subprocess.CalledProcessError as e:
        print("Error retrieving Kubernetes context:", e)
        return None
    
def get_namespaces():
    """Fetch the list of Kubernetes namespaces as JSON."""
    try:
        namespaces = run_cmd(["kubectl", "get", "namespaces", "-o", "json"])
        return json.loads(namespaces)["items"]
    except subprocess.CalledProcessError as e:
        print("Error retrieving namespaces:", e)
        return None
