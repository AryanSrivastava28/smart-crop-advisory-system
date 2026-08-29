"""
Weather Advisory Service

A rule-based system that generates agricultural advisories based on
weather data (temperature, humidity, rainfall, condition, wind speed).
If no weather data is provided, generates realistic sample data.
"""

import random


def _determine_condition(temperature, humidity, rainfall):
    """Determine a weather condition string from the values."""
    if rainfall > 150:
        return "Heavy Rain"
    elif rainfall > 100:
        return "Light Rain"
    elif temperature > 32:
        return "Sunny & Hot"
    elif humidity > 85:
        return "Humid & Cloudy"
    elif temperature < 15:
        return "Cool & Clear"
    else:
        return "Partly Cloudy"


def _build_advisories(temperature, humidity, rainfall):
    """Generate weather-based agricultural advisories."""
    advisories = []

    # Rainfall advisory
    if rainfall > 150:
        advisories.append({
            "title": "Heavy Rainfall Alert",
            "advice": "Ensure proper field drainage to prevent waterlogging. "
                      "Delay fertilizer application until rainfall subsides.",
            "severity": "warning",
        })
    elif rainfall < 50:
        advisories.append({
            "title": "Low Rainfall",
            "advice": "Increase irrigation frequency. Consider mulching to retain "
                      "soil moisture during dry conditions.",
            "severity": "warning",
        })
    else:
        advisories.append({
            "title": "Rainfall is Adequate",
            "advice": f"Current rainfall of {rainfall} mm supports normal crop growth. "
                      f"No additional irrigation needed for most crops.",
            "severity": "success",
        })

    # Temperature advisory
    if temperature > 32:
        advisories.append({
            "title": "High Temperature Warning",
            "advice": f"Temperature of {temperature}°C is high. Provide shade for "
                      f"sensitive crops. Increase watering frequency during peak heat hours.",
            "severity": "warning",
        })
    elif temperature < 10:
        advisories.append({
            "title": "Low Temperature Notice",
            "advice": f"Temperature of {temperature}°C is low. Protect crops with "
                      f"covers or row covers to prevent cold damage.",
            "severity": "warning",
        })
    else:
        advisories.append({
            "title": "Temperature is Favorable",
            "advice": f"{temperature}°C is within the optimal range for most crops. "
                      f"Good conditions for growth.",
            "severity": "success",
        })

    # Humidity advisory
    if humidity > 85:
        advisories.append({
            "title": "High Humidity Notice",
            "advice": f"Elevated humidity ({humidity}%) increases fungal disease risk. "
                      f"Monitor crops and apply preventive fungicide if needed.",
            "severity": "warning",
        })
    elif humidity < 40:
        advisories.append({
            "title": "Low Humidity Notice",
            "advice": f"Low humidity ({humidity}%) may cause water stress. "
                      f"Increase irrigation and use windbreaks to reduce evaporation.",
            "severity": "warning",
        })
    else:
        advisories.append({
            "title": "Humidity is Balanced",
            "advice": f"{humidity}% humidity is suitable for healthy crop development "
                      f"with low disease pressure.",
            "severity": "info",
        })

    return advisories


def _suitable_crops(temperature):
    """Suggest crops suitable for the current temperature."""
    if temperature > 28:
        return ["Rice", "Cotton", "Sugarcane", "Maize"]
    elif temperature < 22:
        return ["Wheat", "Tea", "Peas", "Mustard"]
    else:
        return ["Rice", "Wheat", "Maize", "Pulses"]


def get_weather_advisory(temperature=None, humidity=None, rainfall=None,
                         condition=None, windSpeed=None):
    """
    Generate a weather advisory response.
    If no weather data is provided, generate realistic sample data.
    """
    # Generate sample data if not provided
    if temperature is None:
        temperature = round(random.uniform(25, 33), 1)
    if humidity is None:
        humidity = round(random.uniform(55, 85), 1)
    if rainfall is None:
        rainfall = round(random.uniform(30, 200), 1)
    if windSpeed is None:
        windSpeed = round(random.uniform(5, 25), 1)

    if condition is None:
        condition = _determine_condition(temperature, humidity, rainfall)

    advisories = _build_advisories(temperature, humidity, rainfall)
    suitable = _suitable_crops(temperature)

    return {
        "weather": {
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall,
            "condition": condition,
            "windSpeed": windSpeed,
            "location": "Sample Region",
        },
        "advisories": advisories,
        "suitableCrops": suitable,
    }
