"""
ML Baseline vs Deep Learning Comparison for Crop Yield Prediction
===================================================================

Trains three baseline ML models (Linear Regression, Random Forest, Gradient
Boosting) on the same yield dataset and compares them with the trained Keras
deep learning model.

Outputs:
  - Console report with metrics table (MAE, RMSE, R2) for all models
  - Saved PNG bar chart comparing metrics under
    backend/training/analysis/baseline_figures/

Run: python backend/training/analysis/baseline_comparison.py
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf
from tensorflow import keras

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")
MODEL_DIR = os.path.join(BASE_DIR, "ml_models")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "baseline_figures")

YIELD_CSV = os.path.join(DATASET_DIR, "crop_yield_data.csv")

NUMERICAL_FEATURES = ["area", "rainfall", "temperature", "humidity", "fertilizer"]
CATEGORICAL_FEATURES = ["crop", "season"]
TARGET = "yield"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_and_preprocess():
    """Load dataset and apply the same preprocessing as the DL training script."""
    df = pd.read_csv(YIELD_CSV)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    # One-hot encode categorical features
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    cat_encoded = encoder.fit_transform(df[CATEGORICAL_FEATURES])
    cat_columns = encoder.get_feature_names_out(CATEGORICAL_FEATURES).tolist()
    cat_df = pd.DataFrame(cat_encoded, columns=cat_columns, index=df.index)

    # Normalize numerical features
    scaler = StandardScaler()
    num_scaled = scaler.fit_transform(df[NUMERICAL_FEATURES])
    num_df = pd.DataFrame(num_scaled, columns=NUMERICAL_FEATURES, index=df.index)

    X = pd.concat([num_df, cat_df], axis=1)
    y = df[TARGET].values

    X_train, X_test, y_train, y_test = train_test_split(
        X.values, y, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test


def train_baselines(X_train, X_test, y_train, y_test):
    """Train three ML baseline models and return their metrics."""
    baselines = {}

    # 1. Linear Regression
    print("\n--- Training Linear Regression ---")
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)
    baselines["Linear Regression"] = {
        "mae": mean_absolute_error(y_test, lr_pred),
        "rmse": np.sqrt(mean_squared_error(y_test, lr_pred)),
        "r2": r2_score(y_test, lr_pred),
    }

    # 2. Random Forest Regressor
    print("--- Training Random Forest Regressor ---")
    rf = RandomForestRegressor(n_estimators=100, max_depth=15,
                               random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    baselines["Random Forest"] = {
        "mae": mean_absolute_error(y_test, rf_pred),
        "rmse": np.sqrt(mean_squared_error(y_test, rf_pred)),
        "r2": r2_score(y_test, rf_pred),
    }

    # 3. Gradient Boosting Regressor
    print("--- Training Gradient Boosting Regressor ---")
    gb = GradientBoostingRegressor(n_estimators=100, max_depth=5,
                                   random_state=42)
    gb.fit(X_train, y_train)
    gb_pred = gb.predict(X_test)
    baselines["Gradient Boosting"] = {
        "mae": mean_absolute_error(y_test, gb_pred),
        "rmse": np.sqrt(mean_squared_error(y_test, gb_pred)),
        "r2": r2_score(y_test, gb_pred),
    }

    return baselines


def evaluate_dl(X_train, X_test, y_train, y_test):
    """Load the saved Keras model and evaluate on the same test set."""
    print("--- Evaluating Deep Learning (Keras) model ---")
    model_path = os.path.join(MODEL_DIR, "yield_model.keras")
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Keras model not found at {model_path}. "
            "Run train_yield_model.py first."
        )
    model = keras.models.load_model(model_path)
    dl_pred = model.predict(X_test, verbose=0).flatten()
    return {
        "mae": mean_absolute_error(y_test, dl_pred),
        "rmse": np.sqrt(mean_squared_error(y_test, dl_pred)),
        "r2": r2_score(y_test, dl_pred),
    }


def plot_comparison(all_results):
    """Generate a grouped bar chart comparing MAE, RMSE, and R2 across models."""
    models = list(all_results.keys())
    metrics = ["mae", "rmse", "r2"]
    metric_labels = ["MAE (lower is better)", "RMSE (lower is better)",
                     "R2 Score (higher is better)"]
    colors = ["#fbbf24", "#f59e0b", "#22c55e", "#16a34a"]

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for i, metric in enumerate(metrics):
        values = [all_results[m][metric] for m in models]
        bars = axes[i].bar(models, values, color=colors[:len(models)],
                           edgecolor="white")
        axes[i].set_title(metric_labels[i], fontsize=12, fontweight="bold")
        axes[i].set_ylabel(metric.upper())
        axes[i].tick_params(axis='x', rotation=25)
        # Annotate bars with values
        for bar, val in zip(bars, values):
            axes[i].text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                         f"{val:.3f}", ha="center", va="bottom", fontsize=10,
                         fontweight="bold")

    fig.suptitle("ML Baselines vs Deep Learning — Crop Yield Prediction",
                fontsize=14, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(OUTPUT_DIR, "baseline_vs_dl_comparison.png"), dpi=150)
    plt.close(fig)
    print(f"\nSaved: baseline_vs_dl_comparison.png")


def main():
    print("=" * 70)
    print("  ML Baseline vs Deep Learning Comparison")
    print("=" * 70)

    X_train, X_test, y_train, y_test = load_and_preprocess()

    baselines = train_baselines(X_train, X_test, y_train, y_test)
    dl_metrics = evaluate_dl(X_train, X_test, y_train, y_test)

    all_results = {**baselines, "Deep Learning (Keras)": dl_metrics}

    # Print results table
    print("\n" + "=" * 70)
    print(f"  {'Model':<25} {'MAE':>8} {'RMSE':>8} {'R2':>8}")
    print("-" * 70)
    for model_name, m in all_results.items():
        print(f"  {model_name:<25} {m['mae']:>8.4f} {m['rmse']:>8.4f} {m['r2']:>8.4f}")
    print("=" * 70)

    # Save results as JSON
    results_path = os.path.join(OUTPUT_DIR, "comparison_results.json")
    with open(results_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"Saved: comparison_results.json")

    # Generate comparison chart
    plot_comparison(all_results)

    print("\nComparison complete!")


if __name__ == "__main__":
    main()
