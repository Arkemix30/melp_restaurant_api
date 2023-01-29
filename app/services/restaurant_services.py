# isort:skip_file
from typing import Union

import pandas as pd
from fastapi import Depends, UploadFile
from fastapi.encoders import jsonable_encoder

from app.core import get_logger
from app.models.restaurant import Restaurant
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas import RestaurantCountResponse, RestaurantCreate, RestaurantUpdate
from app.utils.errors import AppError, ErrorType

logger = get_logger(__name__)

# This is the service layer, it is responsible for business logic
# and it is the only layer that can communicate with the repository layer
# and the models layer.


class RestaurantService:
    def __init__(self, restaurant_repository: RestaurantRepository = Depends()):
        self.restaurant_repository = restaurant_repository

    def get(self, id: int) -> Union[Restaurant, AppError]:
        restaurant = self.restaurant_repository.get(id)
        if not restaurant:
            logger.error(f"Restaurant not found with id: {id}")
            return None
        return restaurant

    def get_all(self) -> list[Restaurant]:
        return self.restaurant_repository.get_all()

    def create(self, restaurant: RestaurantCreate) -> Union[Restaurant, AppError]:
        restaurant = Restaurant(**restaurant.dict())
        return self.restaurant_repository.create(restaurant)

    def bulk_create(self, restaurants: list[RestaurantCreate]) -> bool:
        restaurants = [Restaurant(**restaurant.dict()) for restaurant in restaurants]
        return self.restaurant_repository.bulk_create(restaurants)

    def bulk_create_from_csv(self, csv_file: UploadFile) -> Union[bool, AppError]:
        try:
            df = pd.read_csv(csv_file.file)
            restaurants = df.to_dict(orient="records")
        except Exception as err:
            logger.error(f"Error while reading csv file, error: {err}")
            return AppError(
                error_type=ErrorType.INTERNAL_SERVER_ERROR,
                message="Error while reading csv file",
            )
        try:
            restaurants = [Restaurant(**restaurant) for restaurant in restaurants]
        except Exception as err:
            logger.error(f"Error while parsing csv file, error: {err}")
            return AppError(
                error_type=ErrorType.BAD_REQUEST,
                message="Error while parsing csv file, please check all fields",
            )
        return self.restaurant_repository.bulk_create(restaurants)

    def update(self, id: int, restaurant: RestaurantUpdate) -> Restaurant:
        restaurant_in_db = self.restaurant_repository.get(id)

        if not restaurant_in_db:
            return AppError(
                error_type=ErrorType.NOT_FOUND, message="Restaurant not found"
            )

        obj_data = jsonable_encoder(restaurant_in_db)
        if isinstance(restaurant, dict):
            update_data = restaurant
        else:
            update_data = restaurant.dict(exclude_unset=True)

        # This is an iterator over the fields of the model to be updated
        for field in obj_data:
            if field in update_data:
                setattr(restaurant_in_db, field, update_data[field])

        return self.restaurant_repository.update(restaurant_in_db)

    def delete(self, id: str) -> Restaurant:
        restaurant_in_db = self.restaurant_repository.get(id)

        if isinstance(restaurant_in_db, AppError):
            return restaurant_in_db

        if not restaurant_in_db:
            return AppError(
                error_type=ErrorType.NOT_FOUND, message="Restaurant not found"
            )

        return self.restaurant_repository.delete(restaurant_in_db)

    def count_restaurants_by_radius(
        self, lat: float, lng: float, radius: int
    ) -> RestaurantCountResponse:
        result = self.restaurant_repository.get_near_restaurants_by_radius(
            lat, lng, radius
        )
        if isinstance(result, AppError):
            return result

        count = result["count"]
        avg = result["avg"]
        std = result["std"]
        return RestaurantCountResponse(count=count, avg=avg, std=std)
