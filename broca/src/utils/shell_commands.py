import shlex
import subprocess

def run_cmd(cmd:str|list[str])->str:
    if isinstance(cmd, list):
        cmd = " ".join(cmd)
    
    try:
        result = subprocess.run(
            shlex.split(cmd),  # Splits while respecting quotes
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr}"
