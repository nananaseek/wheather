import logging

from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from services.weather import WeatherService
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from schemas.weather import WeatherSchema, WeatherGetSchema
from tasks.task import update_weather

logger = logging.getLogger(__name__)

weather_router = APIRouter(tags=["weather"])


@weather_router.get("/update-weather")
async def update_weather_request(
        city_id: int,
) -> WeatherGetSchema:
    try:
        result = update_weather.delay(city_id)
        try:
            return_value = result.get(timeout=10)
            logger.info(f"Weather is updated : {return_value}")
            return return_value
        except TimeoutError:
            logger.error("Data load to long...")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Too long...')
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@weather_router.get('/get_weather')
async def get_weather(
        city_id: int,
        session: AsyncSession = Depends(get_session)
) -> WeatherGetSchema:
    query = await WeatherService.get_weather(session=session, city_id=city_id)

    if (query is None) or (query == False):
        logger.warning("Can`t found weather for this city")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    weather = WeatherGetSchema.model_validate(query)
    
    return weather