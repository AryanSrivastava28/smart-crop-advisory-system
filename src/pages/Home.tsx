import { Link } from 'react-router-dom'
import { Sprout, TrendingUp, CloudSun, FlaskConical, Lightbulb, ArrowRight, Database, Brain, Cpu, ChartColumn, CircleCheck as CheckCircle2 } from 'lucide-react'
import FeatureCard from '../components/ui/FeatureCard'

const features = [
  {
    icon: Sprout,
    title: 'Crop Recommendation',
    description: 'Get AI-powered crop suggestions based on your soil nutrients, pH, temperature, humidity, and rainfall data.',
    to: '/crop-recommendation',
  },
  {
    icon: TrendingUp,
    title: 'Yield Prediction',
    description: 'Predict expected crop yield using machine learning models that analyze environmental and agricultural inputs.',
    to: '/yield-prediction',
  },
  {
    icon: CloudSun,
    title: 'Weather-Based Advisory',
    description: 'Receive real-time agricultural advice based on current weather conditions and their impact on crops.',
    to: '/weather-advisory',
  },
  {
    icon: FlaskConical,
    title: 'Soil Analysis',
    description: 'Analyze soil health through NPK values, pH levels, and environmental data to make informed farming decisions.',
    to: '/crop-recommendation',
  },
  {
    icon: Lightbulb,
    title: 'Smart Farming Suggestions',
    description: 'Get personalized crop care tips, watering schedules, and pest management advice from our advisory engine.',
    to: '/farmer-advisory',
  },
  {
    icon: ChartColumn,
    title: 'Unified Dashboard',
    description: 'View all your predictions, recommendations, and advisories in one comprehensive dashboard with visual charts.',
    to: '/dashboard',
  },
]

const steps = [
  { icon: Database, title: 'Enter Agricultural Data', description: 'Input soil nutrients (NPK), pH, temperature, humidity, rainfall, and crop details.' },
  { icon: Cpu, title: 'AI Analysis', description: 'Our ML models process your data using trained algorithms to identify optimal patterns.' },
  { icon: Sprout, title: 'Crop Recommendation', description: 'Receive the best crop suggestion with confidence scores and environmental factor analysis.' },
  { icon: TrendingUp, title: 'Yield Prediction', description: 'Get predicted yield estimates with yearly comparisons and contributing factor breakdowns.' },
  { icon: Lightbulb, title: 'Smart Advisory', description: 'Access tailored crop care, irrigation, and pest management advice for your conditions.' },
]

const heroImage = 'https://images.pexels.com/photos/38534084/pexels-photo-38534084.jpeg?auto=compress&cs=tinysrgb&h=650&w=940'
const techImage = 'https://images.pexels.com/photos/4975400/pexels-photo-4975400.jpeg?auto=compress&cs=tinysrgb&h=650&w=940'

