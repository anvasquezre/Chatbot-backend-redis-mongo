from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from src.weather_api.open_weather_wrapper import OpenWeatherWrapper


class SearchInputByLatLong(BaseModel):
    latitude: float = Field(description="latitude of the location")
    longitude: float = Field(description="longitude of the location")


class SearchInputByLocationName(BaseModel):
    location_name: str = Field(
        description="name of the location a City name or country code divided by comma Please use ISO 3166 country codes  Example London uk"
    )


class CurrentWeatherSearchToolByLatLong(BaseTool):
    name = "current"
    description = "useful for when you need to get the current weather of a and specific latitude and longitude"
    args_schema: Type[BaseModel] = SearchInputByLatLong

    def _run(
        self,
        latitude: float,
        longitude: float,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return OpenWeatherWrapper.create().get_weather_from_lat_long(
            latitude, longitude
        )

    async def _arun(
        self,
        latitude: float,
        longitude: float,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return await OpenWeatherWrapper.create().aget_weather_from_lat_long(
            latitude, longitude
        )


class ForecastWeatherSearchTool(BaseTool):
    name = "forecast"
    description = "useful for when you need to get the forecast weather of a and specific latitude and longitude"
    args_schema: Type[BaseModel] = SearchInputByLatLong

    def _run(
        self,
        latitude: float,
        longitude: float,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool"""
        return OpenWeatherWrapper.create().get_weather_forecast_from_lat_long(
            latitude, longitude
        )

    async def _arun(
        self,
        latitude: float,
        longitude: float,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously"""
        return await OpenWeatherWrapper.create().aget_weather_forecast_from_lat_long(
            latitude, longitude
        )


class GetCoordinatesByLocationName(BaseTool):
    name = "get_coordinates"
    description = (
        "useful for when you need to get the coordinates of a location by its name"
    )
    args_schema: Type[BaseModel] = SearchInputByLocationName

    def _run(
        self,
        location_name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return OpenWeatherWrapper.create().get_coordinates_from_location_name(
            location_name
        )

    async def _arun(
        self,
        location_name: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return await OpenWeatherWrapper.create().aget_coordinates_from_location_name(
            location_name
        )
