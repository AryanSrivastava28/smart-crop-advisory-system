import { Lightbulb, Sprout, Layers, Droplets, ShieldCheck, FlaskConical, Info, ShieldAlert } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'
import PageHeader from '../components/ui/PageHeader'
import FormInput, { FormSelect } from '../components/ui/FormInput'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import ErrorMessage from '../components/ui/ErrorMessage'
import ResultCard from '../components/ui/ResultCard'
import { useForm } from '../hooks/useForm'
import { useAsync } from '../hooks/useAsync'
import { getFarmerAdvisory } from '../services'
import type { FarmerAdvisoryResponse } from '../services/types'

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

const soilOptions = [
  { value: 'Loamy', label: 'Loamy' },
  { value: 'Clay', label: 'Clay' },
  { value: 'Sandy', label: 'Sandy' },
  { value: 'Silty', label: 'Silty' },
  { value: 'Peaty', label: 'Peaty' },
  { value: 'Chalky', label: 'Chalky' },
]

const iconMap: Record<string, LucideIcon> = {
  Sprout,
  Layers,
  Droplets,
  ShieldCheck,
  FlaskConical,
}

const riskConfig = {
  Low: { bg: 'bg-primary-50', text: 'text-primary-700', border: 'border-primary-200', icon: ShieldCheck },
  Moderate: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200', icon: ShieldAlert },
  High: { bg: 'bg-red-50', text: 'text-red-700', border: 'border-red-200', icon: ShieldAlert },
}

export default function FarmerAdvisory() {
  const { data, loading, error, run } = useAsync<FarmerAdvisoryResponse>()

  const form = useForm({
    crop: { value: '', required: true, label: 'Crop' },
    soilCondition: { value: '', required: true, label: 'Soil Condition' },
    temperature: { value: '', required: true, label: 'Temperature', min: -10, max: 50 },
    humidity: { value: '', required: true, label: 'Humidity', min: 0, max: 100 },
    rainfall: { value: '', required: true, label: 'Rainfall', min: 0, max: 500 },
  })

  const onSubmit = form.handleSubmit(async () => {
    await run(() =>
      getFarmerAdvisory({
        crop: form.values.crop,
        soilCondition: form.values.soilCondition,
        temperature: Number(form.values.temperature),
        humidity: Number(form.values.humidity),
        rainfall: Number(form.values.rainfall),
      }),
    )
  })

  return (
    <div className="animate-fade-in">
      <PageHeader
        title="Smart Farmer Advisory"
        subtitle="Get personalized crop care suggestions including growing conditions, soil management, watering recommendations, and pest control advice."
        icon={Lightbulb}
      />

      <div className="section-container grid gap-8 py-10 lg:grid-cols-2">
        {/* Form */}
        <div className="card p-6 sm:p-8">
          <h2 className="mb-1 text-lg font-semibold text-earth-800">Advisory Input</h2>
          <p className="mb-6 text-sm text-earth-500">Tell us about your crop and conditions to receive tailored advice.</p>

          <form onSubmit={onSubmit} className="space-y-5">
            <FormSelect label="Crop" name="crop" {...form}
              value={form.values.crop} options={cropOptions} placeholder="Select a crop"
              error={form.errors.crop} />
            <FormSelect label="Soil Condition" name="soilCondition" {...form}
              value={form.values.soilCondition} options={soilOptions} placeholder="Select soil type"
              error={form.errors.soilCondition} />
            <div className="grid gap-5 sm:grid-cols-3">
              <FormInput label="Temperature" name="temperature" {...form} unit="°C"
                value={form.values.temperature} placeholder="e.g. 27" min={-10} max={50} step="0.1"
                error={form.errors.temperature} />
              <FormInput label="Humidity" name="humidity" {...form} unit="%"
                value={form.values.humidity} placeholder="e.g. 70" min={0} max={100}
                error={form.errors.humidity} />
              <FormInput label="Rainfall" name="rainfall" {...form} unit="mm"
                value={form.values.rainfall} placeholder="e.g. 150" min={0} max={500}
                error={form.errors.rainfall} />
            </div>

            <button type="submit" disabled={loading} className="btn-primary w-full">
              {loading ? 'Generating Advisory...' : 'Get Advisory'}
            </button>
          </form>
        </div>

        {/* Results */}
        <div>
          {loading && <LoadingSpinner label="Generating smart advisory..." />}
          {error && <ErrorMessage message={error} />}
          {!loading && !error && !data && (
            <div className="flex flex-col items-center justify-center gap-4 rounded-2xl border-2 border-dashed border-earth-200 py-16 text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary-50 text-primary-400">
                <Lightbulb className="h-8 w-8" />
              </div>
              <div>
                <p className="font-medium text-earth-600">No advisory yet</p>
                <p className="mt-1 text-sm text-earth-400">Enter your crop and conditions to receive smart advice.</p>
              </div>
            </div>
          )}
          {data && !loading && (
            <div className="space-y-6">
              {/* Summary */}
              <ResultCard icon={Lightbulb} title="Advisory Summary">
                <div className="flex items-center gap-3 mb-4">
                  <span className="text-sm font-semibold text-earth-700">{data.crop}</span>
                  {(() => {
                    const cfg = riskConfig[data.riskLevel]
                    return (
                      <span className={`badge ${cfg.bg} ${cfg.text} border ${cfg.border}`}>
                        <cfg.icon className="h-3.5 w-3.5" /> Risk: {data.riskLevel}
                      </span>
                    )
                  })()}
                </div>
                <p className="text-sm leading-relaxed text-earth-600">{data.summary}</p>
              </ResultCard>

              {/* Advisory cards */}
              {data.advisories.map((a) => {
                const Icon = iconMap[a.icon] || Info
                return (
                  <div key={a.category} className="card animate-slide-up p-5">
                    <div className="flex items-start gap-4">
                      <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-primary-50 text-primary-600">
                        <Icon className="h-5 w-5" />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="badge bg-accent-50 text-accent-600">{a.category}</span>
                        </div>
                        <h3 className="mt-2 text-sm font-semibold text-earth-800">{a.title}</h3>
                        <p className="mt-1.5 text-sm leading-relaxed text-earth-500">{a.advice}</p>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
