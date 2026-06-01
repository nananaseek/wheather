import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import City
from schemas.city import CityCreateSchema

from .base import BaseService


logger = logging.getLogger(__name__)


class CityService(BaseService):
    model = City
    create_schema = CityCreateSchema

    @classmethod
    async def get_cities(cls, session: AsyncSession):
        try:
            query = select(City).order_by(City.name)
            data = await session.execute(query)
            return data.scalars().all()
        except Exception as e:
            logger.error(f"Error getting cities: {e}")
            raise e

    @classmethod
    async def get_city_by_name(cls, session: AsyncSession, name: str):
        try:
            query = select(City).where(City.name == name)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting city by name: {e}")
            raise e

    @classmethod
    async def create_city(cls, session: AsyncSession, city: CityCreateSchema):
        try:
            new_city = City(**city.model_dump())
            session.add(new_city)
            await session.commit()
            await session.refresh(new_city)
            return new_city
        except Exception as e:
            logger.error(f"Error creating city: {e}")
            raise e
