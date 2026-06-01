from datetime import datetime
from pydantic import BaseModel, field_validator, ConfigDict


class WeatherSchema(BaseModel):
    temperature: float
    temp_feels_like: float
    temp_min: float
    temp_max: float
    visibility: float
    dt: datetime
    country: str
    sunrise: datetime
    sunset: datetime
    humidity: float
    timezone: str
    name: str
    rain: float
    clouds: int
    description: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("timezone", mode="before")
    @classmethod
    def serialize_timezone(cls, value):
        if value is not None:
            return str(value)
        return value


class WeatherCreateSchema(WeatherSchema):
    city_id: int


class WeatherGetSchema(WeatherSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)