from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class WeatherApiBase(ABC, BaseModel):
    @abstractmethod
    def get_weather_from_lat_long(self, latitude: float, longitude: float) -> str:
        pass

    @abstractmethod
    async def get_weather_from_lat_long(self, latitude: float, longitude: float) -> str:
        pass

    @abstractmethod
    def get_weather_forecast_from_lat_long(self, city: str) -> str:
        pass

    @abstractmethod
    async def aget_weather_forecast_from_lat_long(self, city: str) -> str:
        pass

    @abstractmethod
    def get_air_pollution_from_lat_long(self, city: str) -> str:
        pass

    @abstractmethod
    async def aget_air_pollution_from_lat_long(self, city: str) -> str:
        pass

    @abstractmethod
    def get_coordinates_from_location_name(self, location_name: str) -> str:
        pass

    @abstractmethod
    async def aget_coordinates_from_location_name(self, location_name: str) -> str:
        pass

    @abstractmethod
    def format_response(self, response: Any) -> str:
        pass

    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs) -> "WeatherApiBase":
        pass


class Coord(BaseModel):
    lon: Optional[float] = None
    lat: Optional[float] = None


class Weather(BaseModel):
    id: Optional[int] = None
    weather_description: Optional[str] = Field(None, alias="main")
    description: Optional[str] = None


class Main(BaseModel):
    temp: Optional[float] = None
    feels_like: Optional[float] = None
    pressure: Optional[int] = None
    humidity: Optional[int] = None
    temp_min: Optional[float] = None
    temp_max: Optional[float] = None
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None

    @field_validator("temp_min", "temp_max", "temp", "feels_like", mode="before")
    def kelvin_to_celsius(cls, v):
        return v - 273.15


class Wind(BaseModel):
    speed: Optional[float] = None
    wind_direction_deg: Optional[float] = Field(None, alias="deg")
    gust: Optional[float] = None


class Clouds(BaseModel):
    cloudiness: Optional[float] = Field(None, alias="all")


class Rain(BaseModel):
    one_hour: Optional[float] = Field(None, alias="1h")
    three_hour: Optional[float] = Field(None, alias="3h")


class Snow(BaseModel):
    one_hour: Optional[float] = Field(None, alias="1h")
    thre_hour: Optional[float] = Field(None, alias="3h")


class Sys(BaseModel):
    type: Optional[int] = None
    id: Optional[int] = None
    message: Optional[float] = None
    country: Optional[str] = None
    sunrise: Optional[int] = None
    sunset: Optional[int] = None


class BaseWeatherPrediction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    weather: List[Weather] = []
    main_weather_description: Main = Field(Main(), alias="main")
    visibility: Optional[int] = None
    wind: Wind = Wind()
    clouds: Clouds = Clouds()
    rain: Optional[Rain] = None
    snow: Optional[Snow] = None
    date: str = Field(alias="dt")

    @field_validator("date", mode="before")
    def unix_timestamp_to_date(cls, v):
        return datetime.fromtimestamp(v).strftime("%Y-%m-%d %H:%M:%S")


class CurrentWeather(BaseWeatherPrediction):
    coord: Coord = Coord()
    base: Optional[str] = None


class CurrentWeatherForecast(BaseWeatherPrediction):
    pass


class ForecastWeather(BaseModel):
    model_config = ConfigDict(extra="ignore")
    cod: Optional[str] = None
    message: Optional[int] = None
    cnt: Optional[int] = None
    list: List[BaseWeatherPrediction] = []


class Locations(BaseModel):
    name: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    country: Optional[str] = None
    state: Optional[str] = None


class LocationsFound(BaseModel):
    locations: List[Locations] = []


class ErrorResponse(BaseModel):
    message: str
