import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import ClassVar

import pandas as pd
import requests
from pydantic import BaseModel, ConfigDict
from src.weather_api.weather_api_base import (
    CurrentWeather,
    ErrorResponse,
    ForecastWeather,
    LocationsFound,
    WeatherApiBase,
)
from utils.custom_logger import CustomLogger
from utils.settings import settings

logger = CustomLogger("OpenWeatherWrapper")


class OpenWeatherWrapper(WeatherApiBase):
    api_key: str
    executor: ThreadPoolExecutor
    loop: asyncio.AbstractEventLoop
    base_url: ClassVar[str] = "https://api.openweathermap.org/data/2.5"
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def format_response(self, response_object: BaseModel) -> str:
        return response_object.model_dump_json(exclude_none=True)

    def get_request(self, url: str) -> dict:
        response = requests.get(url)
        response.raise_for_status()
        response = response.json()
        return response

    def get_weather_from_lat_long(self, latitude: float, longitude: float) -> str:
        url = f"{self.base_url}/weather?lat={latitude}&lon={longitude}&appid={self.api_key}"
        try:
            response = self.get_request(url)
            response_parsed = CurrentWeather(**response)
            return self.format_response(response_parsed)
        except requests.exceptions.HTTPError as err:
            logger.exception("Error in getting weather data")
            response_parsed = ErrorResponse(message=str(err))
            return self.format_response(response_parsed)

    async def aget_weather_from_lat_long(
        self, latitude: float, longitude: float
    ) -> str:
        data = await self.loop.run_in_executor(
            self.executor, self.get_weather_from_lat_long, latitude, longitude
        )
        return data

    def get_weather_forecast_from_lat_long(
        self, latitude: float, longitude: float
    ) -> str:
        url = f"{self.base_url}/forecast?lat={latitude}&lon={longitude}&appid={self.api_key}"
        try:
            response = self.get_request(url)
            response_parsed = ForecastWeather(**response)

            return self.format_weather_forecast_to_timeseries_str(response_parsed)
        except requests.exceptions.HTTPError as err:
            logger.exception("Error in getting weather forecast data")
            response_parsed = ErrorResponse(message=str(err))
            return self.format_response(response_parsed)

    async def aget_weather_forecast_from_lat_long(
        self, latitude: float, longitude: float
    ) -> str:
        data = await self.loop.run_in_executor(
            self.executor, self.get_weather_forecast_from_lat_long, latitude, longitude
        )
        return data

    def format_weather_forecast_to_timeseries_str(
        self, forecast: ForecastWeather
    ) -> str:
        records = forecast.list
        data = []
        for record in records:
            data.append(
                {
                    "date": record.date,
                    "temperature": record.main_weather_description.temp,
                    "feels_like": record.main_weather_description.feels_like,
                    "humidity": record.main_weather_description.humidity,
                    "pressure": record.main_weather_description.pressure,
                    "weather": record.weather[0].description,
                }
            )
        df = pd.DataFrame.from_records(data)
        json_data = df.to_json(orient="columns")
        return json_data

    def get_air_pollution_from_lat_long(self, latitude: float, longitude: float) -> str:
        return self.format_response(
            ErrorResponse(message="Not implemented yet")
        )  # TODO implement this

    async def aget_air_pollution_from_lat_long(
        self, latitude: float, longitude: float
    ) -> str:
        data = await self.loop.run_in_executor(
            self.executor, self.get_air_pollution_from_lat_long, latitude, longitude
        )
        return data

    def get_coordinates_from_location_name(self, location_name: str) -> str:
        BASE_URL_FOR_CONVERTING = "http://api.openweathermap.org/geo/1.0"
        url_formated = (
            f"{BASE_URL_FOR_CONVERTING}/direct?q={location_name}&appid={self.api_key}"
        )
        try:
            response = self.get_request(url_formated)

            response_parsed = LocationsFound(locations=response)
            return self.format_response(response_parsed)
        except requests.exceptions.HTTPError as err:
            logger.exception("Error in getting coordinates from location name")
            response_parsed = ErrorResponse(message=str(err))
            return self.format_response(response_parsed)

    async def aget_coordinates_from_location_name(self, location_name: str) -> str:
        data = await self.loop.run_in_executor(
            self.executor, self.get_coordinates_from_location_name, location_name
        )
        return data

    @classmethod
    def create(cls, *args, **kwargs) -> "OpenWeatherWrapper":
        api_key = settings.WEATHER_API.API_KEY.get_secret_value()
        executor = ThreadPoolExecutor(max_workers=5)
        loop = asyncio.get_event_loop()
        return cls(api_key=api_key, executor=executor, loop=loop)
