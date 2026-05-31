from pydantic import BaseModel, ConfigDict


class CitySchema(BaseModel):
    name: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)


class CityGetSchema(BaseModel):
    id: int
    name: str

class CityCreateSchema(CitySchema):
    pass