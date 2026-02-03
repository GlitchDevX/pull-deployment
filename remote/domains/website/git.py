import tempfile
import subprocess
import shutil
from fastapi.exceptions import HTTPException
from domains.website.models import Deployment

def pull_temp_branch(branch_name: str, commit_sha: str, deployment: Deployment):
  with tempfile.TemporaryDirectory() as tmp_dir:
    _pull_to_temp_dir(tmp_dir, branch_name, commit_sha, deployment)
    _copy_to_target_dir(tmp_dir, deployment.target_dir)

def _pull_to_temp_dir(tmp_dir: str, branch_name: str, commit_sha: str, deployment: Deployment):
  credentials_prefix = (f"{deployment.access_token}@" if deployment.access_token else "")
  clone_url = f"https://{credentials_prefix}{deployment.remote}"
  
  clone_args = ["git", "clone", "--single-branch", "-b", branch_name, "--depth", "1", clone_url, "."]
  clone_result = subprocess.run(clone_args, cwd=tmp_dir)

  # checkout exact commit to ignore malicious commits the temp branch
  fetch_result = subprocess.run(["git", "fetch", "--depth", "1", "origin", commit_sha], cwd=tmp_dir)
  checkout_result = subprocess.run(["git", "checkout", commit_sha], cwd=tmp_dir)
  
  if clone_result.returncode != 0 or fetch_result.returncode != 0 or checkout_result.returncode != 0:
    raise HTTPException(status_code=404, detail="Temporary branch or commitSha not found")
  
  shutil.rmtree(f"{tmp_dir}/.git", ignore_errors=True)

def _copy_to_target_dir(tmp_dir: str, target_dir: str):
  shutil.copytree(f"{tmp_dir}/.temp-deployment", target_dir, dirs_exist_ok=True)
