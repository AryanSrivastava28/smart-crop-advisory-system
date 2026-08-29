import { apiRequest } from './apiClient'
import type {
  FarmerAdvisoryRequest,
  FarmerAdvisoryResponse,
} from './types'

function mockAdvisory(req: FarmerAdvisoryRequest): FarmerAdvisoryResponse {
  const risk: 'Low' | 'Moderate' | 'High' =
    req.temperature > 35 || req.humidity > 90
      ? 'High'
      : req.temperature > 30 || req.humidity > 80
        ? 'Moderate'
        : 'Low'

  return {
    crop: req.crop,
    riskLevel: risk,
    summary: `Advisory for ${req.crop} under ${req.soilCondition} soil conditions. Current temperature is ${req.temperature}°C with ${req.humidity}% humidity and ${req.rainfall} mm rainfall. Overall risk level: ${risk}.`,
    advisories: [
      {
        category: 'Growing Conditions',
        title: 'Optimal Growing Environment',
        advice: `${req.crop} thrives in temperatures between 20–30°C. Current temperature of ${req.temperature}°C is ${req.temperature > 30 ? 'above optimal — consider afternoon shading' : req.temperature < 20 ? 'below optimal — monitor growth rate' : 'within the ideal range'}. Maintain consistent conditions for best results.`,
        icon: 'Sprout',
      },
      {
        category: 'Soil Management',
        title: 'Soil Health Recommendations',
        advice: `${req.soilCondition} soil detected. Ensure proper drainage to prevent waterlogging, especially with ${req.rainfall} mm rainfall. Add organic matter to improve soil structure and nutrient retention. Test soil pH every 2–3 months.`,
        icon: 'Layers',
      },
      {
        category: 'Irrigation',
        title: 'Watering Schedule',
        advice: `With ${req.rainfall} mm rainfall and ${req.humidity}% humidity, ${req.rainfall > 150 ? 'reduce supplemental irrigation — natural rainfall is sufficient' : 'irrigate 2–3 times per week'}. Water early morning or late evening to minimize evaporation loss.`,
        icon: 'Droplets',
      },
      {
        category: 'Crop Care',
        title: 'Pest & Disease Management',
        advice: `${req.humidity > 80 ? 'High humidity increases fungal disease risk — apply preventive fungicide and ensure good air circulation.' : 'Humidity is moderate — maintain regular scouting for pests.'} Monitor for common ${req.crop} pests and use integrated pest management practices.`,
        icon: 'ShieldCheck',
      },
      {
        category: 'Fertilization',
        title: 'Nutrient Management',
        advice: `Apply balanced NPK fertilizer based on soil test results. For ${req.crop} in ${req.soilCondition} soil, split applications into 2–3 doses throughout the growing season for efficient nutrient uptake.`,
        icon: 'FlaskConical',
      },
    ],
  }
}

export async function getFarmerAdvisory(
  req: FarmerAdvisoryRequest,
): Promise<FarmerAdvisoryResponse> {
  return apiRequest('/api/farmer-advisory', req, () => mockAdvisory(req))
}
