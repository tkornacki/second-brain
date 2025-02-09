from src.utils.shell_commands import run_cmd
import os
def deploy_service_account(release_name="readonly-sa", namespace="default"):
    """
    Deploys an existing Helm chart from a specified directory.

    Args:
        chart_dir (str): Path to the Helm chart directory.
        release_name (str): Name of the Helm release.
        namespace (str): Kubernetes namespace to deploy the chart in.
    """
    cwd = os.getcwd()
    chart_dir = os.path.join(cwd, "helm")

    install_cmd = [
        "helm",
        "upgrade",
        "--install",
        release_name,
        chart_dir,
        "-n",
        namespace,
        "--dry-run",
        "--debug",
        ]
    print(f"🚀 Deploying Helm chart from: {chart_dir}")
    print(f"🔹 Running: {install_cmd}")

    try:
        results= run_cmd(install_cmd)
        print(results)
        print(f"🎉 Helm release '{release_name}' deployed successfully in namespace '{namespace}'!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error deploying Helm chart: {e}")
