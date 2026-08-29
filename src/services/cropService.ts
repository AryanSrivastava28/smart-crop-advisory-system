import { apiRequest } from './apiClient'
import type {
  CropRecommendationRequest,
  CropRecommendationResponse,
} from './types'

function mockRecommendation(
  req: CropRecommendationRequest,
): CropRecommendationResponse {
  // Simple heuristic-based mock for demonstration.
  const { temperature, rainfall, humidity, ph } = req

  let crop = 'Rice'
  if (temperature < 20 && rainfall > 150) crop = 'Wheat'
  else if (temperature > 28 && rainfall < 80) crop = 'Maize'
  else if (humidity > 80 && rainfall > 180) crop = 'Rice'
  else if (ph < 5.5) crop = 'Tea'
  else if (temperature > 25 && rainfall < 100) crop = 'Cotton'

  const confidence = 82 + Math.floor(Math.random() * 12)

  return {
    crop,
    confidence,
    keyFactors: [
      {
        factor: 'Temperature',
        value: `${temperature}°C`,
        impact: temperature > 25 ? 'Favorable for warm-season growth' : 'Suitable for cool-season crop',
      },
      {
        factor: 'Rainfall',
        value: `${rainfall} mm`,
        impact: rainfall > 150 ? 'Adequate water availability' : 'May require irrigation',
      },
      {
        factor: 'Soil pH',
        value: `${ph}`,
        impact: ph >= 6 && ph <= 7.5 ? 'Optimal nutrient absorption range' : 'Consider soil amendment',
      },
      {
        factor: 'Humidity',
        value: `${humidity}%`,
        impact: humidity > 70 ? 'Good for disease-sensitive crops — monitor' : 'Low disease risk',
      },
    ],
    explanation: `${crop} is recommended because the current soil nutrients (NPK: ${req.nitrogen}-${req.phosphorus}-${req.potassium}), temperature of ${temperature}°C, and rainfall of ${rainfall} mm create an environment well-suited for its growth cycle. The soil pH of ${ph} supports efficient nutrient uptake for this crop.`,
    alternatives: [
      { crop: crop === 'Rice' ? 'Wheat' : 'Rice', suitability: 74 },
      { crop: 'Maize', suitability: 68 },
      { crop: 'Cotton', suitability: 55 },
    ],
  }
}

export async function recommendCrop(
  req: CropRecommendationRequest,
): Promise<CropRecommendationResponse> {
  return apiRequest('/api/crop-recommendation', req, () =>
    mockRecommendation(req),
  )
}
