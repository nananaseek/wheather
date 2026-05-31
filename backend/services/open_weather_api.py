from typing import Any, Coroutine

import httpx
import logging

from httpx import HTTPStatusError

from core.settings import settings
from schemas.city import CityCreateSchema
from schemas.open_weather import WeatherResponse
from schemas.open_weather import GeoApiResponseList


logger = logging.getLogger(__name__)

class OpenWeather:
    app_id = settings.OPEN_WEATHER_API_KEY

    async def get_geo(self, city: str) -> CityCreateSchema | None:
        url = "https://api.openweathermap.org/geo/1.0/direct"
        params = {"q": city, "limit": 1, "appid": self.app_id}

        try:
            logger.info(f'Start pars geo data for city {city}')
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)

                response.raise_for_status()

                result = response.json()

                return CityCreateSchema(**result[0])

        except HTTPStatusError as e:
            logger.error(f'Can`t get latitude and longitude for {city}: {e}', exc_info=True)

    async def get_weather(self, lat: float, lon: float, name: str):
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "units": "metric",
            "lang": "ua",
            "appid": self.app_id,
        }

        try:
            logger.info(f'Start pars weather for {name}')
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)

                response.raise_for_status()
                logger.info(response.json())

                return WeatherResponse(**response.json())
        except HTTPStatusError as e:
            logger.error(f'Cant pars weather for {name}: {e}', exc_info=True)