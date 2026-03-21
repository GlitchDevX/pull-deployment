from typing import List
from pydantic import BaseModel
from pydantic import Field
from domains.shared.models import BaseBody


class DockerBody(BaseBody):
    deployment_id: str = Field(description="Identifier of deployment to trigger")
    deployment_secret: str = Field(description="Secret of deployment to trigger")  # maybe move to header
    image_name: str = Field(description="Name of the docker image to pull")


class DockerResponse(BaseBody):
    result: str


class Deployment(BaseModel):
    id: str = Field(description="Identifier of deployment to trigger")
    secret: str = Field(description="Secret of deployment to trigger")

    # remote: str = Field(description="Remote the temporary branch is located at")

    access_token: str | None = Field(default=None,
                                     description="Access token to have pull access in the docker registry")
    target_dir: str = Field(description="Target directory to pull and restart the docker compose process")


class RateLimit(BaseModel):
    amount: int = Field(default=5, description="Amount of requests allowed per interval")
    interval_minutes: float = Field(default=1, description="Duration of a rate limiting interval in minutes")


class DockerConfig(BaseModel):
    deployments: List[Deployment] = Field(description="List of deployments that you can trigger")
    rate_limit: RateLimit = Field(default=RateLimit(), description="Rate limit settings")