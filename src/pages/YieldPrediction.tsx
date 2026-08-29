import { TrendingUp, ChartBar as BarChart3, Info, CircleCheck as CheckCircle2, TriangleAlert as AlertTriangle, CircleAlert as AlertCircle } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import PageHeader from '../components/ui/PageHeader'
import FormInput, { FormSelect } from '../components/ui/FormInput'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import ErrorMessage from '../components/ui/ErrorMessage'
import ResultCard from '../components/ui/ResultCard'
import ConfidenceBar from '../components/ui/ConfidenceBar'
import { useForm } from '../hooks/useForm'
import { useAsync } from '../hooks/useAsync'
import { predictYield } from '../services'
import type { YieldPredictionResponse } from '../services/types'

const cropOptions = [
  { value: 'Rice', label: 'Rice' },
  { value: 'Wheat', label: 'Wheat' },
  { value: 'Maize', label: 'Maize' },
  { value: 'Cotton', label: 'Cotton' },
  { value: 'Tea', label: 'Tea' },
  { value: 'Sugarcane', label: 'Sugarcane' },
  { value: 'Pulses', label: 'Pulses' },
  { value: 'Soybean', label: 'Soybean' },
]

const seasonOptions = [
  { value: 'Kharif', label: 'Kharif (Monsoon)' },
  { value: 'Rabi', label: 'Rabi (Winter)' },
  { value: 'Zaid', label: 'Zaid (Summer)' },
]

const statusConfig = {
  optimal: { icon: CheckCircle2, color: 'text-primary-600', bg: 'bg-primary-50', label: 'Optimal' },
  moderate: { icon: AlertCircle, color: 'text-amber-600', bg: 'bg-amber-50', label: 'Moderate' },
  low: { icon: AlertTriangle, color: 'text-red-500', bg: 'bg-red-50', label: 'Low' },
}

