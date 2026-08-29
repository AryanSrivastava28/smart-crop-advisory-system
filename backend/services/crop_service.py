"""
Crop Recommendation Service

Loads the trained ML model and provides prediction functionality.
Uses the saved Joblib model (RandomForest or LogisticRegression) to
recommend the best crop based on soil and environmental inputs.
"""

import os
import joblib
import numpy as np

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml_models")

_model = None
_scaler = None
_metadata = None


def _ensure_loaded():
    """Lazy-load the model, scaler, and metadata on first use."""
    global _model, _scaler, _metadata
    if _model is not None:
        return

    model_path = os.path.join(MODEL_DIR, "crop_model.joblib")
    scaler_path = os.path.join(MODEL_DIR, "crop_scaler.joblib")
    metadata_path = os.path.join(MODEL_DIR, "crop_metadata.joblib")

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            "Crop model not found. Run: python backend/training/train_crop_model.py"
        )

    _model = joblib.load(model_path)
    _scaler = joblib.load(scaler_path)
    _metadata = joblib.load(metadata_path)


def predict_crop(nitrogen, phosphorus, potassium, ph, temperature, humidity, rainfall):
    """
    Predict the best crop for the given inputs.

    Returns a dict with:
      - crop: recommended crop name
      - confidence: prediction confidence percentage
      - probabilities: dict of crop -> probability for all classes
    """
    _ensure_loaded()

    # Build feature array in the correct order
    features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])

    # Scale if the model needs it (LogisticRegression)
    if _metadata.get("needs_scaling", False):
        features = _scaler.transform(features)

    # Get prediction and probabilities
    prediction = _model.predict(features)[0]
    probabilities = _model.predict_proba(features)[0]
    classes = _model.classes_

    # Confidence is the probability of the predicted class
    confidence = int(round(max(probabilities) * 100))

    # Build a crop -> probability map
    prob_map = {cls: float(p) for cls, p in zip(classes, probabilities)}

    return {
        "crop": prediction,
        "confidence": confidence,
        "probabilities": prob_map,
    }
