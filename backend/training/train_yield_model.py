"""
Crop Yield Prediction Model Training (Deep Learning)
=====================================================

Trains a neural network using TensorFlow/Keras to predict crop yield
based on crop, area, rainfall, temperature, humidity, fertilizer, and season.

The model is a feedforward neural network with:
  - Input: 7 features (1 categorical encoded, 6 numerical normalized)
  - Hidden layers: 128 -> 64 -> 32 with ReLU activation
  - Output: 1 (regression - predicted yield)

Preprocessing:
  - Categorical features (crop, season) are one-hot encoded
  - Numerical features are normalized using StandardScaler
  - All preprocessing objects are saved for reuse at inference time

Evaluation metrics: MAE, RMSE, R2 Score

Run: python backend/training/train_yield_model.py
"""

import os
import sys
import json

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Suppress TensorFlow verbose logging
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf
from tensorflow import keras

# Paths
DATASET_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "datasets", "crop_yield_data.csv"
)
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml_models")

NUMERICAL_FEATURES = ["area", "rainfall", "temperature", "humidity", "fertilizer"]
CATEGORICAL_FEATURES = ["crop", "season"]
TARGET = "yield"


def load_data():
    """Load and validate the yield prediction dataset."""
    if not os.path.exists(DATASET_PATH):
        print(f"ERROR: Dataset not found at {DATASET_PATH}")
        print("Please run: python backend/training/generate_yield_dataset.py")
        sys.exit(1)

    df = pd.read_csv(DATASET_PATH)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Columns: {list(df.columns)}")
    return df


def preprocess(df):
    """Encode categorical features and normalize numerical features.

    Splits into train/test FIRST, then fits scaler and encoder only on
    training data to prevent data leakage.
    """
    y = df[TARGET].values

    # Split raw data before fitting any preprocessors
    X_raw = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES].copy()
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X_raw, y, test_size=0.2, random_state=42
    )

    # Fit scaler on training numerical features only
    scaler = StandardScaler()
    train_num_scaled = scaler.fit_transform(X_train_raw[NUMERICAL_FEATURES])
    test_num_scaled = scaler.transform(X_test_raw[NUMERICAL_FEATURES])

    # Fit encoder on training categorical features only
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    train_cat_encoded = encoder.fit_transform(X_train_raw[CATEGORICAL_FEATURES])
    test_cat_encoded = encoder.transform(X_test_raw[CATEGORICAL_FEATURES])
    cat_columns = encoder.get_feature_names_out(CATEGORICAL_FEATURES).tolist()

    # Combine numerical + categorical
    X_train = np.hstack([train_num_scaled, train_cat_encoded])
    X_test = np.hstack([test_num_scaled, test_cat_encoded])

    # Full feature list for metadata
    all_features = NUMERICAL_FEATURES + cat_columns
    feature_count = len(all_features)

    return X_train, X_test, y_train, y_test, scaler, encoder, cat_columns, all_features, feature_count


def build_model(input_dim):
    """Build a feedforward neural network for regression."""
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


def main():
    print("=" * 60)
    print("  Crop Yield Prediction - Deep Learning Training")
    print("=" * 60)

    # Set memory growth to avoid TF warnings
    gpus = tf.config.list_physical_devices("GPU")
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

    df = load_data()
    X_train, X_test, y_train, y_test, scaler, encoder, cat_columns, all_features, feature_count = preprocess(df)
    print(f"Features: {all_features}")
    print(f"Feature count: {feature_count}")

    # Build and train the model
    model = build_model(feature_count)
    model.summary()

    print("\n--- Training neural network ---")
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

    # Evaluate
    print("\n--- Evaluation ---")
    y_pred = model.predict(X_test, verbose=0).flatten()

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"MAE:  {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R2:   {r2:.4f}")

    # Save the Keras model
    os.makedirs(MODEL_DIR, exist_ok=True)
    keras_model_path = os.path.join(MODEL_DIR, "yield_model.keras")
    model.save(keras_model_path)
    print(f"\nKeras model saved to {keras_model_path}")

    # Save preprocessing objects
    joblib.dump(scaler, os.path.join(MODEL_DIR, "yield_scaler.joblib"))
    joblib.dump(encoder, os.path.join(MODEL_DIR, "yield_encoder.joblib"))

    # Save metadata
    metadata = {
        "numerical_features": NUMERICAL_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "categorical_columns": cat_columns,
        "all_features": all_features,
        "metrics": {"mae": float(mae), "rmse": float(rmse), "r2": float(r2)},
        "feature_count": feature_count,
    }
    with open(os.path.join(MODEL_DIR, "yield_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Preprocessing objects saved to {MODEL_DIR}")
    print(f"Metadata: {metadata}")
    print("\nTraining complete!")


if __name__ == "__main__":
    main()
