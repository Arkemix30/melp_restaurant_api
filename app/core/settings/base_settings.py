from enum import Enum

from pydantic import BaseSettings


class AppEnvTypes(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"


class BaseConfig(BaseSettings):
    ENVIRONMENT: AppEnvTypes

    class Config:
        env_file = ".env"
