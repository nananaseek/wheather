
import logging

import httpx

from core.settings import settings
from core.celery import AsyncTask, app
from core.database import AsyncSessionLocal
from schemas.weather import WeatherCreateSchema, WeatherSchema, WeatherGetSchema

from services.city import CityService
from services.open_weather_api import OpenWeather
from services.weather import WeatherService

logger = logging.getLogger(__name__)


@app.task(base=AsyncTask, name="create_weather")
async def create_weather(city_id: int):
    parser = OpenWeather()
    async with AsyncSessionLocal() as session:
        try:
            city = await CityService.get_by_id(session, city_id)
            if not city:
                logger.error(f"City not found: {city_id}")
                return False

            response = await parser.get_weather(
                lat=city.latitude,
                lon=city.longitude,
                name=city.name
            )

            weather_create_schema = WeatherCreateSchema(
                city_id=city_id,
                temperature=response.main.temp,
                temp_feels_like=response.main.feels_like,
                temp_min=response.main.temp_min,
                temp_max=response.main.temp_max,
                visibility=response.visibility,
                dt=response.dt,
                country=response.sys.country,
                sunrise=response.sys.sunrise,
                sunset=response.sys.sunset,
                humidity=response.main.humidity,
                timezone=response.timezone,
                name=response.name,
                rain=response.rain.one_h,
                clouds=response.clouds.all,
                description=response.weather[0].description
            )

            await WeatherService.create_weather(
                session=session,
                data=weather_create_schema.model_dump(),
            )

        except Exception as e:
            logger.error(f"Error in celery create weather: {str(e)}", exc_info=True)


@app.task(base=AsyncTask, name="update_weather")
async def update_weather(city_id: int):
    parser = OpenWeather()
    async with AsyncSessionLocal() as session:
        try:
            city = await CityService.get_by_id(session, city_id)
            if not city:
                logger.error(f"City not found: {city_id}")
                return False

            response = await parser.get_weather(
                lat=city.latitude,
                lon=city.longitude,
                name=city.name
            )

            weather_update_schema = WeatherSchema(
                temperature=response.main.temp,
                temp_feels_like=response.main.feels_like,
                temp_min=response.main.temp_min,
                temp_max=response.main.temp_max,
                visibility=response.visibility,
                dt=response.dt,
                country=response.sys.country,
                sunrise=response.sys.sunrise,
                sunset=response.sys.sunset,
                humidity=response.main.humidity,
                timezone=response.timezone,
                name=response.name,
                rain=response.rain.one_h,
                clouds=response.clouds.all,
                description=response.weather[0].description
            )

            updated_weather = await WeatherService.update_weather(
                session=session, city_id=city.id, data=weather_update_schema
            )

            result = WeatherGetSchema.model_validate(updated_weather)

            logger.info(f'Weather is updated, new data: {result}')
            return result

        except Exception as e:
            logger.error(f"Error in celery update task: {str(e)}", exc_info=True)
