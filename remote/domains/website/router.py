from domains.website.service import deploy_website
from domains.website.models import WebsiteBody
from fastapi import APIRouter

router = APIRouter()

@router.put("/deploy-website")
def deploy_website_endpoint(body: WebsiteBody):
  return deploy_website(body)