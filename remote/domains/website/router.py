from fastapi_limiter.depends import RateLimiter
from pyrate_limiter import Limiter, Rate, Duration

from domains.website.internal.config import load_config
from domains.website.internal.service import deploy_website
from domains.website.internal.models import WebsiteBody
from fastapi import APIRouter, Depends

router = APIRouter()
config = load_config()

@router.put(
  "/deploy-website",
  dependencies=[Depends(RateLimiter(
    limiter=Limiter(
      Rate(
        config.rate_limit.amount,
        config.rate_limit.interval_minutes * Duration.MINUTE
      )
    )
  ))],
)
def deploy_website_endpoint(body: WebsiteBody):
  return deploy_website(body)
