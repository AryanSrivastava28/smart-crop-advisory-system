import { Routes, Route } from 'react-router-dom'
import Navbar from './components/layout/Navbar'
import Footer from './components/layout/Footer'
import ScrollToTop from './components/layout/ScrollToTop'
import Home from './pages/Home'
import CropRecommendation from './pages/CropRecommendation'
import YieldPrediction from './pages/YieldPrediction'
import FarmerAdvisory from './pages/FarmerAdvisory'
import WeatherAdvisory from './pages/WeatherAdvisory'
import Dashboard from './pages/Dashboard'

export default function App() {
  return (
    <div className="flex min-h-screen flex-col">
      <ScrollToTop />
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/crop-recommendation" element={<CropRecommendation />} />
          <Route path="/yield-prediction" element={<YieldPrediction />} />
          <Route path="/farmer-advisory" element={<FarmerAdvisory />} />
          <Route path="/weather-advisory" element={<WeatherAdvisory />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </main>
      <Footer />
    </div>
  )
}
