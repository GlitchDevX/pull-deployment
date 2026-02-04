import yaml
from functools import lru_cache

from frozendict import frozendict
from frozendict.cool import deepfreeze
from pydantic import ValidationError
from fastapi.exceptions import HTTPException

from domains.shared.logger import logger
from domains.website.models import AppConfig


def load_config(path: str = "config/config.yml") -> AppConfig:
    parsed_yaml = _load_yaml(path)
    return _parse_config(path, parsed_yaml)

@lru_cache
def _parse_config(path: str, content: frozendict) -> AppConfig:
    try:
        return AppConfig(**content)
    except (ValidationError, TypeError) as err:
        _load_yaml.cache_clear()
        logger.error(f"Config at '{path}' is invalid.\n{str(err)}")
        raise HTTPException(
            status_code=500,
            detail="Could not load deployment config. See application logs for details"
        )


@lru_cache
def _load_yaml(path: str) -> frozendict:
    print("called fs read")
    with open(path) as file:
        return deepfreeze(yaml.safe_load(file))
