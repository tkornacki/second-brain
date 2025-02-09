from src.ollama.requests import get_running_model, generate_kube_command
from src.utils.shell_commands import run_cmd

def main():
    print("Hello, Broca!")
    
    active_model = get_running_model()
    print(f"Running model: {active_model}")
    
    request = "Get all pods in the 'mco' namespace"
    response = generate_kube_command(active_model, request)
    
    print("Request:", request)
    print("Response:", response)
    
    # Prompt user for command execution
    user_input = input("Would you like to run the command? (y/n): ").strip().lower()
    if user_input == "y":
        print("Running command...")
        result = run_cmd(response)
        print("Command Output:\n", result)

if __name__ == "__main__":
    main()
