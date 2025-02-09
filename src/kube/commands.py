from shell.commands import run_cmd
import subprocess
import json

def get_kube_context():
    try:
        context = run_cmd(["kubectl", "config", "current-context"])
        return context.strip()
    except subprocess.CalledProcessError as e:
        print("Error retrieving Kubernetes context:", e)
        return None
    
def get_namespaces():
    try:
        namespaces = run_cmd(["kubectl", "get", "namespaces"])
        return json.loads(namespaces)["items"]
    except subprocess.CalledProcessError as e:
        print("Error retrieving namespaces:", e)
        return None