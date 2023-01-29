from typing import Any, Optional

from pydantic import validator

from app.core.settings.app_settings import AppConfig


class DevConfig(AppConfig):
    debug: bool = True
    DEV_DATABASE_NAME: str
    DEV_DATABASE_USER: str
    DEV_DATABASE_PASSWORD: str
    DEV_DATABASE_HOST: str
    DEV_DATABASE_PORT: str

    DATABASE_URI: Optional[str] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        db_name = values.get("DEV_DATABASE_NAME")
        db_user = values.get("DEV_DATABASE_USER")
        db_password = values.get("DEV_DATABASE_PASSWORD")
        db_host = values.get("DEV_DATABASE_HOST")
        db_port = values.get("DEV_DATABASE_PORT")
        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
