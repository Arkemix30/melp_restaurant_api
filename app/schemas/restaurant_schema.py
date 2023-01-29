from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class RestaurantBase(BaseModel):
    id: Optional[str]
    rating: Optional[int]
    name: Optional[str]
    site: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    street: Optional[str]
    city: Optional[str]
    state: Optional[str]
    lat: Optional[float]
    lng: Optional[float]

    # Custom validator to check if rating is between 0 and 4
    @validator("rating")
    def rating_must_be_between_0_and_4(cls, v):
        if not 0 <= v <= 4:
            raise ValueError("Rating must be between 0 and 4")
        return v


# Properties to receive on Restaurant creation, we make them required
class RestaurantCreate(RestaurantBase):
    rating: int
    name: str
    site: str
    email: EmailStr
    phone: str
    street: str
    city: str
    state: str
    lat: float
    lng: float


# Properties to receive on Restaurant update, we make them optional
# because we don't want to force the user to update all fields
class RestaurantUpdate(RestaurantBase):
    pass


# Class to return the response of restaurant in a radius
class RestaurantCountResponse(BaseModel):
    count: int
    avg: float
    std: float


class RestaurantInDBBase(RestaurantBase):
    id: Optional[str]
    created_at: Optional[dt]
    updated_at: Optional[dt]

    class Config:
        orm_mode = True


class Restaurant(RestaurantInDBBase):
    pass
