from fastapi.exceptions import HTTPException
from domains.shared.logger import logger
from pydantic import ValidationError
from domains.website.models import AppConfig
import yaml

def load_config(path: str = "config.yml") -> AppConfig:
  with open(path) as file:
    parsed_yaml = yaml.safe_load(file)
    try:
      return AppConfig(**parsed_yaml)
    except ValidationError as err:
      logger.error(f"Config at '{path}' is invalid.\n{str(err)}")
      raise HTTPException(status_code=500, detail="Could not load deployment config. See application logs for details")
