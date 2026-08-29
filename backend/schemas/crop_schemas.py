"""
Pydantic models for the Crop Recommendation endpoint.

These match the TypeScript interfaces in src/services/types.ts exactly.
"""

from pydantic import BaseModel, Field


class CropRecommendationRequest(BaseModel):
    nitrogen: float = Field(..., ge=0, le=140)
    phosphorus: float = Field(..., ge=0, le=145)
    potassium: float = Field(..., ge=0, le=205)
    ph: float = Field(..., ge=0, le=14)
    temperature: float = Field(..., ge=-10, le=50)
    humidity: float = Field(..., ge=0, le=100)
    rainfall: float = Field(..., ge=0, le=500)


class KeyFactor(BaseModel):
    factor: str
    value: str
    impact: str


class AlternativeCrop(BaseModel):
    crop: str
    suitability: int


class CropRecommendationResponse(BaseModel):
    crop: str
    confidence: int
    keyFactors: list[KeyFactor]
    explanation: str
    alternatives: list[AlternativeCrop]
