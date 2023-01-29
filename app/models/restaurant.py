from datetime import datetime as dt
from typing import Optional
from uuid import uuid4

from sqlalchemy import func
from sqlmodel import CheckConstraint, Column, DateTime, Field, SQLModel


class Restaurant(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)

    rating: int = Field(default=0, ge=0, le=4)
    name: str
    site: str
    email: str
    phone: str
    street: str
    city: str
    state: str
    lat: float
    lng: float

    created_at: Optional[dt] = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=True, server_default=func.now()
        )
    )
    updated_at: Optional[dt] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True, onupdate=func.now())
    )

    __table_args__ = (
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$'",
            name="valid_email",
        ),
    )
