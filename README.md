# Smart Crop Advisory and Recommendation System

An intelligent agricultural platform that uses Artificial Intelligence, Machine Learning, and environmental data to help farmers make better crop-related decisions. This repository contains the **frontend** application, built to be fully demonstrable on its own with mock data, and ready to connect to a Python FastAPI backend.

## Features

- **Crop Recommendation** — Enter soil nutrients (NPK), pH, temperature, humidity, and rainfall to get an AI-powered crop suggestion with confidence scores and environmental factor analysis.
- **Yield Prediction** — Predict expected crop yield based on crop type, area, rainfall, temperature, humidity, fertilizer usage, and season. Includes a yearly comparison chart.
- **Smart Farmer Advisory** — Get personalized crop care suggestions including growing conditions, soil management, watering schedules, and pest management advice.
- **Weather-Based Advisory** — View current weather conditions and receive agricultural advisories based on temperature, humidity, rainfall, and wind speed.
- **Dashboard** — A unified view of all recommendations, predictions, soil summaries, weather conditions, and advisories with visual charts.

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Framework | React 18 + TypeScript |
| Build Tool | Vite 5 |
| Styling | Tailwind CSS 3 |
| Routing | React Router DOM 6 |
| Charts | Recharts |
| Icons | Lucide React |
| Animations | CSS keyframes + Tailwind transitions |

## Frontend Setup Instructions

```bash
# 1. Install dependencies
npm install

# 2. Start the development server
npm run dev

# 3. Build for production
npm run build

# 4. Preview the production build
npm run preview
```

The dev server runs at `http://localhost:5173`.

## Environment Variables

Create a `.env` file in the project root:

```env
# Backend API base URL — leave empty to use mock data
VITE_API_BASE_URL=http://localhost:8000
```

When `VITE_API_BASE_URL` is **not set or empty**, the frontend automatically uses built-in mock data so all features remain demonstrable. When it is set, the app attempts to call the backend first and gracefully falls back to mock data if the backend is unreachable.

## API Integration Structure

The frontend uses a clean, reusable service layer:

```
src/
├── components/      # Reusable UI and layout components
│   ├── layout/     # Navbar, Footer, ScrollToTop, Logo
│   └── ui/         # FormInput, ResultCard, LoadingSpinner, etc.
├── pages/          # Route-level pages
│   ├── Home.tsx
│   ├── CropRecommendation.tsx
│   ├── YieldPrediction.tsx
│   ├── FarmerAdvisory.tsx
│   ├── WeatherAdvisory.tsx
│   └── Dashboard.tsx
├── services/       # API service layer
│   ├── apiClient.ts    # Central fetch wrapper with mock fallback
│   ├── cropService.ts  # POST /api/crop-recommendation
│   ├── yieldService.ts # POST /api/yield-prediction
│   ├── advisoryService.ts # POST /api/farmer-advisory
│   ├── weatherService.ts # GET /api/weather-advisory
│   ├── types.ts        # Shared TypeScript interfaces
│   └── index.ts        # Re-exports
├── hooks/          # Custom React hooks
│   ├── useAsync.ts     # Async state management
│   └── useForm.ts      # Form state + validation
├── App.tsx         # Route definitions
├── main.tsx        # App entry point
└── index.css       # Global styles + Tailwind
```

## Future Backend Integration Details

The frontend is designed to connect to a Python FastAPI backend. Each service function calls a specific endpoint:

| Feature | Endpoint | Method | Request Body |
|---------|----------|--------|-------------|
| Crop Recommendation | `/api/crop-recommendation` | POST | `{ nitrogen, phosphorus, potassium, ph, temperature, humidity, rainfall }` |
| Yield Prediction | `/api/yield-prediction` | POST | `{ crop, area, rainfall, temperature, humidity, fertilizer, season }` |
| Farmer Advisory | `/api/farmer-advisory` | POST | `{ crop, soilCondition, temperature, humidity, rainfall }` |
| Weather Advisory | `/api/weather-advisory` | GET | — |

### Expected Response Formats

**Crop Recommendation:**
```json
{
  "crop": "Rice",
  "confidence": 92,
  "keyFactors": [{ "factor": "Temperature", "value": "27°C", "impact": "Favorable for warm-season growth" }],
  "explanation": "Rice is recommended because...",
  "alternatives": [{ "crop": "Wheat", "suitability": 74 }]
}
```

**Yield Prediction:**
```json
{
  "crop": "Rice",
  "predictedYield": 2.4,
  "unit": "tonnes/hectare",
  "confidence": 88,
  "explanation": "Based on the provided inputs...",
  "factors": [{ "factor": "Rainfall", "status": "optimal", "detail": "200 mm — ideal for growth" }],
  "yearlyComparison": [{ "year": "2024", "yield": 2.4 }]
}
```

**Farmer Advisory:**
```json
{
  "crop": "Rice",
  "riskLevel": "Moderate",
  "summary": "Advisory for Rice under Loamy soil...",
  "advisories": [{ "category": "Irrigation", "title": "Watering Schedule", "advice": "...", "icon": "Droplets" }]
}
```

**Weather Advisory:**
```json
{
  "weather": { "temperature": 27, "humidity": 72, "rainfall": 120, "condition": "Partly Cloudy", "windSpeed": 12, "location": "Sample Region" },
  "advisories": [{ "title": "Rainfall is Adequate", "advice": "...", "severity": "success" }],
  "suitableCrops": ["Rice", "Wheat", "Maize", "Pulses"]
}
```

To connect the backend, simply set `VITE_API_BASE_URL` in `.env` to the FastAPI server URL. No frontend code changes are needed.
