from fastapi.routing import APIRouter

from .open_weather import weather_router
from .app import city_router

main_router = APIRouter()

main_router.include_router(city_router)
main_router.include_router(weather_router)