"""
Lightweight Hyperparameter Tuning for the Yield Prediction DL Model
====================================================================

Tests a small grid of meaningful hyperparameter combinations:
  - Learning rate: 0.001, 0.0005
  - Dropout rate: 0.10, 0.20
  - Hidden layer size: (128,64,32), (64,32,16)

Uses the same dataset and preprocessing (with proper train/test split)
as train_yield_model.py. Selects the best configuration by validation loss.

Outputs:
  - Console report of all configurations and their validation metrics
  - JSON file with all results and selected configuration
  - Saved to backend/training/analysis/tuning_figures/

Run: python backend/training/analysis/hyperparameter_tuning.py
"""

import os
import json
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf
from tensorflow import keras

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "tuning_figures")

YIELD_CSV = os.path.join(DATASET_DIR, "crop_yield_data.csv")

NUMERICAL_FEATURES = ["area", "rainfall", "temperature", "humidity", "fertilizer"]
CATEGORICAL_FEATURES = ["crop", "season"]
TARGET = "yield"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set global seeds for reproducibility
tf.random.set_seed(42)
np.random.seed(42)


def load_and_preprocess():
    """Load and preprocess with proper train/test split (no data leakage)."""
    df = pd.read_csv(YIELD_CSV)
    y = df[TARGET].values
    X_raw = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES].copy()

    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X_raw, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    train_num = scaler.fit_transform(X_train_raw[NUMERICAL_FEATURES])
    test_num = scaler.transform(X_test_raw[NUMERICAL_FEATURES])

    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    train_cat = encoder.fit_transform(X_train_raw[CATEGORICAL_FEATURES])
    test_cat = encoder.transform(X_test_raw[CATEGORICAL_FEATURES])

    X_train = np.hstack([train_num, train_cat])
    X_test = np.hstack([test_num, test_cat])

    return X_train, X_test, y_train, y_test, X_train.shape[1]


def build_model(input_dim, learning_rate, dropout_rate, hidden_sizes):
    """Build a model with configurable hyperparameters."""
    layers = [keras.layers.Input(shape=(input_dim,))]
    for i, size in enumerate(hidden_sizes):
        layers.append(keras.layers.Dense(size, activation="relu"))
        layers.append(keras.layers.BatchNormalization())
        layers.append(keras.layers.Dropout(dropout_rate))
    layers.append(keras.layers.Dense(1, activation="linear"))

    model = keras.Sequential(layers)
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss="mse",
        metrics=["mae"],
    )
    return model


# Hyperparameter grid
CONFIGS = [
    {"learning_rate": 0.001,  "dropout": 0.10, "hidden_sizes": (128, 64, 32)},
    {"learning_rate": 0.001,  "dropout": 0.20, "hidden_sizes": (128, 64, 32)},
    {"learning_rate": 0.0005, "dropout": 0.10, "hidden_sizes": (128, 64, 32)},
    {"learning_rate": 0.0005, "dropout": 0.20, "hidden_sizes": (128, 64, 32)},
    {"learning_rate": 0.001,  "dropout": 0.15, "hidden_sizes": (64, 32, 16)},
    {"learning_rate": 0.0005, "dropout": 0.15, "hidden_sizes": (64, 32, 16)},
]


def main():
    print("=" * 70)
    print("  Hyperparameter Tuning — Yield Prediction DL Model")
    print("=" * 70)

    X_train, X_test, y_train, y_test, input_dim = load_and_preprocess()
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    print(f"Feature count: {input_dim}")
    print(f"Configurations to test: {len(CONFIGS)}\n")

    results = []

    for i, cfg in enumerate(CONFIGS):
        label = f"Config {i+1}: lr={cfg['learning_rate']}, dropout={cfg['dropout']}, sizes={cfg['hidden_sizes']}"
        print(f"--- Testing {label} ---")

        tf.random.set_seed(42)
        np.random.seed(42)

        model = build_model(input_dim, cfg["learning_rate"], cfg["dropout"], cfg["hidden_sizes"])

        history = model.fit(
            X_train, y_train,
            validation_split=0.15,
            epochs=50,
            batch_size=32,
            verbose=0,
            callbacks=[
                keras.callbacks.EarlyStopping(
                    monitor="val_loss", patience=8, restore_best_weights=True
                ),
            ],
        )

        epochs_run = len(history.history["loss"])
        val_loss = min(history.history["val_loss"])
        val_mae = min(history.history["val_mae"])

        # Also evaluate on test set
        y_pred = model.predict(X_test, verbose=0).flatten()
        test_mae = mean_absolute_error(y_test, y_pred)
        test_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        test_r2 = r2_score(y_test, y_pred)

        result = {
            "config_id": i + 1,
            "learning_rate": cfg["learning_rate"],
            "dropout": cfg["dropout"],
            "hidden_sizes": list(cfg["hidden_sizes"]),
            "epochs_run": epochs_run,
            "val_loss": float(round(val_loss, 4)),
            "val_mae": float(round(val_mae, 4)),
            "test_mae": float(round(test_mae, 4)),
            "test_rmse": float(round(test_rmse, 4)),
            "test_r2": float(round(test_r2, 4)),
        }
        results.append(result)
        print(f"  Val Loss: {val_loss:.4f}, Val MAE: {val_mae:.4f}, "
              f"Test R2: {test_r2:.4f}, Epochs: {epochs_run}\n")

    # Select best by validation loss
    best = min(results, key=lambda r: r["val_loss"])
    print("=" * 70)
    print(f"  BEST CONFIG: #{best['config_id']}")
    print(f"  lr={best['learning_rate']}, dropout={best['dropout']}, "
          f"sizes={best['hidden_sizes']}")
    print(f"  Val Loss: {best['val_loss']}, Val MAE: {best['val_mae']}")
    print(f"  Test R2: {best['test_r2']}, Test MAE: {best['test_mae']}")
    print("=" * 70)

    output = {
        "all_results": results,
        "best_config": best,
        "selection_metric": "val_loss (lower is better)",
    }

    output_path = os.path.join(OUTPUT_DIR, "tuning_results.json")
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Saved: {output_path}")
    print("\nTuning complete!")


if __name__ == "__main__":
    main()
