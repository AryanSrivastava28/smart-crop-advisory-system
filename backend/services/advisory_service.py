"""
Farmer Advisory Service

A rule-based advisory system that generates crop care suggestions
based on the user's input (crop, soil condition, temperature, humidity, rainfall).
"""

# Optimal growing conditions for common crops
CROP_OPTIMAL = {
    "Rice":       {"temp_lo": 20, "temp_hi": 30, "hum_lo": 70, "hum_hi": 90, "rain_lo": 150, "rain_hi": 300},
    "Wheat":      {"temp_lo": 15, "temp_hi": 25, "hum_lo": 40, "hum_hi": 65, "rain_lo": 50,  "rain_hi": 120},
    "Maize":      {"temp_lo": 18, "temp_hi": 32, "hum_lo": 50, "hum_hi": 75, "rain_lo": 60,  "rain_hi": 150},
    "Cotton":     {"temp_lo": 22, "temp_hi": 35, "hum_lo": 50, "hum_hi": 75, "rain_lo": 50,  "rain_hi": 120},
    "Tea":       {"temp_lo": 18, "temp_hi": 28, "hum_lo": 70, "hum_hi": 90, "rain_lo": 120, "rain_hi": 250},
    "Sugarcane":  {"temp_lo": 22, "temp_hi": 35, "hum_lo": 70, "hum_hi": 90, "rain_lo": 100, "rain_hi": 200},
    "Pulses":    {"temp_lo": 18, "temp_hi": 30, "hum_lo": 40, "hum_hi": 65, "rain_lo": 40,  "rain_hi": 100},
    "Soybean":   {"temp_lo": 20, "temp_hi": 32, "hum_lo": 50, "hum_hi": 75, "rain_lo": 60,  "rain_hi": 120},
}

DEFAULT_OPTIMAL = {"temp_lo": 20, "temp_hi": 30, "hum_lo": 50, "hum_hi": 80, "rain_lo": 80, "rain_hi": 200}


def _get_optimal(crop):
    return CROP_OPTIMAL.get(crop, DEFAULT_OPTIMAL)


def _assess_risk(temperature, humidity):
    """Determine overall risk level based on extreme conditions."""
    if temperature > 35 or humidity > 90 or temperature < 5:
        return "High"
    if temperature > 30 or humidity > 80:
        return "Moderate"
    return "Low"


def _temp_advice(crop, temperature, optimal):
    if temperature > optimal["temp_hi"]:
        return (f"{crop} thrives in {optimal['temp_lo']}-{optimal['temp_hi']}°C. "
                f"Current temperature of {temperature}°C is above optimal — "
                f"consider afternoon shading and increased watering.")
    elif temperature < optimal["temp_lo"]:
        return (f"{crop} thrives in {optimal['temp_lo']}-{optimal['temp_hi']}°C. "
                f"Current temperature of {temperature}°C is below optimal — "
                f"monitor growth rate and consider protective covers.")
    else:
        return (f"{crop} thrives in {optimal['temp_lo']}-{optimal['temp_hi']}°C. "
                f"Current temperature of {temperature}°C is within the ideal range. "
                f"Maintain consistent conditions for best results.")


def _soil_advice(soil_condition, rainfall):
    base = f"{soil_condition} soil detected. "
    if soil_condition.lower() == "clay":
        base += "Ensure proper drainage to prevent waterlogging. "
    elif soil_condition.lower() == "sandy":
        base += "Add organic matter to improve water retention. "
    elif soil_condition.lower() == "loamy":
        base += "This is an excellent soil type for most crops. "
    base += f"With {rainfall} mm rainfall, "
    if rainfall > 200:
        base += "ensure field drainage channels are clear."
    else:
        base += "monitor soil moisture and irrigate as needed."
    base += " Test soil pH every 2-3 months."
    return base


def _irrigation_advice(rainfall, humidity):
    if rainfall > 150:
        return (f"With {rainfall} mm rainfall and {humidity}% humidity, "
                f"reduce supplemental irrigation — natural rainfall is sufficient. "
                f"Water early morning or late evening to minimize evaporation loss.")
    elif rainfall < 50:
        return (f"With only {rainfall} mm rainfall, irrigate 3-4 times per week. "
                f"Apply mulching to retain soil moisture. "
                f"Water early morning or late evening to minimize evaporation loss.")
    else:
        return (f"With {rainfall} mm rainfall and {humidity}% humidity, "
                f"irrigate 2-3 times per week. "
                f"Water early morning or late evening to minimize evaporation loss.")


def _pest_advice(crop, humidity):
    if humidity > 80:
        return (f"High humidity ({humidity}%) increases fungal disease risk — "
                f"apply preventive fungicide and ensure good air circulation. "
                f"Monitor for common {crop} pests and use integrated pest management practices.")
    elif humidity < 40:
        return (f"Low humidity ({humidity}%) may stress plants — monitor for spider mites. "
                f"Use integrated pest management practices for {crop}.")
    else:
        return (f"Humidity is moderate ({humidity}%) — maintain regular scouting for pests. "
                f"Monitor for common {crop} pests and use integrated pest management practices.")


def _fertilizer_advice(crop, soil_condition):
    return (f"Apply balanced NPK fertilizer based on soil test results. "
            f"For {crop} in {soil_condition} soil, split applications into 2-3 doses "
            f"throughout the growing season for efficient nutrient uptake.")


def get_advisory(crop, soil_condition, temperature, humidity, rainfall):
    """Generate a complete farmer advisory response."""
    optimal = _get_optimal(crop)
    risk = _assess_risk(temperature, humidity)

    summary = (
        f"Advisory for {crop} under {soil_condition} soil conditions. "
        f"Current temperature is {temperature}°C with {humidity}% humidity "
        f"and {rainfall} mm rainfall. Overall risk level: {risk}."
    )

    advisories = [
        {
            "category": "Growing Conditions",
            "title": "Optimal Growing Environment",
            "advice": _temp_advice(crop, temperature, optimal),
            "icon": "Sprout",
        },
        {
            "category": "Soil Management",
            "title": "Soil Health Recommendations",
            "advice": _soil_advice(soil_condition, rainfall),
            "icon": "Layers",
        },
        {
            "category": "Irrigation",
            "title": "Watering Schedule",
            "advice": _irrigation_advice(rainfall, humidity),
            "icon": "Droplets",
        },
        {
            "category": "Crop Care",
            "title": "Pest & Disease Management",
            "advice": _pest_advice(crop, humidity),
            "icon": "ShieldCheck",
        },
        {
            "category": "Fertilization",
            "title": "Nutrient Management",
            "advice": _fertilizer_advice(crop, soil_condition),
            "icon": "FlaskConical",
        },
    ]

    return {
        "crop": crop,
        "riskLevel": risk,
        "summary": summary,
        "advisories": advisories,
    }
