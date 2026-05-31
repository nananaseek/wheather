from pydantic import BaseModel


class GeoApiResponse(BaseModel):
    name: str
    local_names: dict[str, str] | None = None
    lat: float
    lon: float
    country: str
    state: str | None = None


class GeoApiResponseList(BaseModel):
    results: list[GeoApiResponse]
