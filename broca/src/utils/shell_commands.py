import subprocess

def run_cmd(cmd):
    try:
        # Execute a command securely without using a shell
        result = subprocess.run(
            cmd,
            check=True,  # Raise an exception if the command fails
            shell=False,  # Prevent shell injection
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        # Return error message if command fails
        return f"An error occurred: {e.stderr}"
