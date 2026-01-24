from fastapi import HTTPException
from domains.website.models import Deployment
from domains.website.models import WebsiteBody

def deploy_website(inputs: WebsiteBody):
  deployment = get_deployment_by_id(inputs.deployment_id)

  if not deployment or deployment.deployment_secret != inputs.deployment_secret:
    raise HTTPException(status_code=403)


def get_deployment_by_id(deployment_id: str) -> Deployment | None:
  return Deployment(deployment_id="custos", deployment_secret="BAD_SECRET", access_token="")
