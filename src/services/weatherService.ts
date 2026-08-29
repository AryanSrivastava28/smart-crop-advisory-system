import { apiRequest } from './apiClient'
import type { WeatherAdvisoryResponse } from './types'

function mockWeather(): WeatherAdvisoryResponse {
  const temp = 27 + Math.floor(Math.random() * 6)
  const humidity = 65 + Math.floor(Math.random() * 25)
  const rainfall = 80 + Math.floor(Math.random() * 120)
  const windSpeed = 8 + Math.floor(Math.random() * 15)

  let condition = 'Partly Cloudy'
  if (rainfall > 150) condition = 'Heavy Rain'
  else if (rainfall > 100) condition = 'Light Rain'
  else if (temp > 32) condition = 'Sunny & Hot'
  else if (humidity > 85) condition = 'Humid & Cloudy'

  const advisories: WeatherAdvisoryResponse['advisories'] = []

  if (rainfall > 150) {
    advisories.push({
      title: 'Heavy Rainfall Alert',
      advice: 'Ensure proper field drainage to prevent waterlogging. Delay fertilizer application until rainfall subsides.',
      severity: 'warning',
    })
  } else if (rainfall < 50) {
    advisories.push({
      title: 'Low Rainfall',
      advice: 'Increase irrigation frequency. Consider mulching to retain soil moisture during dry conditions.',
      severity: 'warning',
    })
  } else {
    advisories.push({
      title: 'Rainfall is Adequate',
      advice: 'Current rainfall supports normal crop growth. No additional irrigation needed for most crops.',
      severity: 'success',
    })
  }

  if (temp > 32) {
    advisories.push({
      title: 'High Temperature Warning',
      advice: 'Provide shade for sensitive crops. Increase watering frequency during peak heat hours.',
      severity: 'warning',
    })
  } else {
    advisories.push({
      title: 'Temperature is Favorable',
      advice: `${temp}°C is within the optimal range for most crops. Good conditions for growth.`,
      severity: 'success',
    })
  }

  if (humidity > 85) {
    advisories.push({
      title: 'High Humidity Notice',
      advice: 'Elevated humidity increases fungal disease risk. Monitor crops and apply preventive fungicide if needed.',
      severity: 'warning',
    })
  } else {
    advisories.push({
      title: 'Humidity is Balanced',
      advice: `${humidity}% humidity is suitable for healthy crop development with low disease pressure.`,
      severity: 'info',
    })
  }

  const suitableCrops =
    temp > 28
      ? ['Rice', 'Cotton', 'Sugarcane', 'Maize']
      : temp < 22
        ? ['Wheat', 'Tea', 'Peas', 'Mustard']
        : ['Rice', 'Wheat', 'Maize', 'Pulses']

  return {
    weather: {
      temperature: temp,
      humidity,
      rainfall,
      condition,
      windSpeed,
      location: 'Sample Region',
    },
    advisories,
    suitableCrops,
  }
}

export async function getWeatherAdvisory(): Promise<WeatherAdvisoryResponse> {
  return apiRequest('/api/weather-advisory', {}, mockWeather)
}
