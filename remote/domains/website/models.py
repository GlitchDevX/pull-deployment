from pydantic import BaseModel
from pydantic import Field
from domains.shared.models import BaseBody

class WebsiteBody(BaseBody):
  deployment_id: str = Field(description="Identifier of deployment to trigger")
  deployment_secret: str = Field(description="Secret of deployment to trigger") # maybe move to header
  branch_name: str = Field(description="Name of the temporary branch the content was pushed to")
  
  # thought here is to use the gh token in the action, but the downside would be an overpriviliged token because of required write permission
  access_token: str | None = Field(default=None, description="Access token to have pull access on the temporary branch")

class Deployment(BaseModel):
  deployment_id: str = Field(description="Identifier of deployment to trigger")
  deployment_secret: str = Field(description="Secret of deployment to trigger")
  access_token: str | None = Field(default=None, description="Access token to have pull access on the temporary branch")
