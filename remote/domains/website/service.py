from fastapi import HTTPException
from domains.website.git import pull_temp_branch
from domains.website.models import WebsiteResponse
from domains.website.config import load_config
from domains.website.models import Deployment
from domains.website.models import WebsiteBody

def deploy_website(inputs: WebsiteBody):
  deployment = get_deployment_by_id(inputs.deployment_id)

  if not deployment or deployment.secret != inputs.deployment_secret:
    raise HTTPException(status_code=403)
  
  pull_temp_branch(inputs.branch_name, deployment)

  return WebsiteResponse(result="success")


def get_deployment_by_id(deployment_id: str) -> Deployment | None:
  all_deployments = load_config().deployments

  return next((deployment for deployment in all_deployments if deployment.id == deployment_id), None)
