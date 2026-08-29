"""
Crop Recommendation API Route

POST /api/crop-recommendation
Accepts soil and environmental data, returns a crop recommendation
using the trained ML model.
"""

from fastapi import APIRouter, HTTPException

from schemas import CropRecommendationRequest, CropRecommendationResponse, KeyFactor, AlternativeCrop
from services.crop_service import predict_crop

router = APIRouter()


@router.post("/crop-recommendation", response_model=CropRecommendationResponse)
async def crop_recommendation(req: CropRecommendationRequest):
    try:
        result = predict_crop(
            nitrogen=req.nitrogen,
            phosphorus=req.phosphorus,
            potassium=req.potassium,
            ph=req.ph,
            temperature=req.temperature,
            humidity=req.humidity,
            rainfall=req.rainfall,
        )

        # Build key factors analysis
        key_factors = [
            KeyFactor(
                factor="Temperature",
                value=f"{req.temperature}°C",
                impact=("Favorable for warm-season growth" if req.temperature > 25
                        else "Suitable for cool-season crop"),
            ),
            KeyFactor(
                factor="Rainfall",
                value=f"{req.rainfall} mm",
                impact=("Adequate water availability" if req.rainfall > 150
                        else "May require irrigation"),
            ),
            KeyFactor(
                factor="Soil pH",
                value=f"{req.ph}",
                impact=("Optimal nutrient absorption range" if 6 <= req.ph <= 7.5
                        else "Consider soil amendment"),
            ),
            KeyFactor(
                factor="Humidity",
                value=f"{req.humidity}%",
                impact=("Good for disease-sensitive crops — monitor" if req.humidity > 70
                        else "Low disease risk"),
            ),
        ]

        # Build alternatives from top probabilities (excluding the top pick)
        prob_map = result["probabilities"]
        sorted_crops = sorted(prob_map.items(), key=lambda x: x[1], reverse=True)
        alternatives = [
            AlternativeCrop(crop=c, suitability=int(round(p * 100)))
            for c, p in sorted_crops[1:4]
        ]

        # Build explanation
        explanation = (
            f"{result['crop']} is recommended because the current soil nutrients "
            f"(NPK: {req.nitrogen}-{req.phosphorus}-{req.potassium}), "
            f"temperature of {req.temperature}°C, and rainfall of {req.rainfall} mm "
            f"create an environment well-suited for its growth cycle. "
            f"The soil pH of {req.ph} supports efficient nutrient uptake for this crop."
        )

        return CropRecommendationResponse(
            crop=result["crop"],
            confidence=result["confidence"],
            keyFactors=key_factors,
            explanation=explanation,
            alternatives=alternatives,
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
