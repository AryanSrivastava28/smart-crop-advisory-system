"""
Pydantic models for the Yield Prediction endpoint.

These match the TypeScript interfaces in src/services/types.ts exactly.
"""

from typing import Literal

from pydantic import BaseModel, Field


class YieldPredictionRequest(BaseModel):
    crop: str
    area: float = Field(..., gt=0)
    rainfall: float = Field(..., ge=0)
    temperature: float = Field(..., ge=-10, le=50)
    humidity: float = Field(..., ge=0, le=100)
    fertilizer: float = Field(..., ge=0)
    season: str


class YieldFactor(BaseModel):
    factor: str
    status: Literal["optimal", "moderate", "low"]
    detail: str


class YearlyComparison(BaseModel):
    year: str
    yield_: float = Field(..., alias="yield")

    model_config = {"populate_by_name": True}


class YieldPredictionResponse(BaseModel):
    crop: str
    predictedYield: float
    unit: str
    confidence: int
    explanation: str
    factors: list[YieldFactor]
    yearlyComparison: list[YearlyComparison]
