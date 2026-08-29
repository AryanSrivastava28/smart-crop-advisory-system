import { apiRequest } from './apiClient'
import type {
  YieldPredictionRequest,
  YieldPredictionResponse,
} from './types'

const cropBaseYields: Record<string, number> = {
  Rice: 2.4,
  Wheat: 3.1,
  Maize: 5.5,
  Cotton: 1.8,
  Tea: 1.5,
  Sugarcane: 70,
  Pulses: 0.9,
  Soybean: 1.6,
}

function mockYield(req: YieldPredictionRequest): YieldPredictionResponse {
  const base = cropBaseYields[req.crop] ?? 2.5
  const areaFactor = Math.max(0.7, Math.min(1.2, req.area / 5))
  const rainFactor = req.rainfall > 120 && req.rainfall < 250 ? 1.1 : 0.9
  const tempFactor = req.temperature > 20 && req.temperature < 32 ? 1.05 : 0.92
  const fertFactor = req.fertilizer > 50 && req.fertilizer < 150 ? 1.08 : 0.95

  const predicted = +(base * areaFactor * rainFactor * tempFactor * fertFactor).toFixed(2)
  const confidence = 78 + Math.floor(Math.random() * 15)

  const status = (v: number, lo: number, hi: number): 'optimal' | 'moderate' | 'low' =>
    v >= lo && v <= hi ? 'optimal' : v < lo ? 'low' : 'moderate'

  return {
    crop: req.crop,
    predictedYield: predicted,
    unit: 'tonnes/hectare',
    confidence,
    explanation: `Based on the provided inputs, ${req.crop} is expected to yield approximately ${predicted} tonnes per hectare. The prediction considers ${req.area} hectares of land, ${req.rainfall} mm rainfall, ${req.temperature}°C temperature, and ${req.fertilizer} kg/ha fertilizer usage during the ${req.season} season.`,
    factors: [
      {
        factor: 'Rainfall',
        status: status(req.rainfall, 120, 250),
        detail: `${req.rainfall} mm — ${status(req.rainfall, 120, 250) === 'optimal' ? 'ideal for growth' : 'adjust irrigation'}`,
      },
      {
        factor: 'Temperature',
        status: status(req.temperature, 20, 32),
        detail: `${req.temperature}°C — ${status(req.temperature, 20, 32) === 'optimal' ? 'within optimal range' : 'consider shade/ventilation'}`,
      },
      {
        factor: 'Fertilizer',
        status: status(req.fertilizer, 50, 150),
        detail: `${req.fertilizer} kg/ha — ${status(req.fertilizer, 50, 150) === 'optimal' ? 'balanced application' : 'review dosage'}`,
      },
      {
        factor: 'Humidity',
        status: status(req.humidity, 50, 80),
        detail: `${req.humidity}% — ${status(req.humidity, 50, 80) === 'optimal' ? 'good for growth' : 'monitor for disease'}`,
      },
    ],
    yearlyComparison: [
      { year: '2021', yield: +(predicted * 0.88).toFixed(2) },
      { year: '2022', yield: +(predicted * 0.92).toFixed(2) },
      { year: '2023', yield: +(predicted * 0.96).toFixed(2) },
      { year: '2024', yield: predicted },
    ],
  }
}

export async function predictYield(
  req: YieldPredictionRequest,
): Promise<YieldPredictionResponse> {
  return apiRequest('/api/yield-prediction', req, () => mockYield(req))
}
