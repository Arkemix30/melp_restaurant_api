# isort: skip_file
import json

from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile, status

from app.core import get_logger
from app.models import Restaurant
from app.schemas import RestaurantCountResponse, RestaurantCreate, RestaurantUpdate
from app.services.restaurant_services import RestaurantService
from app.utils.errors import AppError

logger = get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=list[Restaurant])
async def get_all_restaurants(
    restaurant_service: RestaurantService = Depends(),
) -> list[Restaurant]:
    return restaurant_service.get_all()


@router.get("/statistics", response_model=RestaurantCountResponse, tags=["statistics"])
async def count_restaurants_by_radius(
    latitude: float,
    longitude: float,
    radius: int,
    restaurant_service: RestaurantService = Depends(),
) -> RestaurantCountResponse:
    result = restaurant_service.count_restaurants_by_radius(latitude, longitude, radius)

    if isinstance(result, AppError):
        raise HTTPException(detail=result.message, status_code=result.error_type)

    return result


@router.get("/{id}", response_model=Restaurant)
async def get_restaurant_by_id(
    id: str,
    restaurant_service: RestaurantService = Depends(),
) -> Restaurant:
    restaurant = restaurant_service.get(id)
    if restaurant:
        return restaurant
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found"
        )


@router.post("/", response_model=Restaurant)
async def create_restaurant(
    restaurant: RestaurantCreate,
    restaurant_service: RestaurantService = Depends(),
) -> Restaurant:
    result = restaurant_service.create(restaurant)
    if isinstance(result, AppError):
        raise HTTPException(detail=result.message, status_code=result.error_type)

    return result


@router.post("/bulk_create")
async def bulk_create_restaurants(
    restaurants: list[RestaurantCreate],
    restaurant_service: RestaurantService = Depends(),
) -> Response:

    result = restaurant_service.bulk_create(restaurants)
    if isinstance(result, AppError):
        raise HTTPException(detail=result.message, status_code=result.error_type)

    return Response(
        content=json.dumps({"data": "Restaurants created succesfully"}),
        status_code=201,
        headers={"Content-Type": "application/json"},
    )


@router.post("/bulk_create_from_csv")
async def bulk_create_restaurants_from_csv(
    csv_file: UploadFile,
    restaurant_service: RestaurantService = Depends(),
) -> Response:
    result = restaurant_service.bulk_create_from_csv(csv_file)
    if isinstance(result, AppError):
        raise HTTPException(detail=result.message, status_code=result.error_type)

    return Response(
        content=json.dumps({"data": "Restaurants created succesfully"}),
        status_code=201,
        headers={"Content-Type": "application/json"},
    )


@router.put("/{id}", response_model=Restaurant)
async def update_restaurant(
    id: str,
    restaurant: RestaurantUpdate,
    restaurant_service: RestaurantService = Depends(),
) -> Restaurant:
    result = restaurant_service.update(id, restaurant)

    if isinstance(result, AppError):
        raise HTTPException(detail=result.message, status_code=result.error_type)

    return result


@router.delete("/{id}")
async def delete_restaurant(
    id: str,
    restaurant_service: RestaurantService = Depends(),
) -> Restaurant:
    result = restaurant_service.delete(id)

    if isinstance(result, AppError):
        raise HTTPException(detail=result.message, status_code=result.error_type)

    return Response(
        content=json.dumps({"data": "Restaurant deleted succesfully"}),
        status_code=200,
        headers={"Content-Type": "application/json"},
    )
