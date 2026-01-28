from fastapi.exceptions import HTTPException
from domains.shared.logger import logger
from pydantic import ValidationError
from domains.website.models import AppConfig
import yaml


def load_config(path: str = "config.yml") -> AppConfig:
    parsed_yaml = _load_yaml(path)
    try:
        return AppConfig(**parsed_yaml)
    except ValidationError as err:
        logger.error(f"Config at '{path}' is invalid.\n{str(err)}")
        raise HTTPException(
            status_code=500,
            detail="Could not load deployment config. See application logs for details"
        )


def _load_yaml(path: str):
    with open(path) as file:
        return yaml.safe_load(file)
