from pydantic import BaseModel, ConfigDict

from schemas.weather import WeatherSchema


class CitySchema(BaseModel):
    name: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)


class CityGetSchema(BaseModel):
    id: int
    name: str
    weather: WeatherSchema

class CityCreateSchema(CitySchema):
    pass