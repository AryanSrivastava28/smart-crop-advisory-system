"""
Farmer Advisory API Route

POST /api/farmer-advisory
Accepts crop, soil condition, and weather data, returns
personalized crop care advisories.
"""

from fastapi import APIRouter, HTTPException

from schemas import FarmerAdvisoryRequest, FarmerAdvisoryResponse
from services.advisory_service import get_advisory

router = APIRouter()


@router.post("/farmer-advisory", response_model=FarmerAdvisoryResponse)
async def farmer_advisory(req: FarmerAdvisoryRequest):
    try:
        result = get_advisory(
            crop=req.crop,
            soil_condition=req.soilCondition,
            temperature=req.temperature,
            humidity=req.humidity,
            rainfall=req.rainfall,
        )
        return FarmerAdvisoryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Advisory error: {str(e)}")
