import { useEffect, useState } from 'react'
import { CloudSun, Thermometer, Droplets, CloudRain, Wind, CircleCheck as CheckCircle2, TriangleAlert as AlertTriangle, Info, RefreshCw } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'
import PageHeader from '../components/ui/PageHeader'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import ErrorMessage from '../components/ui/ErrorMessage'
import { getWeatherAdvisory } from '../services'
import type { WeatherAdvisoryResponse } from '../services/types'

const severityConfig: Record<string, { bg: string; text: string; border: string; icon: LucideIcon }> = {
  success: { bg: 'bg-primary-50', text: 'text-primary-700', border: 'border-primary-200', icon: CheckCircle2 },
  warning: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200', icon: AlertTriangle },
  info: { bg: 'bg-accent-50', text: 'text-accent-600', border: 'border-accent-200', icon: Info },
}

export default function WeatherAdvisory() {
  const [data, setData] = useState<WeatherAdvisoryResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchWeather = async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await getWeatherAdvisory()
      setData(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load weather data')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchWeather()
  }, [])

  const weatherStats = data ? [
    { icon: Thermometer, label: 'Temperature', value: `${data.weather.temperature}°C`, color: 'text-orange-500', bg: 'bg-orange-50' },
    { icon: Droplets, label: 'Humidity', value: `${data.weather.humidity}%`, color: 'text-accent-500', bg: 'bg-accent-50' },
    { icon: CloudRain, label: 'Rainfall', value: `${data.weather.rainfall} mm`, color: 'text-primary-600', bg: 'bg-primary-50' },
    { icon: Wind, label: 'Wind Speed', value: `${data.weather.windSpeed} km/h`, color: 'text-earth-500', bg: 'bg-earth-100' },
  ] : []

  return (
    <div className="animate-fade-in">
      <PageHeader
        title="Weather-Based Advisory"
        subtitle="Current weather conditions and their impact on farming activities, with tailored agricultural advice based on real-time data."
        icon={CloudSun}
      >
        <div className="mt-6">
          <button onClick={fetchWeather} disabled={loading} className="btn-secondary">
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} /> Refresh Data
          </button>
        </div>
      </PageHeader>

      <div className="section-container py-10">
        {loading && <LoadingSpinner label="Fetching weather data..." />}
        {error && <ErrorMessage message={error} onRetry={fetchWeather} />}

        {data && !loading && (
          <div className="space-y-8">
            {/* Weather overview */}
            <div className="card overflow-hidden">
              <div className="bg-gradient-to-br from-accent-500 to-accent-700 px-6 py-8 text-white sm:px-8">
                <div className="flex flex-wrap items-center justify-between gap-4">
                  <div>
                    <p className="text-sm text-accent-50">Current Condition</p>
                    <p className="mt-1 text-3xl font-bold">{data.weather.condition}</p>
                    <p className="mt-1 text-sm text-accent-100">{data.weather.location}</p>
                  </div>
                  <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-white/20 backdrop-blur-sm">
                    <CloudSun className="h-10 w-10" />
                  </div>
                </div>
              </div>
              <div className="grid gap-4 p-6 sm:grid-cols-2 lg:grid-cols-4">
                {weatherStats.map((stat) => (
                  <div key={stat.label} className="flex items-center gap-3 rounded-xl bg-earth-50 p-4">
                    <div className={`flex h-11 w-11 items-center justify-center rounded-xl ${stat.bg} ${stat.color}`}>
                      <stat.icon className="h-5 w-5" />
                    </div>
                    <div>
                      <p className="text-xs text-earth-500">{stat.label}</p>
                      <p className="text-lg font-bold text-earth-800">{stat.value}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Advisories */}
            <div>
              <h2 className="mb-4 text-lg font-semibold text-earth-800">Agricultural Advisories</h2>
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {data.advisories.map((adv, i) => {
                  const cfg = severityConfig[adv.severity]
                  return (
                    <div key={i} className={`card animate-slide-up border-l-4 ${cfg.border} p-5`} style={{ animationDelay: `${i * 80}ms` }}>
                      <div className="flex items-start gap-3">
                        <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg ${cfg.bg} ${cfg.text}`}>
                          <cfg.icon className="h-4 w-4" />
                        </div>
                        <div>
                          <h3 className="text-sm font-semibold text-earth-800">{adv.title}</h3>
                          <p className="mt-1 text-xs leading-relaxed text-earth-500">{adv.advice}</p>
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>

            {/* Suitable crops */}
            <div className="card p-6">
              <h2 className="mb-4 text-lg font-semibold text-earth-800">Crops Suitable for Current Weather</h2>
              <div className="flex flex-wrap gap-3">
                {data.suitableCrops.map((crop) => (
                  <span key={crop} className="badge bg-primary-50 px-4 py-2 text-sm text-primary-700">
                    <span className="h-2 w-2 rounded-full bg-primary-500" /> {crop}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
