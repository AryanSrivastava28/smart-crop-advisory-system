"""
Pydantic models for the Farmer Advisory endpoint.

These match the TypeScript interfaces in src/services/types.ts exactly.
"""

from typing import Literal

from pydantic import BaseModel, Field


class FarmerAdvisoryRequest(BaseModel):
    crop: str
    soilCondition: str
    temperature: float = Field(..., ge=-10, le=50)
    humidity: float = Field(..., ge=0, le=100)
    rainfall: float = Field(..., ge=0, le=500)


class AdvisoryItem(BaseModel):
    category: str
    title: str
    advice: str
    icon: str


class FarmerAdvisoryResponse(BaseModel):
    crop: str
    advisories: list[AdvisoryItem]
    riskLevel: Literal["Low", "Moderate", "High"]
    summary: str
