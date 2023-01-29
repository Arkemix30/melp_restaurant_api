# Python Imports
from typing import Union

# Third Party Imports
from fastapi import Depends
from sqlalchemy import func
from sqlmodel import Session, select

# Local Imports
from app.core import get_logger
from app.infrastructure import get_db_session
from app.models import Restaurant
from app.utils.errors import AppError, ErrorType

logger = get_logger(__name__)


class RestaurantRepository:
    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    def get(self, id: str) -> Union[Restaurant, None, AppError]:
        """
        Get a restaurant by id

        Parameters
        ----------
        `id` : str
            The id of the restaurant to get

        Returns
        -------
        `Union[Restaurant, None, AppError]`
            The restaurant if found, otherwise an AppError
        """
        try:
            statement = select(Restaurant).where(Restaurant.id == id)
            return self.session.exec(statement).first()
        except Exception as err:
            error_msg = "Error when fetching restaurant with id: {id}"
            logger.error(f"{error_msg}, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error when fetching restaurant",
            )

    def get_all(self) -> Union[list[Restaurant], AppError]:
        """
        Get all restaurants

        Returns
        -------
        `Union[list[Restaurant], AppError]`
            A list of restaurants if found, otherwise an AppError
        """
        statement = select(Restaurant)
        try:
            return self.session.exec(statement).fetchall()
        except Exception as err:
            error_msg = "Error while fetching all restaurants"
            logger.error(f"{error_msg}, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while fetching all restaurants",
            )

    def create(self, restaurant: Restaurant) -> Union[Restaurant, AppError]:
        """
        Create a restaurant

        Parameters
        ----------
        `restaurant` : Restaurant
            The restaurant to create

        Returns
        -------
        `Union[Restaurant, AppError]`
            The created restaurant if successful, otherwise an AppError
        """

        try:
            self.session.add(restaurant)
            self.session.commit()
            self.session.refresh(restaurant)
            return restaurant
        except Exception as err:
            error_msg = "Error while creating restaurant"
            logger.error(f"{error_msg}, error: {err}")
            self.session.rollback()
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while creating restaurant",
            )

    def bulk_create(self, restaurants: list[Restaurant]) -> Union[bool, AppError]:
        """
        Create multiple restaurants

        Parameters
        ----------
        `restaurants` : list[Restaurant]
            The restaurants to create

        Returns
        -------
        `Union[bool, AppError]`
            True if successful, otherwise an AppError
        """

        try:
            self.session.add_all(restaurants)
            self.session.commit()
            return True
        except Exception as err:
            error_msg = "Error while creating restaurants"
            logger.error(f"{error_msg}, error: {err}")
            self.session.rollback()
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while creating restaurants",
            )

    def update(self, restaurant: Restaurant) -> Union[Restaurant, AppError]:
        try:
            self.session.add(restaurant)
            self.session.commit()
            self.session.refresh(restaurant)
        except Exception as err:
            error_msg = "Error while updating restaurant"
            logger.error(f"{error_msg}, error: {err}")
            self.session.rollback()
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while updating restaurant",
            )
        return restaurant

    def delete(self, restaurant: Restaurant) -> Union[bool, AppError]:
        if not restaurant:
            return AppError(
                error_type=ErrorType.NOT_FOUND, message="Restaurant not found"
            )

        try:
            self.session.delete(restaurant)
            self.session.commit()
            return True
        except Exception as err:
            error_msg = "Error while deleting restaurant"
            logger.error(f"{error_msg}, error: {err}")
            self.session.rollback()
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while deleting restaurant",
            )

    # Specific Use Case Method
    def get_near_restaurants_by_radius(
        self, incoming_lat: float, incoming_lng: float, incoming_radius: float
    ) -> list[Restaurant]:
        """
        Retrieves a restaurant object from the `Restaurant`
        table whose coordinates are within the specified distance
        from the given incoming latitude and longitude.

        Parameters
        ----------
        `incoming_lat` : float
            The latitude of the incoming request.
        `incoming_lng` : float
            The longitude of the incoming request.
        `incoming_radius` : float
            The radius of the incoming request.

        Returns
        -------
        `result`: dict
            { "count": int, "avg": float, "std": float }

        """

        # The query is basically a SQL query that uses the
        # PostGIS extension to calculate the distance between two points
        # and then filters the results based on the distance.

        statement = select(
            func.count(Restaurant.id).label("count"),
            func.avg(Restaurant.rating).label("avg"),
            func.stddev(Restaurant.rating).label("std"),
        ).where(
            func.ST_DWithin(
                func.ST_Transform(
                    func.ST_SetSRID(
                        func.ST_MakePoint(Restaurant.lng, Restaurant.lat),
                        4326,
                    ),
                    3857,
                ),
                func.ST_Transform(
                    func.ST_SetSRID(func.ST_MakePoint(incoming_lng, incoming_lat), 4326),
                    3857,
                ),
                incoming_radius,
            )
        )

        try:
            result = self.session.exec(statement).fetchone()
        except Exception as err:
            error_msg = "Error while fetching all restaurants withing a radius"
            logger.error(f"{error_msg}, error: {err}")
            return AppError(error_type=ErrorType.DATASOURCE_ERROR, message=error_msg)

        if not result:
            return {
                "count": 0,
                "avg": 0,
                "std": 0,
            }

        return {
            "count": result["count"] if result["count"] else 0,
            "avg": result["avg"] if result["avg"] else 0,
            "std": result["std"] if result["std"] else 0,
        }