export default function YieldPrediction() {
  const { data, loading, error, run } = useAsync<YieldPredictionResponse>()

  const form = useForm({
    crop: { value: '', required: true, label: 'Crop' },
    area: { value: '', required: true, label: 'Area', min: 0.1, max: 10000 },
    rainfall: { value: '', required: true, label: 'Rainfall', min: 0, max: 500 },
    temperature: { value: '', required: true, label: 'Temperature', min: -10, max: 50 },
    humidity: { value: '', required: true, label: 'Humidity', min: 0, max: 100 },
    fertilizer: { value: '', required: true, label: 'Fertilizer', min: 0, max: 500 },
    season: { value: '', required: true, label: 'Season' },
  })

  const onSubmit = form.handleSubmit(async () => {
    await run(() =>
      predictYield({
        crop: form.values.crop,
        area: Number(form.values.area),
        rainfall: Number(form.values.rainfall),
        temperature: Number(form.values.temperature),
        humidity: Number(form.values.humidity),
        fertilizer: Number(form.values.fertilizer),
        season: form.values.season,
      }),
    )
  })

  return (
    <div className="animate-fade-in">
      <PageHeader
        title="Crop Yield Prediction"
        subtitle="Predict expected crop yield based on environmental inputs, fertilizer usage, and historical data patterns using machine learning."
        icon={TrendingUp}
      />

      <div className="section-container grid gap-8 py-10 lg:grid-cols-2">
        {/* Form */}
        <div className="card p-6 sm:p-8">
          <h2 className="mb-1 text-lg font-semibold text-earth-800">Prediction Input</h2>
          <p className="mb-6 text-sm text-earth-500">Provide crop and environmental details for yield estimation.</p>

          <form onSubmit={onSubmit} className="space-y-5">
            <FormSelect label="Crop Name" name="crop" {...form}
              value={form.values.crop} options={cropOptions} placeholder="Select a crop"
              error={form.errors.crop} />
            <div className="grid gap-5 sm:grid-cols-2">
              <FormInput label="Area" name="area" {...form} unit="hectares"
                value={form.values.area} placeholder="e.g. 5" min={0.1} max={10000} step="0.1"
                error={form.errors.area} hint="0.1–10000 ha" />
              <FormInput label="Rainfall" name="rainfall" {...form} unit="mm"
                value={form.values.rainfall} placeholder="e.g. 200" min={0} max={500}
                error={form.errors.rainfall} hint="0–500 mm" />
              <FormInput label="Temperature" name="temperature" {...form} unit="°C"
                value={form.values.temperature} placeholder="e.g. 27" min={-10} max={50} step="0.1"
                error={form.errors.temperature} hint="-10 to 50" />
              <FormInput label="Humidity" name="humidity" {...form} unit="%"
                value={form.values.humidity} placeholder="e.g. 70" min={0} max={100}
                error={form.errors.humidity} hint="0–100%" />
              <FormInput label="Fertilizer Usage" name="fertilizer" {...form} unit="kg/ha"
                value={form.values.fertilizer} placeholder="e.g. 100" min={0} max={500}
                error={form.errors.fertilizer} hint="0–500 kg/ha" />
              <FormSelect label="Season" name="season" {...form}
                value={form.values.season} options={seasonOptions} placeholder="Select season"
                error={form.errors.season} />
            </div>

            <button type="submit" disabled={loading} className="btn-primary w-full">
              {loading ? 'Predicting...' : 'Predict Yield'}
            </button>
          </form>
        </div>

        {/* Results */}
        <div>
          {loading && <LoadingSpinner label="Running yield prediction model..." />}
          {error && <ErrorMessage message={error} />}
          {!loading && !error && !data && (
            <div className="flex flex-col items-center justify-center gap-4 rounded-2xl border-2 border-dashed border-earth-200 py-16 text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary-50 text-primary-400">
                <BarChart3 className="h-8 w-8" />
              </div>
              <div>
                <p className="font-medium text-earth-600">No prediction yet</p>
                <p className="mt-1 text-sm text-earth-400">Enter your data and click "Predict Yield" to see results.</p>
              </div>
            </div>
          )}
          {data && !loading && (
            <div className="space-y-6">
              {/* Main result */}
              <ResultCard icon={TrendingUp} title="Predicted Yield Result">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-earth-500">Selected Crop</p>
                    <p className="mt-1 text-2xl font-bold text-primary-700">{data.crop}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-earth-500">Predicted Yield</p>
                    <p className="mt-1 text-3xl font-bold text-earth-800">{data.predictedYield}</p>
                    <p className="text-xs text-earth-400">{data.unit}</p>
                  </div>
                </div>
                <div className="mt-6">
                  <ConfidenceBar value={data.confidence} label="Prediction Confidence" />
                </div>
              </ResultCard>

              {/* Factor analysis */}
              <ResultCard icon={Info} title="Contributing Factors">
                <div className="space-y-4">
                  {data.factors.map((f) => {
                    const cfg = statusConfig[f.status]
                    return (
                      <div key={f.factor} className="flex items-start gap-3 border-b border-earth-100 pb-4 last:border-0 last:pb-0">
                        <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg ${cfg.bg} ${cfg.color}`}>
                          <cfg.icon className="h-4 w-4" />
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center justify-between">
                            <p className="text-sm font-semibold text-earth-700">{f.factor}</p>
                            <span className={`badge ${cfg.bg} ${cfg.color}`}>{cfg.label}</span>
                          </div>
                          <p className="mt-0.5 text-xs text-earth-500">{f.detail}</p>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </ResultCard>

              {/* Yearly comparison chart */}
              <ResultCard icon={BarChart3} title="Yearly Yield Comparison">
                <div className="h-64 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data.yearlyComparison}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e7e5e4" vertical={false} />
                      <XAxis dataKey="year" tick={{ fontSize: 12, fill: '#78716c' }} axisLine={false} tickLine={false} />
                      <YAxis tick={{ fontSize: 12, fill: '#78716c' }} axisLine={false} tickLine={false} />
                      <Tooltip
                        contentStyle={{ borderRadius: '12px', border: '1px solid #e7e5e4', fontSize: '13px' }}
                        cursor={{ fill: '#f0fdf4' }}
                      />
                      <Bar dataKey="yield" radius={[8, 8, 0, 0]} name="Yield (t/ha)">
                        {data.yearlyComparison.map((_entry, i) => (
                          <Cell key={i} fill={i === data.yearlyComparison.length - 1 ? '#16a34a' : '#86efac'} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <p className="mt-4 text-xs text-earth-400">
                  The highlighted bar shows the current predicted yield. Earlier years show historical context.
                </p>
              </ResultCard>

              {/* Explanation */}
              <ResultCard icon={Info} title="Prediction Explanation">
                <p className="text-sm leading-relaxed text-earth-600">{data.explanation}</p>
              </ResultCard>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
