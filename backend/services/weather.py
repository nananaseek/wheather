import logging
from typing import Any, Coroutine

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from models import Weather
from schemas.weather import WeatherSchema, WeatherCreateSchema
from .base import BaseService


logger = logging.getLogger(__name__)

class WeatherService(BaseService):
    model = Weather

    @classmethod
    async def create_weather(
            cls,
            session: AsyncSession,
            data: WeatherCreateSchema
    ) -> Weather | None:
        try:
            weather = Weather(**data.model_dump())
            session.add(weather)
            await session.commit()
            await session.refresh(weather)
            return weather
        except Exception as e:
            logger.error(f'Error in creating weather: {e}', exc_info=True)
            await session.rollback()

    @classmethod
    async def get_weather(
            cls,
            session: AsyncSession,
            city_id: int
    ) -> list[Weather]:
        query = select(Weather).where(Weather.city_id == city_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def update_weather(
            cls,
            session: AsyncSession,
            data: WeatherSchema,
            city_id: int
    ) -> Weather | None:
        try:
            updated_weather = update(Weather).where(Weather.city_id == city_id).values(**data.model_dump()).returning(Weather)
            result = await session.execute(updated_weather)
            updated_weather_object = result.scalar_one()
            await session.commit()
            await session.refresh(updated_weather_object)
            return updated_weather_object
        except Exception as e:
            await session.rollback()
            logger.error(f"Error in update weather data {e}", exc_info=True)
