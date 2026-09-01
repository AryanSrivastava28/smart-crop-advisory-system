"""
Training Curves & Overfitting Analysis for the Deep Learning Yield Model
========================================================================

Retrains the Keras neural network (same architecture as train_yield_model.py)
with verbose history logging, then:

  1. Plots training vs validation loss curves (MSE)
  2. Plots training vs validation MAE curves
  3. Performs overfitting analysis by comparing final train vs validation
     metrics and computing the generalization gap
  4. Saves all figures to backend/training/analysis/training_figures/

Run: python backend/training/analysis/training_curves.py
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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
MODEL_DIR = os.path.join(BASE_DIR, "ml_models")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "training_figures")

YIELD_CSV = os.path.join(DATASET_DIR, "crop_yield_data.csv")

NUMERICAL_FEATURES = ["area", "rainfall", "temperature", "humidity", "fertilizer"]
CATEGORICAL_FEATURES = ["crop", "season"]
TARGET = "yield"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_and_preprocess():
    """Load and preprocess the yield dataset (same as train_yield_model.py)."""
    df = pd.read_csv(YIELD_CSV)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    cat_encoded = encoder.fit_transform(df[CATEGORICAL_FEATURES])
    cat_columns = encoder.get_feature_names_out(CATEGORICAL_FEATURES).tolist()
    cat_df = pd.DataFrame(cat_encoded, columns=cat_columns, index=df.index)

    scaler = StandardScaler()
    num_scaled = scaler.fit_transform(df[NUMERICAL_FEATURES])
    num_df = pd.DataFrame(num_scaled, columns=NUMERICAL_FEATURES, index=df.index)

    X = pd.concat([num_df, cat_df], axis=1)
    y = df[TARGET].values

    X_train, X_test, y_train, y_test = train_test_split(
        X.values, y, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test, X.shape[1]


def build_model(input_dim):
    """Same architecture as train_yield_model.py for consistency."""
    model = keras.Sequential([
        keras.layers.Input(shape=(input_dim,)),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.15),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.1),
        keras.layers.Dense(32, activation="relu"),
        keras.layers.Dense(1, activation="linear"),
    ])
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="mse",
        metrics=["mae"],
    )
    return model


def plot_loss_curves(history):
    """Plot training vs validation loss (MSE)."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(history.history["loss"], label="Training Loss (MSE)",
            color="#16a34a", linewidth=2)
    ax.plot(history.history["val_loss"], label="Validation Loss (MSE)",
            color="#f59e0b", linewidth=2, linestyle="--")
    ax.set_title("Training vs Validation Loss (MSE)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss (MSE)")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "training_validation_loss.png"), dpi=150)
    plt.close(fig)
    print(f"Saved: training_validation_loss.png")


def plot_mae_curves(history):
    """Plot training vs validation MAE."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(history.history["mae"], label="Training MAE",
            color="#16a34a", linewidth=2)
    ax.plot(history.history["val_mae"], label="Validation MAE",
            color="#f59e0b", linewidth=2, linestyle="--")
    ax.set_title("Training vs Validation MAE", fontsize=14, fontweight="bold")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("MAE (tonnes/hectare)")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "training_validation_mae.png"), dpi=150)
    plt.close(fig)
    print(f"Saved: training_validation_mae.png")


def overfitting_analysis(history, model, X_train, y_train, X_test, y_test):
    """
    Compare final train vs test metrics and compute the generalization gap.

    A large gap between training and validation performance indicates
    overfitting. We report:
      - Final train loss vs final val loss
      - Final train MAE vs final val MAE
      - Test set metrics (MAE, RMSE, R2)
      - Generalization gap = |val_loss - train_loss|
    """
    final_train_loss = history.history["loss"][-1]
    final_val_loss = history.history["val_loss"][-1]
    final_train_mae = history.history["mae"][-1]
    final_val_mae = history.history["val_mae"][-1]
    gen_gap = abs(final_val_loss - final_train_loss)

    # Test set evaluation
    y_pred = model.predict(X_test, verbose=0).flatten()
    test_mae = mean_absolute_error(y_test, y_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    test_r2 = r2_score(y_test, y_pred)

    print("\n" + "=" * 60)
    print("  Overfitting Analysis")
    print("=" * 60)
    print(f"  Final Training Loss (MSE):   {final_train_loss:.4f}")
    print(f"  Final Validation Loss (MSE): {final_val_loss:.4f}")
    print(f"  Final Training MAE:          {final_train_mae:.4f}")
    print(f"  Final Validation MAE:        {final_val_mae:.4f}")
    print(f"  Generalization Gap (|val-tr|): {gen_gap:.4f}")
    print("-" * 60)
    print(f"  Test MAE:  {test_mae:.4f}")
    print(f"  Test RMSE: {test_rmse:.4f}")
    print(f"  Test R2:   {test_r2:.4f}")
    print("=" * 60)

    # Interpretation
    if gen_gap < 0.5:
        assessment = ("The generalization gap is small, indicating the model "
                       "generalizes well. Overfitting is well-controlled by the "
                       "Dropout layers and Early Stopping.")
    elif gen_gap < 2.0:
        assessment = ("Moderate generalization gap. The model shows slight "
                       "overfitting but performs adequately on unseen data.")
    else:
        assessment = ("Large generalization gap detected. The model may be "
                       "overfitting. Consider stronger regularization or more data.")
    print(f"\n  Assessment: {assessment}")

    # Save analysis as JSON
    analysis = {
        "final_train_loss": float(final_train_loss),
        "final_val_loss": float(final_val_loss),
        "final_train_mae": float(final_train_mae),
        "final_val_mae": float(final_val_mae),
        "generalization_gap": float(gen_gap),
        "test_mae": float(test_mae),
        "test_rmse": float(test_rmse),
        "test_r2": float(test_r2),
        "assessment": assessment,
    }
    analysis_path = os.path.join(OUTPUT_DIR, "overfitting_analysis.json")
    with open(analysis_path, "w") as f:
        json.dump(analysis, f, indent=2)
    print(f"Saved: overfitting_analysis.json")

    return analysis


def main():
    print("=" * 70)
    print("  Training Curves & Overfitting Analysis")
    print("=" * 70)

    X_train, X_test, y_train, y_test, input_dim = load_and_preprocess()

    model = build_model(input_dim)
    model.summary()

    print("\n--- Training neural network (max 80 epochs) ---")
    history = model.fit(
        X_train, y_train,
        validation_split=0.15,
        epochs=80,
        batch_size=32,
        verbose=1,
        callbacks=[
            keras.callbacks.EarlyStopping(
                monitor="val_loss", patience=10, restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor="val_loss", factor=0.5, patience=5, min_lr=1e-6
            ),
        ],
    )

    print(f"\nTraining stopped after {len(history.history['loss'])} epochs")

    # Generate plots
    plot_loss_curves(history)
    plot_mae_curves(history)

    # Overfitting analysis
    overfitting_analysis(history, model, X_train, y_train, X_test, y_test)

    print("\nTraining curves analysis complete!")


if __name__ == "__main__":
    main()
