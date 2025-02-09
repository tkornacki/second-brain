from src.ollama.requests import get_running_model, generate_kube_command
print("Hello, Broca!")
active_model=get_running_model()
print(f"Active model: {active_model}")

response = generate_kube_command(active_model, "Get all pods in the 'mco' namespace")
print("Command Output:\n", response)