from pydantic.v1.utils import to_lower_camel
from pydantic import ConfigDict
from pydantic import BaseModel

class BaseBody(BaseModel):
  model_config = ConfigDict(populate_by_name=True, alias_generator=to_lower_camel)