"""
Weather Advisory API Route

POST /api/weather-advisory
Accepts optional weather data, returns weather-based agricultural advisories.
If no weather data is provided, generates realistic sample data.
"""

from fastapi import APIRouter, HTTPException

from schemas import WeatherAdvisoryRequest, WeatherAdvisoryResponse
from services.weather_service import get_weather_advisory

router = APIRouter()


@router.post("/weather-advisory", response_model=WeatherAdvisoryResponse)
async def weather_advisory(req: WeatherAdvisoryRequest):
    try:
        result = get_weather_advisory(
            temperature=req.temperature,
            humidity=req.humidity,
            rainfall=req.rainfall,
            condition=req.condition,
            windSpeed=req.windSpeed,
        )
        return WeatherAdvisoryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather advisory error: {str(e)}")
