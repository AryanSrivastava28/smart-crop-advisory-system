"""
Crop Recommendation Model Training
===================================

Trains two classification algorithms on the Crop Recommendation Dataset
and saves the best one using Joblib.

DATASET REQUIRED:
  - Name: Crop Recommendation Dataset
  - Source: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset
  - File: Crop_recommendation.csv
  - Place at: backend/datasets/Crop_recommendation.csv

The dataset contains 2,200 rows with columns:
  N, P, K, temperature, humidity, ph, rainfall, label

The 'label' column is the crop name (rice, wheat, maize, etc.).
"""

import os
import sys

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Paths
DATASET_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "datasets", "Crop_recommendation.csv"
)
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml_models")


def load_data():
    """Load and validate the crop recommendation dataset."""
    if not os.path.exists(DATASET_PATH):
        print(f"ERROR: Dataset not found at {DATASET_PATH}")
        print("Please download Crop_recommendation.csv from:")
        print("  https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset")
        sys.exit(1)

    df = pd.read_csv(DATASET_PATH)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Columns: {list(df.columns)}")
    print(f"Crops: {df['label'].unique().tolist()}")
    return df


def preprocess(df):
    """Split features and labels, then train/test split."""
    X = df[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]].values
    y = df["label"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale features for Logistic Regression; RandomForest is scale-invariant
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, scaler


def train_and_compare(X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test):
    """Train two models and compare their performance."""
    results = {}

    # Model 1: Random Forest Classifier
    print("\n--- Training Random Forest Classifier ---")
    rf = RandomForestClassifier(
        n_estimators=100, max_depth=15, random_state=42, n_jobs=-1
    )
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_acc = accuracy_score(y_test, rf_pred)
    results["RandomForest"] = {"model": rf, "accuracy": rf_acc}
    print(f"Random Forest Accuracy: {rf_acc:.4f}")
    print(classification_report(y_test, rf_pred, zero_division=0))

    # Model 2: Logistic Regression (with scaled features)
    print("\n--- Training Logistic Regression ---")
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train_scaled, y_train)
    lr_pred = lr.predict(X_test_scaled)
    lr_acc = accuracy_score(y_test, lr_pred)
    results["LogisticRegression"] = {"model": lr, "accuracy": lr_acc}
    print(f"Logistic Regression Accuracy: {lr_acc:.4f}")
    print(classification_report(y_test, lr_pred, zero_division=0))

    # Select best model
    best_name = max(results, key=lambda k: results[k]["accuracy"])
    print(f"\n=== Best Model: {best_name} (Accuracy: {results[best_name]['accuracy']:.4f}) ===")
    return results, best_name


def save_model(results, best_name, scaler):
    """Save the best model, scaler, and metadata using Joblib."""
    os.makedirs(MODEL_DIR, exist_ok=True)

    best_model = results[best_name]["model"]
    joblib.dump(best_model, os.path.join(MODEL_DIR, "crop_model.joblib"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "crop_scaler.joblib"))

    # Save metadata: model name, accuracy, feature names, class labels
    metadata = {
        "model_name": best_name,
        "accuracy": results[best_name]["accuracy"],
        "features": ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"],
        "classes": best_model.classes_.tolist(),
        "needs_scaling": best_name == "LogisticRegression",
    }
    joblib.dump(metadata, os.path.join(MODEL_DIR, "crop_metadata.joblib"))
    print(f"Model saved to {MODEL_DIR}/crop_model.joblib")
    print(f"Metadata: {metadata}")


def main():
    print("=" * 60)
    print("  Crop Recommendation Model Training")
    print("=" * 60)

    df = load_data()
    X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, scaler = preprocess(df)
    results, best_name = train_and_compare(
        X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test
    )
    save_model(results, best_name, scaler)

    print("\nTraining complete!")


if __name__ == "__main__":
    main()
