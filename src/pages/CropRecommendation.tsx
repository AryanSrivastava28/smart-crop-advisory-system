import { Sprout, Leaf, ThumbsUp, Info } from 'lucide-react'
import PageHeader from '../components/ui/PageHeader'
import FormInput from '../components/ui/FormInput'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import ErrorMessage from '../components/ui/ErrorMessage'
import ResultCard from '../components/ui/ResultCard'
import ConfidenceBar from '../components/ui/ConfidenceBar'
import { useForm } from '../hooks/useForm'
import { useAsync } from '../hooks/useAsync'
import { recommendCrop } from '../services'
import type { CropRecommendationResponse } from '../services/types'

export default function CropRecommendation() {
  const { data, loading, error, run } = useAsync<CropRecommendationResponse>()

  const form = useForm({
    nitrogen: { value: '', required: true, label: 'Nitrogen', min: 0, max: 140 },
    phosphorus: { value: '', required: true, label: 'Phosphorus', min: 0, max: 145 },
    potassium: { value: '', required: true, label: 'Potassium', min: 0, max: 205 },
    ph: { value: '', required: true, label: 'Soil pH', min: 0, max: 14 },
    temperature: { value: '', required: true, label: 'Temperature', min: -10, max: 50 },
    humidity: { value: '', required: true, label: 'Humidity', min: 0, max: 100 },
    rainfall: { value: '', required: true, label: 'Rainfall', min: 0, max: 500 },
  })

  const onSubmit = form.handleSubmit(async () => {
    await run(() =>
      recommendCrop({
        nitrogen: Number(form.values.nitrogen),
        phosphorus: Number(form.values.phosphorus),
        potassium: Number(form.values.potassium),
        ph: Number(form.values.ph),
        temperature: Number(form.values.temperature),
        humidity: Number(form.values.humidity),
        rainfall: Number(form.values.rainfall),
      }),
    )
  })

  return (
    <div className="animate-fade-in">
      <PageHeader
        title="Crop Recommendation"
        subtitle="Enter your soil and environmental data to get an AI-powered crop recommendation with confidence scores and factor analysis."
        icon={Sprout}
      />

      <div className="section-container grid gap-8 py-10 lg:grid-cols-2">
        {/* Form */}
        <div className="card p-6 sm:p-8">
          <h2 className="mb-1 text-lg font-semibold text-earth-800">Agricultural Data Input</h2>
          <p className="mb-6 text-sm text-earth-500">Fill in all fields to get an accurate recommendation.</p>

          <form onSubmit={onSubmit} className="space-y-5">
            <div className="grid gap-5 sm:grid-cols-2">
              <FormInput label="Nitrogen (N)" name="nitrogen" {...form} unit="kg/ha"
                value={form.values.nitrogen} placeholder="e.g. 90" min={0} max={140}
                error={form.errors.nitrogen} hint="0–140" />
              <FormInput label="Phosphorus (P)" name="phosphorus" {...form} unit="kg/ha"
                value={form.values.phosphorus} placeholder="e.g. 42" min={0} max={145}
                error={form.errors.phosphorus} hint="0–145" />
              <FormInput label="Potassium (K)" name="potassium" {...form} unit="kg/ha"
                value={form.values.potassium} placeholder="e.g. 43" min={0} max={205}
                error={form.errors.potassium} hint="0–205" />
              <FormInput label="Soil pH" name="ph" {...form} unit="0–14"
                value={form.values.ph} placeholder="e.g. 6.5" min={0} max={14} step="0.1"
                error={form.errors.ph} hint="0–14" />
              <FormInput label="Temperature" name="temperature" {...form} unit="°C"
                value={form.values.temperature} placeholder="e.g. 25" min={-10} max={50} step="0.1"
                error={form.errors.temperature} hint="-10 to 50" />
              <FormInput label="Humidity" name="humidity" {...form} unit="%"
                value={form.values.humidity} placeholder="e.g. 80" min={0} max={100}
                error={form.errors.humidity} hint="0–100%" />
              <FormInput label="Rainfall" name="rainfall" {...form} unit="mm"
                value={form.values.rainfall} placeholder="e.g. 200" min={0} max={500}
                error={form.errors.rainfall} hint="0–500 mm" />
            </div>

            <button type="submit" disabled={loading} className="btn-primary w-full">
              {loading ? 'Analyzing...' : 'Recommend Crop'}
            </button>
          </form>
        </div>

        {/* Results */}
        <div>
          {loading && <LoadingSpinner label="Analyzing your agricultural data..." />}
          {error && <ErrorMessage message={error} />}
          {!loading && !error && !data && (
            <div className="flex flex-col items-center justify-center gap-4 rounded-2xl border-2 border-dashed border-earth-200 py-16 text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary-50 text-primary-400">
                <Leaf className="h-8 w-8" />
              </div>
              <div>
                <p className="font-medium text-earth-600">No recommendation yet</p>
                <p className="mt-1 text-sm text-earth-400">Enter your data and click "Recommend Crop" to see results.</p>
              </div>
            </div>
          )}
          {data && !loading && (
            <div className="space-y-6">
              {/* Main result */}
              <ResultCard icon={Sprout} title="Recommended Crop">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-earth-500">Recommended Crop</p>
                    <p className="mt-1 text-3xl font-bold text-primary-700">{data.crop}</p>
                  </div>
                  <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-primary-50 text-primary-600">
                    <Sprout className="h-10 w-10" />
                  </div>
                </div>
                <div className="mt-6">
                  <ConfidenceBar value={data.confidence} label="Recommendation Confidence" />
                </div>
              </ResultCard>

              {/* Key factors */}
              <ResultCard icon={Info} title="Important Environmental Factors">
                <div className="space-y-4">
                  {data.keyFactors.map((f) => (
                    <div key={f.factor} className="flex items-start gap-3 border-b border-earth-100 pb-4 last:border-0 last:pb-0">
                      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-accent-50 text-accent-600">
                        <ThumbsUp className="h-4 w-4" />
                      </div>
                      <div>
                        <p className="text-sm font-semibold text-earth-700">{f.factor}: {f.value}</p>
                        <p className="mt-0.5 text-xs text-earth-500">{f.impact}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </ResultCard>

              {/* Explanation */}
              <ResultCard icon={Info} title="Why This Crop?">
                <p className="text-sm leading-relaxed text-earth-600">{data.explanation}</p>
              </ResultCard>

              {/* Alternatives */}
              <ResultCard icon={Leaf} title="Alternative Crops">
                <div className="space-y-3">
                  {data.alternatives.map((alt) => (
                    <div key={alt.crop} className="flex items-center justify-between">
                      <span className="text-sm font-medium text-earth-700">{alt.crop}</span>
                      <div className="flex items-center gap-3">
                        <div className="h-2 w-32 overflow-hidden rounded-full bg-earth-100">
                          <div className="h-full rounded-full bg-primary-400 transition-all duration-700" style={{ width: `${alt.suitability}%` }} />
                        </div>
                        <span className="text-xs font-medium text-earth-500">{alt.suitability}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </ResultCard>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
