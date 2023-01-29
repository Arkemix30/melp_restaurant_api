from enum import Enum
from typing import Optional

from fastapi import status
from pydantic import BaseModel


class ErrorType(Enum):
    BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    NOT_FOUND = status.HTTP_404_NOT_FOUND
    DATASOURCE_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR
    INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR


class AppError(BaseModel):
    error_type: ErrorType
    message: Optional[str]

    class Config:
        use_enum_values = True
