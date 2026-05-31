import logging
from typing import Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Base

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=Base)


class BaseService:
    model: Type[ModelType]

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int):
        try:
            query = select(cls.model).where(cls.model.id == id)
            result = await session.execute(query)
            return result.scalar()
        except Exception as e:
            logger.error(f"Error getting city by id: {e}")
            raise e

    @classmethod
    async def get_all(cls, session: AsyncSession):
        try:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting all cities: {e}")
            raise e

    @classmethod
    async def create(cls, session: AsyncSession, data: dict):
        try:
            is_obj = select(cls.model)
            new_item = cls.model(**data)
            session.add(new_item)
            await session.commit()
            await session.refresh(new_item)
            return new_item
        except Exception as e:
            logger.error(f"Error creating item: {e}")
            raise e

    @classmethod
    async def delete(cls, session: AsyncSession, id: int):
        try:
            request = delete(cls.model).where(cls.model.id == id)
            await session.execute(request)
            await session.commit()
        except Exception as e:
            logger.error(f"Error in deleting object:{e}", exc_info=True)
            await session.rollback()
