from domains.website.models import AppConfig
import yaml

def load_config(path: str = "config.yml") -> AppConfig:
  with open(path) as file:
    parsed_yaml = yaml.safe_load(file)
    return AppConfig(**parsed_yaml)
