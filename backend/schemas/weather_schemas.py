"""
Pydantic models for the Weather Advisory endpoint.

These match the TypeScript interfaces in src/services/types.ts exactly.
The frontend currently sends an empty body for weather, but we accept
optional weather values so the backend can generate advice from user input.
"""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class WeatherAdvisoryRequest(BaseModel):
    temperature: Optional[float] = Field(None, ge=-10, le=50)
    humidity: Optional[float] = Field(None, ge=0, le=100)
    rainfall: Optional[float] = Field(None, ge=0, le=500)
    condition: Optional[str] = None
    windSpeed: Optional[float] = Field(None, ge=0, le=200)


class WeatherData(BaseModel):
    temperature: float
    humidity: float
    rainfall: float
    condition: str
    windSpeed: float
    location: str


class WeatherAdvisoryItem(BaseModel):
    title: str
    advice: str
    severity: Literal["info", "warning", "success"]


class WeatherAdvisoryResponse(BaseModel):
    weather: WeatherData
    advisories: list[WeatherAdvisoryItem]
    suitableCrops: list[str]
