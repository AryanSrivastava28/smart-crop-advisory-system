import { Link } from 'react-router-dom'
import { Sprout, TrendingUp, CloudSun, Lightbulb, FlaskConical, ArrowRight, Activity, Layers, Droplets, Thermometer } from 'lucide-react'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadialBarChart, RadialBar, PolarAngleAxis } from 'recharts'
import PageHeader from '../components/ui/PageHeader'
import type { LucideIcon } from 'lucide-react'

interface SummaryCardProps {
  icon: LucideIcon
  title: string
  value: string
  subtitle: string
  to: string
  delay: number
  children?: React.ReactNode
}

function SummaryCard({ icon: Icon, title, value, subtitle, to, delay, children }: SummaryCardProps) {
  return (
    <Link
      to={to}
      className="card card-hover group flex flex-col p-6 animate-fade-in-up"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="flex items-start justify-between">
        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-primary-50 text-primary-600 transition-colors group-hover:bg-primary-600 group-hover:text-white">
          <Icon className="h-5 w-5" />
        </div>
        <ArrowRight className="h-4 w-4 text-earth-300 transition-all group-hover:translate-x-1 group-hover:text-primary-500" />
      </div>
      <p className="mt-4 text-xs font-medium uppercase tracking-wide text-earth-400">{title}</p>
      <p className="mt-1 text-2xl font-bold text-earth-800">{value}</p>
      <p className="mt-1 text-sm text-earth-500">{subtitle}</p>
      {children}
    </Link>
  )
}

const yieldData = [
  { month: 'Jan', yield: 1.8 },
  { month: 'Feb', yield: 2.1 },
  { month: 'Mar', yield: 2.5 },
  { month: 'Apr', yield: 2.3 },
  { month: 'May', yield: 2.8 },
  { month: 'Jun', yield: 3.1 },
  { month: 'Jul', yield: 2.9 },
  { month: 'Aug', yield: 3.3 },
]

const soilData = [
  { name: 'Nitrogen', value: 90, fill: '#16a34a' },
  { name: 'Phosphorus', value: 42, fill: '#0ea5e9' },
  { name: 'Potassium', value: 43, fill: '#f59e0b' },
]

