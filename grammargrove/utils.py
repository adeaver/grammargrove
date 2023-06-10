import os

from enum import Enum

class Environment(Enum):
    Dev = 'dev'
    Prod = 'prod'

def get_environment() -> Environment:
    return Environment(os.environ.get("ENV", "dev"))

def get_base_url_for_environment() -> str:
    env = get_environment()
    if env == Environment.Dev:
        return "http://localhost:8000"
    elif env == Environment.Prod:
        return "https://www.grammargrove.com"
    else:
        raise ValueError(f"{env.value} has no url")
