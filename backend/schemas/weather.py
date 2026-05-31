from datetime import datetime
from pydantic import BaseModel


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
    rain: int
    clouds: int
    description: str
    

class WeatherCreateSchema(WeatherSchema):
    city_id: int


class WeatherGetSchema(WeatherSchema):
    id: int