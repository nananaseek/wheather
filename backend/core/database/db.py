from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import AsyncAttrs

from core.settings import settings


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


engine = create_async_engine(settings.get_db_url(), echo=True, future=True)
AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

