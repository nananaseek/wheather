import asyncio
import logging

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session

from schemas.city import CitySchema, CityGetSchema
from services.city import CityService
from services.open_weather_api import OpenWeather
from services.weather import WeatherService
from tasks.task import create_weather

logger = logging.getLogger(__name__)

city_router = APIRouter(tags=["city"])


@city_router.post("/create-city", description="Create city by name")
async def get_geo(
        city: str,
        session: AsyncSession = Depends(get_session),
        parser: OpenWeather = Depends(OpenWeather)
) -> CitySchema:
    try:
            is_city = await CityService.get_city_by_name(session=session, name=city)
            logger.info(f"Is city: {is_city}")
            if is_city:
                if str(is_city.name).lower() == city.lower():
                    msg = "City with this name already in database"
                    logger.error(msg)
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)


            city_data = await parser.get_geo(city=city)

            if not city_data:
                logger.error(f"Can`t take {city} coordinates")
                raise HTTPException(status_code=500, detail='Can`t pars coordinates')

            result = await CityService.create(
                session=session, data=city_data.model_dump()
            )

            create_weather.delay(result.id)

            return CitySchema.model_validate(result)


    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@city_router.get('/get-all-city', description='get list of all city')
async def get_all_city(
        session : AsyncSession = Depends(get_session)
) -> list[CityGetSchema]:
    try:
        raw_city_list = await CityService.get_cities(session=session)
        result = []
        for city in raw_city_list:
            weather = city.weather
            while weather is None:
                logger.warning("Weather for city is not ready! Whaiting...")
                await asyncio.sleep(0.5)
                weather = await WeatherService.get_weather(session=session, city_id=city.id)
                
            result.append(CityGetSchema(id=city.id, name=city.name, weather=weather))
        
        return result
    except Exception as e:
        logger.error(f"Error in get all city: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@city_router.delete('/delete-city-id/', description='Delete object by id')
async def delete_city(
        city_id: int,
        session: AsyncSession = Depends(get_session)
) -> bool:
    try:
        await CityService.delete(id=city_id, session=session)
        return True
    except Exception as e:
        logger.error(f'Error in delete city {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))