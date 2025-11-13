"""
Model Loader for UrbanPulse ML Predictions
Loads and caches the trained LightGBM model for fast inference
"""
import os
import json
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Import feature engineering
from ml.features import compute_feature_matrix


# Paths
BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"
CONFIG_FILE = BASE_DIR / "model_config.json"

MODEL_FILE = MODELS_DIR / "model.pkl"

# Global model cache
_cached_model: Optional[Any] = None
_model_config: Optional[Dict[str, Any]] = None


def get_model():
    """
    Get the cached model, loading it if necessary
    
    Returns:
        Trained LightGBM model
    
    Raises:
        FileNotFoundError: If model file doesn't exist
    """
    global _cached_model
    
    if _cached_model is not None:
        return _cached_model
    
    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_FILE}. "
            "Please run 'python backend/ml/train_model.py' first to train the model."
        )
    
    print(f"Loading model from {MODEL_FILE}...")
    _cached_model = joblib.load(MODEL_FILE)
    print("  ✓ Model loaded and cached")
    
    return _cached_model


def get_config() -> Dict[str, Any]:
    """Load model configuration"""
    global _model_config
    
    if _model_config is not None:
        return _model_config
    
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")
    
    with open(CONFIG_FILE, 'r') as f:
        _model_config = json.load(f)
    
    return _model_config


def preprocess_input(input_dict: Dict[str, Any]) -> pd.DataFrame:
    """
    Preprocess input dictionary to DataFrame with required features
    
    Args:
        input_dict: Dictionary with input features
    
    Returns:
        Preprocessed DataFrame ready for prediction
    """
    # Create DataFrame from input
    df = pd.DataFrame([input_dict])
    
    # Extract timestamp features if timestamp is provided
    if 'timestamp' in df.columns:
        if isinstance(df['timestamp'].iloc[0], str):
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour_of_day'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['day_of_month'] = df['timestamp'].dt.day
    else:
        # Use current time if not provided
        now = datetime.now()
        df['hour_of_day'] = now.hour
        df['day_of_week'] = now.weekday()
        df['day_of_month'] = now.day
    
    # Compute feature matrix (adds derived features)
    df = compute_feature_matrix(df)
    
    return df


def predict_from_dict(input_dict: Dict[str, Any]) -> float:
    """
    Predict congestion_level from input dictionary
    
    Args:
        input_dict: Dictionary with features:
            - avg_speed (float)
            - vehicle_count (int)
            - pm25 (float)
            - temperature (float)
            - humidity (float)
            - wind_speed (float)
            - rainfall (float)
            - segment_id (int, optional)
            - timestamp (datetime, optional)
    
    Returns:
        Predicted congestion_level (float)
    
    Raises:
        FileNotFoundError: If model not found
        ValueError: If required features are missing
    """
    # Get model and config
    model = get_model()
    config = get_config()
    
    # Preprocess input
    df = preprocess_input(input_dict)
    
    # Get feature columns from config
    base_features = config.get('feature_columns', [])
    timestamp_features = ['hour_of_day', 'day_of_week', 'day_of_month']
    
    # Collect all available features
    all_features = []
    for feat in base_features + timestamp_features:
        if feat in df.columns:
            all_features.append(feat)
    
    # Add engineered features if available
    engineered_features = ['traffic_density', 'pm25_dispersion', 'heat_index', 'weather_speed_impact']
    for feat in engineered_features:
        if feat in df.columns and feat not in all_features:
            all_features.append(feat)
    
    # Check for missing required features
    required_base = ['avg_speed', 'vehicle_count', 'pm25', 'temperature', 'humidity', 'wind_speed', 'rainfall']
    missing = [f for f in required_base if f not in df.columns]
    if missing:
        raise ValueError(f"Missing required features: {missing}")
    
    # Extract features for prediction
    X = df[all_features]
    
    # Fill any remaining NaN with 0
    X = X.fillna(0)
    
    # Make prediction
    prediction = model.predict(X, num_iteration=model.best_iteration)[0]
    
    # Ensure prediction is in valid range [0, 1]
    prediction = max(0.0, min(1.0, float(prediction)))
    
    return prediction