export default function Home() {
  return (
    <div className="animate-fade-in">
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary-50 via-white to-accent-50">
        <div className="absolute inset-0 opacity-5" style={{
          backgroundImage: 'radial-gradient(circle at 1px 1px, #16a34a 1px, transparent 0)',
          backgroundSize: '32px 32px',
        }} />
        <div className="section-container relative grid items-center gap-12 py-16 lg:grid-cols-2 lg:py-24">
          <div className="animate-fade-in-up">
            <span className="badge bg-primary-100 text-primary-700">
              <Brain className="h-3.5 w-3.5" /> AI-Powered Agriculture
            </span>
            <h1 className="mt-4 text-4xl font-bold leading-tight text-earth-800 sm:text-5xl lg:text-6xl">
              Smart Crop Advisory &<br />
              <span className="text-gradient">Recommendation System</span>
            </h1>
            <p className="mt-6 max-w-xl text-base leading-relaxed text-earth-600 sm:text-lg">
              An intelligent agricultural platform that uses Artificial
              Intelligence, Machine Learning, and environmental data to help
              farmers make better crop-related decisions — from choosing the
              right crop to predicting yield and receiving smart advisories.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Link to="/crop-recommendation" className="btn-primary">
                Get Started <ArrowRight className="h-4 w-4" />
              </Link>
              <Link to="/dashboard" className="btn-secondary">
                View Dashboard
              </Link>
            </div>
            <div className="mt-10 flex flex-wrap gap-6 text-sm text-earth-500">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-primary-500" /> Crop Recommendation
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-primary-500" /> Yield Prediction
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-primary-500" /> Weather Advisory
              </div>
            </div>
          </div>

          <div className="relative animate-fade-in-up" style={{ animationDelay: '200ms' }}>
            <div className="overflow-hidden rounded-3xl shadow-2xl shadow-primary-900/10">
              <img
                src={heroImage}
                alt="Green agricultural field"
                className="h-full w-full object-cover"
                loading="eager"
              />
            </div>
            <div className="absolute -bottom-5 -left-5 hidden rounded-2xl bg-white p-4 shadow-xl sm:block">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary-600 text-white">
                  <Sprout className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-sm font-bold text-earth-800">AI + Agriculture</p>
                  <p className="text-xs text-earth-500">Smarter farming</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="section-container py-16 lg:py-24">
        <div className="mx-auto max-w-2xl text-center">
          <span className="badge bg-accent-50 text-accent-600">Features</span>
          <h2 className="mt-4 text-3xl font-bold text-earth-800 sm:text-4xl">
            Everything you need for smarter farming
          </h2>
          <p className="mt-4 text-base text-earth-500">
            Our platform brings together machine learning, environmental data,
            and agricultural expertise to support every stage of the farming
            decision process.
          </p>
        </div>

        <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((f, i) => (
            <FeatureCard key={f.title} {...f} delay={i * 80} />
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-gradient-to-br from-earth-50 to-primary-50/30 py-16 lg:py-24">
        <div className="section-container">
          <div className="mx-auto max-w-2xl text-center">
            <span className="badge bg-primary-100 text-primary-700">How It Works</span>
            <h2 className="mt-4 text-3xl font-bold text-earth-800 sm:text-4xl">
              From data to decision in five steps
            </h2>
            <p className="mt-4 text-base text-earth-500">
              A simple, guided flow that takes your agricultural data and
              transforms it into actionable insights.
            </p>
          </div>

          <div className="mt-14">
            <div className="grid gap-8 lg:grid-cols-5">
              {steps.map((step, i) => (
                <div key={step.title} className="relative">
                  <div className="card card-hover flex flex-col items-center p-6 text-center">
                    <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary-600 text-white shadow-lg shadow-primary-600/20">
                      <step.icon className="h-6 w-6" />
                    </div>
                    <span className="mt-4 text-xs font-bold text-primary-500">
                      STEP {i + 1}
                    </span>
                    <h3 className="mt-1 text-sm font-semibold text-earth-800">{step.title}</h3>
                    <p className="mt-2 text-xs leading-relaxed text-earth-500">{step.description}</p>
                  </div>
                  {i < steps.length - 1 && (
                    <div className="absolute -right-4 top-1/2 hidden -translate-y-1/2 text-primary-300 lg:block">
                      <ArrowRight className="h-5 w-5" />
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Technology section */}
      <section className="section-container py-16 lg:py-24">
        <div className="grid items-center gap-12 lg:grid-cols-2">
          <div className="relative order-2 lg:order-1">
            <div className="overflow-hidden rounded-3xl shadow-2xl shadow-primary-900/10">
              <img
                src={techImage}
                alt="Farmer using technology in the field"
                className="h-full w-full object-cover"
                loading="lazy"
              />
            </div>
          </div>
          <div className="order-1 lg:order-2">
            <span className="badge bg-accent-50 text-accent-600">Technology</span>
            <h2 className="mt-4 text-3xl font-bold text-earth-800 sm:text-4xl">
              Powered by Machine Learning
            </h2>
            <p className="mt-4 text-base leading-relaxed text-earth-500">
              Our system leverages trained ML/DL models to analyze soil
              composition, weather patterns, and historical crop data. The
              frontend is designed to connect seamlessly with a Python FastAPI
              backend that hosts the actual prediction models.
            </p>
            <ul className="mt-8 space-y-4">
              {[
                { icon: Brain, text: 'ML models for crop recommendation based on NPK and environmental data' },
                { icon: TrendingUp, text: 'Deep learning yield prediction using historical and current inputs' },
                { icon: CloudSun, text: 'Real-time weather integration for context-aware advisories' },
                { icon: Lightbulb, text: 'Intelligent advisory engine for crop care and pest management' },
              ].map((item) => (
                <li key={item.text} className="flex items-start gap-3">
                  <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary-50 text-primary-600">
                    <item.icon className="h-4 w-4" />
                  </div>
                  <span className="text-sm text-earth-600">{item.text}</span>
                </li>
              ))}
            </ul>
            <Link to="/crop-recommendation" className="btn-primary mt-8">
              Try It Now <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-gradient-to-r from-primary-600 to-primary-700 py-16">
        <div className="section-container text-center">
          <h2 className="text-3xl font-bold text-white sm:text-4xl">
            Ready to make smarter farming decisions?
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-base text-primary-50">
            Start by entering your agricultural data and let our AI-powered
            system guide you to the best crop choices and yield predictions.
          </p>
          <Link
            to="/crop-recommendation"
            className="mt-8 inline-flex items-center justify-center gap-2 rounded-xl bg-white px-8 py-3.5 text-sm font-semibold text-primary-700 shadow-lg transition-all hover:bg-primary-50 hover:shadow-xl active:scale-[0.98]"
          >
            Get Started <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </section>
    </div>
  )
}