export default function Dashboard() {
  return (
    <div className="animate-fade-in">
      <PageHeader
        title="Dashboard"
        subtitle="An overview of all your crop recommendations, yield predictions, soil analysis, weather conditions, and advisories in one place."
        icon={Activity}
      />

      <div className="section-container py-10">
        {/* Summary cards */}
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <SummaryCard icon={Sprout} title="Recommended Crop" value="Rice" subtitle="92% confidence — based on NPK & weather data" to="/crop-recommendation" delay={0}>
            <div className="mt-3 h-2 w-full overflow-hidden rounded-full bg-earth-100">
              <div className="h-full rounded-full bg-primary-500 transition-all duration-700" style={{ width: '92%' }} />
            </div>
          </SummaryCard>

          <SummaryCard icon={TrendingUp} title="Predicted Yield" value="2.4 t/ha" subtitle="Rice — 88% confidence" to="/yield-prediction" delay={80}>
            <div className="mt-3 flex items-center gap-2 text-xs text-primary-600">
              <TrendingUp className="h-3.5 w-3.5" /> +8% vs last year
            </div>
          </SummaryCard>

          <SummaryCard icon={CloudSun} title="Weather Summary" value="Partly Cloudy" subtitle="27°C · 72% humidity · 120mm rain" to="/weather-advisory" delay={160} />

          <SummaryCard icon={FlaskConical} title="Soil Summary" value="Healthy" subtitle="pH 6.5 · Loamy soil · NPK balanced" to="/crop-recommendation" delay={240}>
            <div className="mt-3 flex gap-2">
              <span className="badge bg-primary-50 text-primary-600">N: 90</span>
              <span className="badge bg-accent-50 text-accent-600">P: 42</span>
              <span className="badge bg-amber-50 text-amber-600">K: 43</span>
            </div>
          </SummaryCard>

          <SummaryCard icon={Lightbulb} title="Latest Advisory" value="Moderate Risk" subtitle="Monitor humidity for fungal disease" to="/farmer-advisory" delay={320} />

          <SummaryCard icon={Layers} title="Soil Type" value="Loamy" subtitle="Good drainage & nutrient retention" to="/crop-recommendation" delay={400} />
        </div>

        {/* Charts row */}
        <div className="mt-8 grid gap-6 lg:grid-cols-2">
          {/* Yield trend */}
          <div className="card p-6">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <h3 className="text-base font-semibold text-earth-800">Yield Trend</h3>
                <p className="text-xs text-earth-500">Monthly predicted yield (tonnes/hectare)</p>
              </div>
              <Link to="/yield-prediction" className="btn-ghost text-xs">
                Details <ArrowRight className="h-3 w-3" />
              </Link>
            </div>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={yieldData}>
                  <defs>
                    <linearGradient id="yieldGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#16a34a" stopOpacity={0.3} />
                      <stop offset="100%" stopColor="#16a34a" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e7e5e4" vertical={false} />
                  <XAxis dataKey="month" tick={{ fontSize: 12, fill: '#78716c' }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fontSize: 12, fill: '#78716c' }} axisLine={false} tickLine={false} />
                  <Tooltip
                    contentStyle={{ borderRadius: '12px', border: '1px solid #e7e5e4', fontSize: '13px' }}
                    cursor={{ stroke: '#16a34a', strokeWidth: 1 }}
                  />
                  <Area type="monotone" dataKey="yield" stroke="#16a34a" strokeWidth={2} fill="url(#yieldGradient)" name="Yield (t/ha)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Soil nutrient levels */}
          <div className="card p-6">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <h3 className="text-base font-semibold text-earth-800">Soil Nutrient Levels</h3>
                <p className="text-xs text-earth-500">NPK values in kg/ha</p>
              </div>
              <Link to="/crop-recommendation" className="btn-ghost text-xs">
                Details <ArrowRight className="h-3 w-3" />
              </Link>
            </div>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <RadialBarChart data={soilData} innerRadius="25%" outerRadius="100%" startAngle={90} endAngle={-270}>
                  <PolarAngleAxis type="number" domain={[0, 140]} tick={false} />
                  <RadialBar dataKey="value" cornerRadius={10} background={{ fill: '#f5f5f4' }} />
                  <Tooltip
                    contentStyle={{ borderRadius: '12px', border: '1px solid #e7e5e4', fontSize: '13px' }}
                  />
                </RadialBarChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-2 flex justify-center gap-6">
              {soilData.map((s) => (
                <div key={s.name} className="flex items-center gap-2">
                  <span className="h-3 w-3 rounded-full" style={{ backgroundColor: s.fill }} />
                  <span className="text-xs text-earth-600">{s.name}: {s.value} kg/ha</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Environmental conditions */}
        <div className="mt-8 card p-6">
          <h3 className="mb-4 text-base font-semibold text-earth-800">Environmental Conditions</h3>
          <div className="grid gap-4 sm:grid-cols-3">
            <div className="flex items-center gap-4 rounded-xl bg-orange-50 p-4">
              <Thermometer className="h-8 w-8 text-orange-500" />
              <div>
                <p className="text-xs text-earth-500">Temperature</p>
                <p className="text-xl font-bold text-earth-800">27°C</p>
                <p className="text-xs text-primary-600">Optimal range</p>
              </div>
            </div>
            <div className="flex items-center gap-4 rounded-xl bg-accent-50 p-4">
              <Droplets className="h-8 w-8 text-accent-500" />
              <div>
                <p className="text-xs text-earth-500">Humidity</p>
                <p className="text-xl font-bold text-earth-800">72%</p>
                <p className="text-xs text-primary-600">Good for growth</p>
              </div>
            </div>
            <div className="flex items-center gap-4 rounded-xl bg-primary-50 p-4">
              <CloudSun className="h-8 w-8 text-primary-600" />
              <div>
                <p className="text-xs text-earth-500">Rainfall</p>
                <p className="text-xl font-bold text-earth-800">120 mm</p>
                <p className="text-xs text-primary-600">Adequate</p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick actions */}
        <div className="mt-8 card p-6">
          <h3 className="mb-4 text-base font-semibold text-earth-800">Quick Actions</h3>
          <div className="flex flex-wrap gap-3">
            <Link to="/crop-recommendation" className="btn-primary">Recommend Crop</Link>
            <Link to="/yield-prediction" className="btn-secondary">Predict Yield</Link>
            <Link to="/farmer-advisory" className="btn-secondary">Get Advisory</Link>
            <Link to="/weather-advisory" className="btn-secondary">Check Weather</Link>
          </div>
        </div>
      </div>
    </div>
  )
}
