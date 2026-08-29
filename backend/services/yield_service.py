"""
Yield Prediction Service

Loads the trained Keras neural network and preprocessing objects
to predict crop yield based on environmental and agricultural inputs.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd

# Suppress TF verbose logging
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf
from tensorflow import keras

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml_models")

_model = None
_scaler = None
_encoder = None
_metadata = None


def _ensure_loaded():
    """Lazy-load the Keras model and preprocessing objects on first use."""
    global _model, _scaler, _encoder, _metadata
    if _model is not None:
        return

    model_path = os.path.join(MODEL_DIR, "yield_model.keras")
    scaler_path = os.path.join(MODEL_DIR, "yield_scaler.joblib")
    encoder_path = os.path.join(MODEL_DIR, "yield_encoder.joblib")
    metadata_path = os.path.join(MODEL_DIR, "yield_metadata.json")

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            "Yield model not found. Run: python backend/training/train_yield_model.py"
        )

    _model = keras.models.load_model(model_path)
    _scaler = joblib.load(scaler_path)
    _encoder = joblib.load(encoder_path)
    with open(metadata_path, "r") as f:
        _metadata = json.load(f)


def predict_yield(crop, area, rainfall, temperature, humidity, fertilizer, season):
    """
    Predict crop yield using the trained neural network.

    Returns a dict with:
      - predicted_yield: float (tonnes/hectare)
      - unit: str
    """
    _ensure_loaded()

    numerical_features = _metadata["numerical_features"]
    categorical_features = _metadata["categorical_features"]

    # Build numerical feature array
    num_values = np.array([[area, rainfall, temperature, humidity, fertilizer]])
    num_scaled = _scaler.transform(num_values)

    # One-hot encode categorical features
    cat_df = pd.DataFrame([[crop, season]], columns=categorical_features)
    cat_encoded = _encoder.transform(cat_df).toarray() if hasattr(_encoder.transform(cat_df), 'toarray') else _encoder.transform(cat_df)

    # Combine features
    features = np.hstack([num_scaled, cat_encoded])

    # Predict
    prediction = float(_model.predict(features, verbose=0).flatten()[0])
    prediction = max(0.0, prediction)

    return {
        "predicted_yield": round(prediction, 2),
        "unit": "tonnes/hectare",
    }
