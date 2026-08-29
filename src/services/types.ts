export interface CropRecommendationRequest {
  nitrogen: number
  phosphorus: number
  potassium: number
  ph: number
  temperature: number
  humidity: number
  rainfall: number
}

export interface CropRecommendationResponse {
  crop: string
  confidence: number
  keyFactors: { factor: string; value: string; impact: string }[]
  explanation: string
  alternatives: { crop: string; suitability: number }[]
}

export interface YieldPredictionRequest {
  crop: string
  area: number
  rainfall: number
  temperature: number
  humidity: number
  fertilizer: number
  season: string
}

export interface YieldPredictionResponse {
  crop: string
  predictedYield: number
  unit: string
  confidence: number
  explanation: string
  factors: { factor: string; status: 'optimal' | 'moderate' | 'low'; detail: string }[]
  yearlyComparison: { year: string; yield: number }[]
}

export interface FarmerAdvisoryRequest {
  crop: string
  soilCondition: string
  temperature: number
  humidity: number
  rainfall: number
}

export interface FarmerAdvisoryResponse {
  crop: string
  advisories: { category: string; title: string; advice: string; icon: string }[]
  riskLevel: 'Low' | 'Moderate' | 'High'
  summary: string
}

export interface WeatherData {
  temperature: number
  humidity: number
  rainfall: number
  condition: string
  windSpeed: number
  location: string
}

export interface WeatherAdvisoryResponse {
  weather: WeatherData
  advisories: { title: string; advice: string; severity: 'info' | 'warning' | 'success' }[]
  suitableCrops: string[]
}
