from fastapi import APIRouter

from .routes.restaurant_routes import router as restaurant_routes

router = APIRouter()
router.include_router(restaurant_routes, prefix="/restaurants", tags=["restaurants"])
