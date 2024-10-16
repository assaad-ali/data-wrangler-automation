import subprocess
import os
from modules.utils.logger import get_logger

logger = get_logger(__name__)

def run_command(command):
    """
    Run a shell command and return the result.
    """
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, shell=True
        )
        if result.returncode != 0:
            logger.error(f"Command failed: {command}\n{result.stderr}")
        else:
            logger.info(f"Command succeeded: {command}\n{result.stdout}")
        return result.returncode
    except Exception as e:
        logger.error(f"Exception running command: {command}\n{e}")
        return 1

def check_dvc_initialized():
    return os.path.isdir(".dvc")

def check_git_initialized():
    return os.path.isdir(".git")

def dvc_init():
    return run_command("dvc init")

def git_init():
    return run_command("git init")

def dvc_add(path):
    return run_command(f"dvc add {path}")

def git_add(path):
    return run_command(f"git add {path}")

def git_commit(message):
    return run_command(f'git commit -m "{message}"')

def dvc_push():
    return run_command("dvc push")

def dvc_pull():
    return run_command("dvc pull")

def git_push():
    return run_command("git push")

def git_pull():
    return run_command("git pull")

def configure_s3_remote(remote_name, bucket_name, region):
    """
    Configure S3 remote for DVC.
    """
    try:
        if dvc_remote_add(remote_name, f"s3://{bucket_name}") != 0:
            logger.error(f"Failed to add remote {remote_name}.")
            return False
        if dvc_remote_modify(remote_name, "endpointurl", f"https://s3.{region}.amazonaws.com") != 0:
            logger.error(f"Failed to modify remote {remote_name}.")
            return False
        logger.info(f"Configured S3 remote '{remote_name}' for bucket '{bucket_name}' in region '{region}'.")
        return True
    except Exception as e:
        logger.error(f"Failed to configure S3 remote: {e}")
        return False

def check_s3_configured(remote_name):
    try:
        result = run_command(f"dvc remote list | grep {remote_name}")
        if result != 0:
            logger.error(f"Remote {remote_name} is not configured.")
            return False
        logger.info(f"Remote {remote_name} is already configured.")
        return True
        
    except Exception as e:
        logger.error(f"Failed to check if S3 is configured: {e}")
        return False

def dvc_remote_add(remote_name, url):
    return run_command(f"dvc remote add -d {remote_name} {url}")

def dvc_remote_modify(remote_name, option, value):
    return run_command(f"dvc remote modify {remote_name} {option} {value}")

def check_gdrive_configured(remote_name):

    try:
        result = run_command(f"dvc remote list | grep {remote_name}")
        if result != 0:
            logger.info(f"Remote {remote_name} is not configured.")
            return False
    except Exception as e:
        logger.error(f"Error checking Google Drive configuration: {e}")
        return False

def setup_gdrive_remote(remote_name, folder_id):
    try:
        run_command(f"dvc remote add -d {remote_name} gdrive://{folder_id}")
        run_command(f"dvc remote modify {remote_name} gdrive_use_service_account true")

        logger.info("Google Drive remote setup complete.")

    except Exception as e:
        logger.error(f"Error setting up Google Drive remote: {e}")

def modify_gdrive_remote(remote_name, client_id, client_secret):
    try:
        run_command(f"dvc remote modify {remote_name} gdrive_client_id {client_id}")
        run_command(f"dvc remote modify {remote_name} gdrive_client_secret {client_secret}")

        logger.info("Google Drive remote modified with client ID and secret.")
        
    except Exception as e:
        logger.error(f"Error modifying Google Drive remote: {e}")
