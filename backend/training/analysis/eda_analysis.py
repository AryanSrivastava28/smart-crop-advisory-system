"""
Exploratory Data Analysis (EDA) for Crop Recommendation & Yield Datasets
========================================================================

Performs a complete EDA on both datasets used in this project:
  1. Crop Recommendation Dataset (Crop_recommendation.csv)
     - 22 crops, 7 features (N, P, K, temperature, humidity, ph, rainfall)
  2. Crop Yield Dataset (crop_yield_data.csv)
     - 8 crops, 7 features (crop, area, rainfall, temperature, humidity,
       fertilizer, season) + target (yield)

Outputs:
  - Console report (shape, head, missing values, descriptive statistics)
  - Saved PNG visualizations under backend/training/analysis/eda_figures/

Run: python backend/training/analysis/eda_analysis.py
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "eda_figures")

CROP_CSV = os.path.join(DATASET_DIR, "Crop_recommendation.csv")
YIELD_CSV = os.path.join(DATASET_DIR, "crop_yield_data.csv")

sns.set_theme(style="whitegrid", palette="Set2")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. CROP RECOMMENDATION DATASET EDA
# ---------------------------------------------------------------------------
def eda_crop_recommendation():
    print("=" * 70)
    print("  EDA: Crop Recommendation Dataset")
    print("=" * 70)

    df = pd.read_csv(CROP_CSV)

    # --- Basic shape ---
    print(f"\nDataset shape: {df.shape}")
    print(f"  Rows (samples): {df.shape[0]}")
    print(f"  Columns (features + label): {df.shape[1]}")

    # --- First rows ---
    print("\nFirst 5 rows:")
    print(df.head())

    # --- Missing values ---
    print("\nMissing values per column:")
    missing = df.isnull().sum()
    print(missing)
    print(f"Total missing values: {missing.sum()}")

    # --- Descriptive statistics ---
    print("\nDescriptive statistics:")
    print(df.describe().round(2))

    # --- Class distribution ---
    print(f"\nNumber of crop classes: {df['label'].nunique()}")
    print("Samples per crop:")
    print(df['label'].value_counts())

    # --- Visualizations ---

    # 1a. Feature distributions (histograms)
    numeric_cols = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    fig, axes = plt.subplots(3, 3, figsize=(16, 12))
    axes = axes.flatten()
    for i, col in enumerate(numeric_cols):
        axes[i].hist(df[col], bins=30, color="#22c55e", edgecolor="white", alpha=0.8)
        axes[i].set_title(f"Distribution of {col}", fontsize=12, fontweight="bold")
        axes[i].set_xlabel(col)
        axes[i].set_ylabel("Frequency")
    # Hide unused subplots
    for j in range(len(numeric_cols), len(axes)):
        axes[j].set_visible(False)
    fig.suptitle("Crop Recommendation Dataset — Feature Distributions",
                fontsize=14, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(os.path.join(OUTPUT_DIR, "crop_feature_distributions.png"), dpi=150)
    plt.close(fig)
    print(f"\nSaved: crop_feature_distributions.png")

    # 1b. Correlation heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="YlGn", ax=ax,
                linewidths=0.5, square=True)
    ax.set_title("Crop Recommendation — Feature Correlation Heatmap",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "crop_correlation_heatmap.png"), dpi=150)
    plt.close(fig)
    print(f"Saved: crop_correlation_heatmap.png")

    # 1c. Crop class distribution bar chart
    fig, ax = plt.subplots(figsize=(12, 5))
    crop_counts = df['label'].value_counts()
    ax.bar(crop_counts.index, crop_counts.values, color="#16a34a", edgecolor="white")
    ax.set_title("Crop Recommendation — Samples per Crop Class",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Crop")
    ax.set_ylabel("Number of Samples")
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "crop_class_distribution.png"), dpi=150)
    plt.close(fig)
    print(f"Saved: crop_class_distribution.png")

    # 1d. Boxplots of features by crop (top 6 crops for readability)
    top_crops = df['label'].value_counts().head(6).index.tolist()
    df_top = df[df['label'].isin(top_crops)]
    fig, axes = plt.subplots(2, 4, figsize=(18, 8))
    axes = axes.flatten()
    for i, col in enumerate(numeric_cols):
        sns.boxplot(data=df_top, x='label', y=col, ax=axes[i], palette="Set2")
        axes[i].set_title(f"{col} by Crop", fontsize=11, fontweight="bold")
        axes[i].tick_params(axis='x', rotation=30)
    for j in range(len(numeric_cols), len(axes)):
        axes[j].set_visible(False)
    fig.suptitle("Crop Recommendation — Feature Boxplots (Top 6 Crops)",
                fontsize=14, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(os.path.join(OUTPUT_DIR, "crop_boxplots.png"), dpi=150)
    plt.close(fig)
    print(f"Saved: crop_boxplots.png")


# ---------------------------------------------------------------------------
# 2. CROP YIELD DATASET EDA
# ---------------------------------------------------------------------------
def eda_crop_yield():
    print("\n" + "=" * 70)
    print("  EDA: Crop Yield Dataset")
    print("=" * 70)

    df = pd.read_csv(YIELD_CSV)

    # --- Basic shape ---
    print(f"\nDataset shape: {df.shape}")
    print(f"  Rows (samples): {df.shape[0]}")
    print(f"  Columns (features + target): {df.shape[1]}")

    # --- First rows ---
    print("\nFirst 5 rows:")
    print(df.head())

    # --- Missing values ---
    print("\nMissing values per column:")
    missing = df.isnull().sum()
    print(missing)
    print(f"Total missing values: {missing.sum()}")

    # --- Descriptive statistics ---
    print("\nDescriptive statistics:")
    print(df.describe().round(2))

    # --- Categorical feature distributions ---
    print(f"\nCrops: {df['crop'].nunique()} — {df['crop'].unique().tolist()}")
    print(f"Seasons: {df['season'].nunique()} — {df['season'].unique().tolist()}")
    print("\nSamples per crop:")
    print(df['crop'].value_counts())
    print("\nSamples per season:")
    print(df['season'].value_counts())

    # --- Visualizations ---

    numeric_cols = ["area", "rainfall", "temperature", "humidity",
                   "fertilizer", "yield"]

    # 2a. Feature distributions
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()
    for i, col in enumerate(numeric_cols):
        axes[i].hist(df[col], bins=30, color="#f59e0b", edgecolor="white", alpha=0.8)
        axes[i].set_title(f"Distribution of {col}", fontsize=12, fontweight="bold")
        axes[i].set_xlabel(col)
        axes[i].set_ylabel("Frequency")
    fig.suptitle("Crop Yield Dataset — Feature Distributions",
                fontsize=14, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(os.path.join(OUTPUT_DIR, "yield_feature_distributions.png"), dpi=150)
    plt.close(fig)
    print(f"\nSaved: yield_feature_distributions.png")

    # 2b. Correlation heatmap (numeric features only)
    fig, ax = plt.subplots(figsize=(8, 6))
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="YlOrBr", ax=ax,
                linewidths=0.5, square=True)
    ax.set_title("Crop Yield — Feature Correlation Heatmap",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "yield_correlation_heatmap.png"), dpi=150)
    plt.close(fig)
    print(f"Saved: yield_correlation_heatmap.png")

    # 2c. Yield by crop (boxplot)
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.boxplot(data=df, x='crop', y='yield', ax=ax, palette="Set2")
    ax.set_title("Crop Yield — Yield Distribution by Crop",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Crop")
    ax.set_ylabel("Yield (tonnes/hectare)")
    ax.tick_params(axis='x', rotation=30)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "yield_by_crop.png"), dpi=150)
    plt.close(fig)
    print(f"Saved: yield_by_crop.png")

    # 2d. Yield by season (boxplot)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x='season', y='yield', ax=ax, palette="Set3")
    ax.set_title("Crop Yield — Yield Distribution by Season",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Season")
    ax.set_ylabel("Yield (tonnes/hectare)")
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "yield_by_season.png"), dpi=150)
    plt.close(fig)
    print(f"Saved: yield_by_season.png")

    # 2e. Pairplot of key numeric features colored by crop
    pair = sns.pairplot(
        df[["rainfall", "temperature", "humidity", "fertilizer", "yield", "crop"]],
        hue="crop", diag_kind="kde", plot_kws={"s": 10, "alpha": 0.6},
        corner=True,
    )
    pair.fig.suptitle("Crop Yield — Pairplot by Crop", fontsize=14,
                      fontweight="bold", y=1.02)
    pair.savefig(os.path.join(OUTPUT_DIR, "yield_pairplot.png"), dpi=150)
    plt.close(pair.fig)
    print(f"Saved: yield_pairplot.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    eda_crop_recommendation()
    eda_crop_yield()
    print("\n" + "=" * 70)
    print("  EDA complete. All figures saved to:")
    print(f"  {OUTPUT_DIR}")
    print("=" * 70)
