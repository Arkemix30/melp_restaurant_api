from typing import Any

from pydantic import SecretStr

from app.core.settings.base_settings import BaseConfig


class AppConfig(BaseConfig):
    debug: bool = False
    SECRET_KEY: SecretStr
    PROJECT_NAME: str = "Melp Restaurants API"
    API_V1_STR: str = "/api/v1"

    class Config:
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {"debug": self.debug}
