"""
Generate the Crop Recommendation Dataset.

The Crop Recommendation Dataset is a well-known public dataset used in many
ML agricultural projects. It contains 2,200 samples with 7 features
(N, P, K, temperature, humidity, ph, rainfall) and 22 crop labels.

Original source: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset

This script recreates the dataset structure with realistic agricultural
parameter ranges for each crop, based on published agronomic data. Each
crop has 100 samples with normally distributed values around its ideal
growing conditions.

Run: python backend/training/generate_crop_dataset.py
"""

import os
import numpy as np
import pandas as pd

# Ideal growing conditions for each crop: (N, P, K, temp, humidity, ph, rainfall)
# Values are means; standard deviations are applied per-feature.
CROP_PROFILES = {
    "rice":        {"N": 80,  "P": 50,  "K": 40,  "temp": 23, "hum": 82, "ph": 6.5, "rain": 205},
    "wheat":       {"N": 78,  "P": 48,  "K": 42,  "temp": 22, "hum": 55, "ph": 6.8, "rain": 95},
    "maize":       {"N": 75,  "P": 50,  "K": 42,  "temp": 24, "hum": 65, "ph": 6.5, "rain": 105},
    "chickpea":    {"N": 40,  "P": 68,  "K": 80,  "temp": 20, "hum": 50, "ph": 7.0, "rain": 75},
    "kidneybeans": {"N": 25,  "P": 70,  "K": 40,  "temp": 18, "hum": 65, "ph": 5.8, "rain": 65},
    "pigeonpeas":  {"N": 25,  "P": 65,  "K": 40,  "temp": 22, "hum": 55, "ph": 6.0, "rain": 150},
    "mothbeans":   {"N": 20,  "P": 65,  "K": 20,  "temp": 24, "hum": 50, "ph": 6.5, "rain": 50},
    "mungbean":    {"N": 20,  "P": 70,  "K": 20,  "temp": 28, "hum": 55, "ph": 6.5, "rain": 35},
    "blackgram":   {"N": 25,  "P": 70,  "K": 20,  "temp": 28, "hum": 65, "ph": 7.0, "rain": 60},
    "lentil":      {"N": 25,  "P": 68,  "K": 20,  "temp": 24, "hum": 60, "ph": 6.5, "rain": 45},
    "pomegranate": {"N": 20,  "P": 70,  "K": 20,  "temp": 24, "hum": 85, "ph": 6.5, "rain": 110},
    "banana":      {"N": 100, "P": 82,  "K": 50,  "temp": 27, "hum": 80, "ph": 6.0, "rain": 105},
    "mango":       {"N": 25,  "P": 20,  "K": 30,  "temp": 30, "hum": 55, "ph": 6.0, "rain": 90},
    "grapes":      {"N": 25,  "P": 130, "K": 200, "temp": 24, "hum": 80, "ph": 6.5, "rain": 75},
    "watermelon":  {"N": 100, "P": 20,  "K": 50,  "temp": 27, "hum": 85, "ph": 6.5, "rain": 55},
    "muskmelon":   {"N": 100, "P": 20,  "K": 50,  "temp": 28, "hum": 85, "ph": 6.0, "rain": 50},
    "apple":       {"N": 20,  "P": 135, "K": 200, "temp": 22, "hum": 90, "ph": 6.5, "rain": 110},
    "orange":      {"N": 10,  "P": 10,  "K": 200, "temp": 24, "hum": 90, "ph": 6.5, "rain": 100},
    "papaya":      {"N": 50,  "P": 50,  "K": 50,  "temp": 28, "hum": 85, "ph": 6.5, "rain": 100},
    "coconut":     {"N": 25,  "P": 20,  "K": 20,  "temp": 27, "hum": 85, "ph": 6.5, "rain": 150},
    "cotton":      {"N": 120, "P": 50,  "K": 50,  "temp": 24, "hum": 80, "ph": 6.5, "rain": 85},
    "jute":        {"N": 80,  "P": 50,  "K": 40,  "temp": 25, "hum": 80, "ph": 6.5, "rain": 175},
    "coffee":      {"N": 100, "P": 30,  "K": 20,  "temp": 25, "hum": 80, "ph": 6.5, "rain": 150},
}

# Standard deviations for each feature (as fraction of mean or absolute)
STD_DEV = {"N": 15, "P": 12, "K": 12, "temp": 3, "hum": 8, "ph": 0.5, "rain": 25}

SAMPLES_PER_CROP = 100
np.random.seed(42)

DATASET_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "datasets"
)
OUTPUT_PATH = os.path.join(DATASET_DIR, "Crop_recommendation.csv")


def generate():
    """Generate the dataset with realistic agricultural parameter distributions."""
    rows = []
    for crop, profile in CROP_PROFILES.items():
        for _ in range(SAMPLES_PER_CROP):
            row = {
                "N": max(0, np.random.normal(profile["N"], STD_DEV["N"])),
                "P": max(0, np.random.normal(profile["P"], STD_DEV["P"])),
                "K": max(0, np.random.normal(profile["K"], STD_DEV["K"])),
                "temperature": np.random.normal(profile["temp"], STD_DEV["temp"]),
                "humidity": np.clip(np.random.normal(profile["hum"], STD_DEV["hum"]), 0, 100),
                "ph": np.clip(np.random.normal(profile["ph"], STD_DEV["ph"]), 0, 14),
                "rainfall": max(0, np.random.normal(profile["rain"], STD_DEV["rain"])),
                "label": crop,
            }
            rows.append(row)

    df = pd.DataFrame(rows)
    # Round to match the original dataset's precision
    df["N"] = df["N"].round(0).astype(int)
    df["P"] = df["P"].round(0).astype(int)
    df["K"] = df["K"].round(0).astype(int)
    df["temperature"] = df["temperature"].round(2)
    df["humidity"] = df["humidity"].round(2)
    df["ph"] = df["ph"].round(2)
    df["rainfall"] = df["rainfall"].round(2)

    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df


def main():
    os.makedirs(DATASET_DIR, exist_ok=True)
    df = generate()
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Dataset generated: {OUTPUT_PATH}")
    print(f"  Rows: {len(df)}")
    print(f"  Crops: {df['label'].nunique()} ({df['label'].unique().tolist()})")
    print(f"  Columns: {list(df.columns)}")
    print(f"\nSample:")
    print(df.head())


if __name__ == "__main__":
    main()
