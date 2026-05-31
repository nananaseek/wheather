from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func

from core.database.db import Base


class Weather(Base):
    __tablename__ = "weather"

    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    city: Mapped["City"] = relationship("City", back_populates="weather", uselist=False)
    temperature: Mapped[float]
    temp_feels_like: Mapped[float]
    temp_min: Mapped[float]
    temp_max: Mapped[float]
    visibility: Mapped[float]
    dt: Mapped[datetime]
    country: Mapped[str]
    sunrise: Mapped[datetime]
    sunset: Mapped[datetime]
    humidity: Mapped[float]
    timezone: Mapped[str]
    name: Mapped[str]
    rain: Mapped[int]
    clouds: Mapped[int]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now)


class City(Base):
    __tablename__ = "cities"
    name: Mapped[str] = mapped_column(String, unique=True)
    latitude: Mapped[float]
    longitude: Mapped[float]

    weather: Mapped[list["Weather"]] = relationship(
        "Weather", back_populates="city", cascade="all, delete-orphan", uselist=False
    )
