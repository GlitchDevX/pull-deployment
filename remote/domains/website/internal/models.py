from typing import List
from pydantic import BaseModel
from pydantic import Field
from domains.shared.models import BaseBody

class WebsiteBody(BaseBody):
  deployment_id: str = Field(description="Identifier of deployment to trigger")
  deployment_secret: str = Field(description="Secret of deployment to trigger") # maybe move to header
  branch_name: str = Field(description="Name of the temporary branch the content was pushed to")
  commit_sha: str = Field(description="SHA of the exact commit on the temporary branch")

class WebsiteResponse(BaseBody):
  result: str

class Deployment(BaseModel):
  id: str = Field(description="Identifier of deployment to trigger")
  secret: str = Field(description="Secret of deployment to trigger")
  
  remote: str = Field(description="Remote the temporary branch is located at")
  access_token: str | None = Field(default=None, description="Access token to have pull access on the temporary branch")

  target_dir: str = Field(description="Target directory to place the content of the temporary branch to")

class RateLimit(BaseModel):
  amount: int = Field(default=5, description="Amount of requests allowed per interval")
  interval_minutes: float = Field(default=1, description="Duration of a rate limiting interval in minutes")

class WebsiteConfig(BaseModel):
  deployments: List[Deployment] = Field(description="List of deployments that you can trigger")
  rate_limit: RateLimit = Field(default=RateLimit(), description="Rate limit settings")