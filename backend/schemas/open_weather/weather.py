from pydantic import BaseModel


class Coord(BaseModel):
    lon: float
    lat: float


class WeatherItem(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class MainWeatherData(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: int | None = None
    grnd_level: int | None = None


class Wind(BaseModel):
    speed: float
    deg: int
    gust: float | None = None


class Rain(BaseModel):
    one_h: float | None = None


class Clouds(BaseModel):
    all: int


class Sys(BaseModel):
    type: int | None = None
    id: int | None = None
    country: str
    sunrise: int
    sunset: int


class WeatherResponse(BaseModel):
    coord: Coord
    weather: list[WeatherItem]
    base: str
    main: MainWeatherData
    visibility: int
    wind: Wind
    rain: Rain | None = None
    clouds: Clouds
    dt: int
    sys: Sys
    timezone: int
    id: int
    name: str
    cod: int
