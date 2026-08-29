"""
Smart Crop Advisory and Recommendation System - FastAPI Backend

This is the entry point for the backend server. It sets up the FastAPI app,
configures CORS for the React frontend, and includes all route modules.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import crop_router, yield_router, advisory_router, weather_router

app = FastAPI(
    title="Smart Crop Advisory API",
    description="AI/ML-powered crop recommendation, yield prediction, and advisory system",
    version="1.0.0",
)

# CORS: allow the React frontend (dev server runs on port 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Client-Info", "Apikey"],
)

# Register route modules
app.include_router(crop_router, prefix="/api", tags=["Crop Recommendation"])
app.include_router(yield_router, prefix="/api", tags=["Yield Prediction"])
app.include_router(advisory_router, prefix="/api", tags=["Farmer Advisory"])
app.include_router(weather_router, prefix="/api", tags=["Weather Advisory"])


@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Smart Crop Advisory API",
        "endpoints": [
            "/api/crop-recommendation",
            "/api/yield-prediction",
            "/api/farmer-advisory",
            "/api/weather-advisory",
        ],
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
