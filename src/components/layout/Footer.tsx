import { Link } from 'react-router-dom'
import { Leaf, Github, Mail } from 'lucide-react'
import Logo from './Logo'

export default function Footer() {
  return (
    <footer className="border-t border-earth-200 bg-white">
      <div className="section-container py-12">
        <div className="grid gap-8 md:grid-cols-3">
          {/* Brand */}
          <div>
            <Link to="/" className="flex items-center gap-2 text-primary-700">
              <Logo />
              <span className="font-display text-sm font-bold">
                Smart Crop Advisory
              </span>
            </Link>
            <p className="mt-4 max-w-xs text-sm leading-relaxed text-earth-500">
              An intelligent agricultural platform using AI, Machine Learning,
              and environmental data to help farmers make better crop-related
              decisions.
            </p>
          </div>

          {/* Quick links */}
          <div>
            <h4 className="text-sm font-semibold text-earth-800">Explore</h4>
            <ul className="mt-4 space-y-2 text-sm">
              <li>
                <Link to="/crop-recommendation" className="text-earth-500 transition-colors hover:text-primary-600">
                  Crop Recommendation
                </Link>
              </li>
              <li>
                <Link to="/yield-prediction" className="text-earth-500 transition-colors hover:text-primary-600">
                  Yield Prediction
                </Link>
              </li>
              <li>
                <Link to="/farmer-advisory" className="text-earth-500 transition-colors hover:text-primary-600">
                  Farmer Advisory
                </Link>
              </li>
              <li>
                <Link to="/weather-advisory" className="text-earth-500 transition-colors hover:text-primary-600">
                  Weather Advisory
                </Link>
              </li>
              <li>
                <Link to="/dashboard" className="text-earth-500 transition-colors hover:text-primary-600">
                  Dashboard
                </Link>
              </li>
            </ul>
          </div>

          {/* Project info */}
          <div>
            <h4 className="text-sm font-semibold text-earth-800">Project</h4>
            <p className="mt-4 text-sm text-earth-500">
              Smart Crop Advisory and Recommendation System — a college mini
              project demonstrating AI/ML integration in agriculture.
            </p>
            <div className="mt-4 flex gap-3">
              <a
                href="#"
                className="flex h-9 w-9 items-center justify-center rounded-lg bg-earth-100 text-earth-600 transition-colors hover:bg-primary-50 hover:text-primary-600"
                aria-label="GitHub"
              >
                <Github className="h-4 w-4" />
              </a>
              <a
                href="#"
                className="flex h-9 w-9 items-center justify-center rounded-lg bg-earth-100 text-earth-600 transition-colors hover:bg-primary-50 hover:text-primary-600"
                aria-label="Email"
              >
                <Mail className="h-4 w-4" />
              </a>
              <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-earth-100 text-earth-600">
                <Leaf className="h-4 w-4" />
              </span>
            </div>
          </div>
        </div>

        <div className="mt-10 border-t border-earth-200 pt-6 text-center text-xs text-earth-400">
          © {new Date().getFullYear()} Smart Crop Advisory and Recommendation
          System. Built for educational purposes.
        </div>
      </div>
    </footer>
  )
}
