"""
Feature Engineering Module for UrbanPulse ML Pipeline
Computes derived features from raw dataset columns
"""
import pandas as pd
import numpy as np
from typing import Dict, Any
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def compute_feature_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute derived features from raw dataset
    
    Args:
        df: DataFrame with columns: avg_speed, vehicle_count, congestion_level,
            pm25, temperature, humidity, wind_speed, rainfall, segment_id
    
    Returns:
        DataFrame with additional feature columns
    """
    df = df.copy()
    
    # Feature 1: speed_drop = max_speed_per_segment - current_speed
    if 'segment_id' in df.columns and 'avg_speed' in df.columns:
        max_speed_per_segment = df.groupby('segment_id')['avg_speed'].transform('max')
        df['speed_drop'] = max_speed_per_segment - df['avg_speed']
    else:
        df['speed_drop'] = 0
    
    # Feature 2: congestion_ratio = vehicle_count / max(vehicle_count)
    if 'vehicle_count' in df.columns:
        max_vehicle_count = df['vehicle_count'].max()
        if max_vehicle_count > 0:
            df['congestion_ratio'] = df['vehicle_count'] / max_vehicle_count
        else:
            df['congestion_ratio'] = 0
    else:
        df['congestion_ratio'] = 0
    
    # Feature 3: humidity_temp_interaction = humidity * temperature
    if 'humidity' in df.columns and 'temperature' in df.columns:
        df['humidity_temp_interaction'] = df['humidity'] * df['temperature']
    else:
        df['humidity_temp_interaction'] = 0
    
    # Additional useful features
    if 'avg_speed' in df.columns and 'vehicle_count' in df.columns:
        # Traffic density: vehicles per unit speed
        df['traffic_density'] = df['vehicle_count'] / (df['avg_speed'] + 1)  # +1 to avoid division by zero
    
    if 'pm25' in df.columns and 'wind_speed' in df.columns:
        # Pollution dispersion: higher wind speed should reduce effective PM2.5
        df['pm25_dispersion'] = df['pm25'] / (df['wind_speed'] + 1)
    
    if 'temperature' in df.columns and 'humidity' in df.columns:
        # Heat index approximation
        df['heat_index'] = df['temperature'] * (1 + df['humidity'] / 100)
    
    if 'rainfall' in df.columns and 'avg_speed' in df.columns:
        # Weather impact on speed
        df['weather_speed_impact'] = df['avg_speed'] * (1 - df['rainfall'] / 10).clip(0.5, 1.0)
    
    return df


def scale_features(df: pd.DataFrame, 
                   feature_columns: list = None,
                   scaler_type: str = 'standard'):
    """
    Scale features using StandardScaler or MinMaxScaler
    
    Args:
        df: DataFrame with features to scale
        feature_columns: List of column names to scale. If None, scales all numeric columns
        scaler_type: 'standard' (StandardScaler) or 'minmax' (MinMaxScaler)
    
    Returns:
        Tuple of (scaled_df, scaler_object)
    """
    df = df.copy()
    
    if feature_columns is None:
        # Select numeric columns only
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        # Exclude timestamp and ID columns if they exist
        exclude_cols = ['timestamp', 'segment_id', 'location_id']
        feature_columns = [col for col in numeric_cols if col not in exclude_cols]
    
    # Filter to only columns that exist in dataframe
    feature_columns = [col for col in feature_columns if col in df.columns]
    
    if not feature_columns:
        return df, None
    
    # Initialize scaler
    if scaler_type == 'standard':
        scaler = StandardScaler()
    elif scaler_type == 'minmax':
        scaler = MinMaxScaler()
    else:
        raise ValueError(f"Unknown scaler_type: {scaler_type}. Use 'standard' or 'minmax'")
    
    # Scale features
    df[feature_columns] = scaler.fit_transform(df[feature_columns])
    
    return df, scaler

