from typing import Any, Optional

from pydantic import validator

from app.core.settings.app_settings import AppConfig


class ProdConfig(AppConfig):
    PROD_DATABASE_NAME: str
    PROD_DATABASE_USER: str
    PROD_DATABASE_PASSWORD: str
    PROD_DATABASE_HOST: str
    PROD_DATABASE_PORT: str

    DATABASE_URI: Optional[str] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        db_name = values.get("PROD_DATABASE_NAME")
        db_user = values.get("PROD_DATABASE_USER")
        db_password = values.get("PROD_DATABASE_PASSWORD")
        db_host = values.get("PROD_DATABASE_HOST")
        db_port = values.get("PROD_DATABASE_PORT")
        return f"postgresql://" f"{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
