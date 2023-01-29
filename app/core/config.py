from functools import lru_cache
from typing import Type, Union

from app.core.settings.app_settings import AppConfig
from app.core.settings.base_settings import AppEnvTypes, BaseConfig
from app.core.settings.development_settings import DevConfig
from app.core.settings.production_settings import ProdConfig

environments: dict[AppEnvTypes, Type[AppConfig]] = {
    AppEnvTypes.dev: DevConfig,
    AppEnvTypes.prod: ProdConfig,
}


@lru_cache
def get_app_settings() -> Union[DevConfig, ProdConfig]:
    app_env = BaseConfig().ENVIRONMENT
    config = environments[app_env]
    return config()
