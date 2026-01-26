from fastapi.exceptions import HTTPException
from shutil import rmtree, copytree
import subprocess
from domains.website.models import Deployment
import tempfile

def pull_temp_branch(branch_name: str, deployment: Deployment):
  with tempfile.TemporaryDirectory() as tmp_dir:
    _pull_to_temp_dir(tmp_dir, branch_name, deployment)
    _copy_to_target_dir(tmp_dir, deployment.target_dir)

def _pull_to_temp_dir(tmp_dir: str, branch_name: str, deployment: Deployment):
  credentials_prefix = (f"{deployment.access_token}@" if deployment.access_token else "")
  clone_url = f"https://{credentials_prefix}{deployment.remote}"
  
  args = ["git", "clone", "-b", branch_name, "--depth", "1", clone_url, "."]
  result = subprocess.run(args, cwd=tmp_dir)
  
  if result.returncode != 0:
    raise HTTPException(status_code=404, detail="Temporary branch not found")
  
  rmtree(f"{tmp_dir}/.git", ignore_errors=True)

def _copy_to_target_dir(tmp_dir: str, target_dir: str):
  copytree(tmp_dir, target_dir, dirs_exist_ok=True)
