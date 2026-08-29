"""
Generate a Crop Yield Prediction Dataset.

This generates a realistic crop yield dataset with features matching the
frontend form: crop, area, rainfall, temperature, humidity, fertilizer,
season, and yield (target).

The yield values are based on documented average yields per crop from
FAO and Indian agricultural statistics, with environmental modifiers.

Run: python backend/training/generate_yield_dataset.py
"""

import os
import numpy as np
import pandas as pd

# Base yield in tonnes/hectare for each crop (FAO/Indian agriculture data)
CROP_BASE_YIELD = {
    "Rice": 2.4,
    "Wheat": 3.1,
    "Maize": 5.5,
    "Cotton": 1.8,
    "Tea": 1.5,
    "Sugarcane": 70.0,
    "Pulses": 0.9,
    "Soybean": 1.6,
}

# Season multipliers
SEASON_MULT = {"Kharif": 1.0, "Rabi": 0.95, "Zaid": 0.85}

# Ideal ranges for environmental factors
IDEAL_RANGES = {
    "rainfall": {"lo": 120, "hi": 250},
    "temperature": {"lo": 20, "hi": 32},
    "humidity": {"lo": 50, "hi": 80},
    "fertilizer": {"lo": 50, "hi": 150},
}

SAMPLES_PER_CROP = 200
np.random.seed(123)

DATASET_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "datasets"
)
OUTPUT_PATH = os.path.join(DATASET_DIR, "crop_yield_data.csv")


def environmental_factor(value, lo, hi):
    """Return a multiplier based on how close the value is to the ideal range."""
    if lo <= value <= hi:
        return 1.0 + np.random.uniform(0, 0.1)
    elif value < lo:
        # Below ideal — diminishing returns
        deficit = (lo - value) / lo
        return max(0.6, 1.0 - deficit * 0.4)
    else:
        # Above ideal — excess is harmful
        excess = (value - hi) / hi
        return max(0.7, 1.0 - excess * 0.3)


def generate():
    rows = []
    for crop, base_yield in CROP_BASE_YIELD.items():
        for season in SEASON_MULT:
            for _ in range(SAMPLES_PER_CROP // 3):
                rainfall = np.random.uniform(20, 400)
                temperature = np.random.uniform(10, 40)
                humidity = np.random.uniform(30, 95)
                fertilizer = np.random.uniform(0, 250)
                area = np.round(np.random.uniform(0.5, 20), 2)

                # Calculate yield with environmental modifiers
                rain_f = environmental_factor(rainfall, **IDEAL_RANGES["rainfall"])
                temp_f = environmental_factor(temperature, **IDEAL_RANGES["temperature"])
                hum_f = environmental_factor(humidity, **IDEAL_RANGES["humidity"])
                fert_f = environmental_factor(fertilizer, **IDEAL_RANGES["fertilizer"])
                season_f = SEASON_MULT[season]

                # Add small random noise
                noise = np.random.normal(1.0, 0.05)

                predicted_yield = base_yield * rain_f * temp_f * hum_f * fert_f * season_f * noise
                predicted_yield = max(0.1, predicted_yield)

                rows.append({
                    "crop": crop,
                    "area": area,
                    "rainfall": round(rainfall, 2),
                    "temperature": round(temperature, 2),
                    "humidity": round(humidity, 2),
                    "fertilizer": round(fertilizer, 2),
                    "season": season,
                    "yield": round(predicted_yield, 3),
                })

    df = pd.DataFrame(rows)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df


def main():
    os.makedirs(DATASET_DIR, exist_ok=True)
    df = generate()
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Dataset generated: {OUTPUT_PATH}")
    print(f"  Rows: {len(df)}")
    print(f"  Crops: {df['crop'].nunique()} ({df['crop'].unique().tolist()})")
    print(f"  Columns: {list(df.columns)}")
    print(f"\nSample:")
    print(df.head())
    print(f"\nYield stats:")
    print(df["yield"].describe())


if __name__ == "__main__":
    main()
