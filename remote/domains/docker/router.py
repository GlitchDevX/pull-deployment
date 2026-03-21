from fastapi_limiter.depends import RateLimiter
from pyrate_limiter import Limiter, Rate, Duration

from fastapi import APIRouter, Depends

from domains.docker.internal.config import load_config
from domains.docker.internal.models import DockerBody

router = APIRouter()
config = load_config()

@router.put(
  "/deploy-docker-compose",
  dependencies=[Depends(RateLimiter(
    limiter=Limiter(
      Rate(
        config.rate_limit.amount,
        config.rate_limit.interval_minutes * Duration.MINUTE
      )
    )
  ))],
)
def deploy_docker_endpoint(body: DockerBody):
  return deploy_docker_compose(body)
