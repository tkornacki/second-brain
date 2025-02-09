import subprocess

def run_cmd(cmd):
    try:
        # security_comment: internal script for dev deployments.
        result = subprocess.run(  # nosec
            cmd,
            check=True,
            shell=False,  # Prevent shell injection
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr}"