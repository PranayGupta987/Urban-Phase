"""
Dataset Preparation Pipeline for UrbanPulse ML Models
Generates synthetic datasets and merges them for training
"""
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from features import compute_feature_matrix

# Paths
BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / "dataset"

# Ensure dataset directory exists
DATASET_DIR.mkdir(exist_ok=True)

TRAFFIC_CSV = DATASET_DIR / "traffic_data.csv"
AQI_CSV = DATASET_DIR / "aqi_data.csv"
WEATHER_CSV = DATASET_DIR / "weather_data.csv"
MERGED_CSV = DATASET_DIR / "merged_training_data.csv"
CONFIG_JSON = BASE_DIR / "model_config.json"


def generate_traffic_data(hours: int = 48) -> pd.DataFrame:
    """
    Generate synthetic traffic data with realistic patterns
    
    Args:
        hours: Number of hours of data to generate
    
    Returns:
        DataFrame with traffic data
    """
    print(f"Generating traffic data for {hours} hours...")
    
    # Generate timestamps (every 5 minutes)
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    timestamps = []
    current = start_time
    end_time = start_time + timedelta(hours=hours)
    
    while current < end_time:
        timestamps.append(current)
        current += timedelta(minutes=5)
    
    n_timestamps = len(timestamps)
    n_segments = 200
    
    # Generate data for each segment
    data = []
    
    for segment_id in range(1, n_segments + 1):
        # Base speed varies by segment (highway vs city street)
        base_speed = np.random.uniform(30, 70) if segment_id % 3 == 0 else np.random.uniform(15, 45)
        
        for timestamp in timestamps:
            # Time-based patterns
            hour = timestamp.hour
            
            # Rush hour patterns (7-9 AM, 5-7 PM)
            if hour in [7, 8, 9, 17, 18, 19]:
                speed_multiplier = np.random.uniform(0.4, 0.7)
                vehicle_multiplier = np.random.uniform(1.5, 2.5)
            # Night time (11 PM - 5 AM)
            elif hour in [23, 0, 1, 2, 3, 4]:
                speed_multiplier = np.random.uniform(1.1, 1.3)
                vehicle_multiplier = np.random.uniform(0.3, 0.6)
            # Normal hours
            else:
                speed_multiplier = np.random.uniform(0.8, 1.1)
                vehicle_multiplier = np.random.uniform(0.8, 1.2)
            
            # Add some randomness
            speed_noise = np.random.normal(0, 5)
            avg_speed = max(10, min(80, base_speed * speed_multiplier + speed_noise))
            
            # Vehicle count correlates with speed (inverse relationship)
            vehicle_count = max(50, min(300, int(base_speed * (1 - speed_multiplier) * 10 * vehicle_multiplier + np.random.normal(0, 20))))
            
            # Congestion level (0-1): inverse of normalized speed
            normalized_speed = (avg_speed - 10) / 70  # Normalize to 0-1
            congestion_level = max(0, min(1, 1 - normalized_speed + np.random.normal(0, 0.1)))
            
            data.append({
                'timestamp': timestamp,
                'segment_id': segment_id,
                'avg_speed': round(avg_speed, 2),
                'congestion_level': round(congestion_level, 3),
                'vehicle_count': vehicle_count
            })
    
    df = pd.DataFrame(data)
    print(f"Generated {len(df)} traffic records ({n_segments} segments × {n_timestamps} timestamps)")
    return df


def generate_aqi_data(hours: int = 48) -> pd.DataFrame:
    """
    Generate synthetic AQI data with realistic patterns
    
    Args:
        hours: Number of hours of data to generate
    
    Returns:
        DataFrame with AQI data
    """
    print(f"Generating AQI data for {hours} hours...")
    
    # Generate timestamps (every 5 minutes)
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    timestamps = []
    current = start_time
    end_time = start_time + timedelta(hours=hours)
    
    while current < end_time:
        timestamps.append(current)
        current += timedelta(minutes=5)
    
    n_timestamps = len(timestamps)
    n_locations = 50
    
    # Generate data for each location
    data = []
    
    for location_id in range(1, n_locations + 1):
        # Base PM2.5 varies by location (industrial vs residential)
        base_pm25 = np.random.uniform(80, 150) if location_id % 5 == 0 else np.random.uniform(20, 80)
        
        for timestamp in timestamps:
            # Time-based patterns (higher during day, lower at night)
            hour = timestamp.hour
            
            # Daytime (8 AM - 8 PM) - higher pollution
            if 8 <= hour < 20:
                pm25_multiplier = np.random.uniform(1.1, 1.4)
            # Night time - lower pollution
            else:
                pm25_multiplier = np.random.uniform(0.7, 0.9)
            
            # Add randomness
            pm25_noise = np.random.normal(0, 10)
            pm25 = max(10, min(200, base_pm25 * pm25_multiplier + pm25_noise))
            
            # AQI calculation (simplified, based on PM2.5)
            if pm25 <= 12:
                aqi = int((pm25 / 12) * 50)
            elif pm25 <= 35.4:
                aqi = int(50 + ((pm25 - 12) / (35.4 - 12)) * 50)
            elif pm25 <= 55.4:
                aqi = int(100 + ((pm25 - 35.4) / (55.4 - 35.4)) * 50)
            elif pm25 <= 150.4:
                aqi = int(150 + ((pm25 - 55.4) / (150.4 - 55.4)) * 50)
            else:
                aqi = int(200 + ((pm25 - 150.4) / (250.4 - 150.4)) * 100)
            
            aqi = max(50, min(200, aqi))
            
            data.append({
                'timestamp': timestamp,
                'location_id': location_id,
                'pm25': round(pm25, 2),
                'aqi': aqi
            })
    
    df = pd.DataFrame(data)
    print(f"Generated {len(df)} AQI records ({n_locations} locations × {n_timestamps} timestamps)")
    return df


def generate_weather_data(hours: int = 48) -> pd.DataFrame:
    """
    Generate synthetic weather data with realistic patterns
    
    Args:
        hours: Number of hours of data to generate
    
    Returns:
        DataFrame with weather data
    """
    print(f"Generating weather data for {hours} hours...")
    
    # Generate timestamps (every 5 minutes)
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    timestamps = []
    current = start_time
    end_time = start_time + timedelta(hours=hours)
    
    while current < end_time:
        timestamps.append(current)
        current += timedelta(minutes=5)
    
    data = []
    
    # Base weather parameters (tropical city like Singapore/Bangalore)
    base_temp = 28.0  # Celsius
    base_humidity = 70.0  # Percentage
    
    for timestamp in timestamps:
        hour = timestamp.hour
        
        # Temperature: cooler at night, warmer during day
        if 2 <= hour < 6:
            temp = base_temp - np.random.uniform(3, 6)
        elif 12 <= hour < 16:
            temp = base_temp + np.random.uniform(2, 5)
        else:
            temp = base_temp + np.random.uniform(-1, 2)
        
        temp = max(20, min(38, temp))
        
        # Humidity: higher at night, lower during day
        if 2 <= hour < 6:
            humidity = base_humidity + np.random.uniform(5, 15)
        elif 12 <= hour < 16:
            humidity = base_humidity - np.random.uniform(10, 20)
        else:
            humidity = base_humidity + np.random.uniform(-5, 5)
        
        humidity = max(40, min(95, humidity))
        
        # Wind speed: varies throughout day
        wind_speed = np.random.uniform(5, 25) + np.random.normal(0, 3)
        wind_speed = max(0, min(40, wind_speed))
        
        # Rainfall: occasional, higher probability during afternoon
        if 14 <= hour < 18:
            rain_prob = 0.3
        else:
            rain_prob = 0.1
        
        if np.random.random() < rain_prob:
            rainfall = np.random.exponential(2.0)
            rainfall = min(20, rainfall)  # Cap at 20mm
        else:
            rainfall = 0.0
        
        data.append({
            'timestamp': timestamp,
            'temperature': round(temp, 2),
            'humidity': round(humidity, 2),
            'wind_speed': round(wind_speed, 2),
            'rainfall': round(rainfall, 2)
        })
    
    df = pd.DataFrame(data)
    print(f"Generated {len(df)} weather records")
    return df


def merge_datasets(traffic_df: pd.DataFrame, 
                   aqi_df: pd.DataFrame, 
                   weather_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge traffic, AQI, and weather datasets by nearest timestamp
    
    Args:
        traffic_df: Traffic data DataFrame
        aqi_df: AQI data DataFrame
        weather_df: Weather data DataFrame
    
    Returns:
        Merged DataFrame
    """
    print("Merging datasets...")
    
    # Set timestamp as index for easier merging
    traffic_df = traffic_df.set_index('timestamp').sort_index()
    aqi_df = aqi_df.set_index('timestamp').sort_index()
    weather_df = weather_df.set_index('timestamp').sort_index()
    
    # Merge weather first (most frequent, every 5 min)
    merged = traffic_df.join(weather_df, how='left')
    
    # For AQI, we need to merge by nearest timestamp
    # Since AQI has location_id, we'll average or take first location
    # For simplicity, let's take the first location's data
    aqi_single = aqi_df[aqi_df['location_id'] == 1].drop('location_id', axis=1)
    
    # Merge AQI using nearest timestamp
    merged = merged.join(aqi_single, how='left', rsuffix='_aqi')
    
    # Forward fill missing values (within reasonable time window)
    merged = merged.ffill(limit=2)
    merged = merged.bfill(limit=2)
    
    # Drop rows with any remaining NaN values
    merged = merged.dropna()
    
    # Reset index to get timestamp as column
    merged = merged.reset_index()
    
    print(f"Merged dataset: {len(merged)} rows")
    return merged


def save_datasets(traffic_df: pd.DataFrame, 
                  aqi_df: pd.DataFrame, 
                  weather_df: pd.DataFrame,
                  merged_df: pd.DataFrame):
    """Save all datasets to CSV files"""
    print("\nSaving datasets...")
    
    traffic_df.to_csv(TRAFFIC_CSV, index=False)
    print(f"  ✓ Saved {TRAFFIC_CSV} ({len(traffic_df)} rows)")
    
    aqi_df.to_csv(AQI_CSV, index=False)
    print(f"  ✓ Saved {AQI_CSV} ({len(aqi_df)} rows)")
    
    weather_df.to_csv(WEATHER_CSV, index=False)
    print(f"  ✓ Saved {WEATHER_CSV} ({len(weather_df)} rows)")
    
    merged_df.to_csv(MERGED_CSV, index=False)
    print(f"  ✓ Saved {MERGED_CSV} ({len(merged_df)} rows)")


def print_summary_stats(df: pd.DataFrame):
    """Print summary statistics of the merged dataset"""
    print("\n" + "="*60)
    print("DATASET SUMMARY STATISTICS")
    print("="*60)
    
    print(f"\nTotal Records: {len(df):,}")
    print(f"Time Range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"Unique Segments: {df['segment_id'].nunique()}")
    
    print("\n--- Traffic Features ---")
    print(df[['avg_speed', 'congestion_level', 'vehicle_count']].describe())
    
    print("\n--- AQI Features ---")
    print(df[['pm25', 'aqi']].describe())
    
    print("\n--- Weather Features ---")
    print(df[['temperature', 'humidity', 'wind_speed', 'rainfall']].describe())
    
    print("\n--- Missing Values ---")
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.sum() > 0 else "No missing values!")
    
    print("="*60)


def create_model_config():
    """Create model_config.json if it doesn't exist"""
    if CONFIG_JSON.exists():
        print(f"\n{CONFIG_JSON} already exists, skipping...")
        return
    
    config = {
        "train_fraction": 0.8,
        "target_variable": "congestion_level",
        "feature_columns": [
            "avg_speed",
            "vehicle_count",
            "pm25",
            "temperature",
            "humidity",
            "wind_speed",
            "rainfall",
            "speed_drop",
            "humidity_temp_interaction"
        ]
    }
    
    with open(CONFIG_JSON, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"  ✓ Created {CONFIG_JSON}")


def main():
    """Main pipeline execution"""
    print("="*60)
    print("URBANPULSE ML DATASET PREPARATION PIPELINE")
    print("="*60)
    
    # Generate or load datasets
    if TRAFFIC_CSV.exists():
        print(f"\nLoading existing {TRAFFIC_CSV}...")
        traffic_df = pd.read_csv(TRAFFIC_CSV, parse_dates=['timestamp'])
    else:
        traffic_df = generate_traffic_data(hours=48)
    
    if AQI_CSV.exists():
        print(f"\nLoading existing {AQI_CSV}...")
        aqi_df = pd.read_csv(AQI_CSV, parse_dates=['timestamp'])
    else:
        aqi_df = generate_aqi_data(hours=48)
    
    if WEATHER_CSV.exists():
        print(f"\nLoading existing {WEATHER_CSV}...")
        weather_df = pd.read_csv(WEATHER_CSV, parse_dates=['timestamp'])
    else:
        weather_df = generate_weather_data(hours=48)
    
    # Merge datasets
    merged_df = merge_datasets(traffic_df, aqi_df, weather_df)
    
    # Compute features
    print("\nComputing features...")
    merged_df = compute_feature_matrix(merged_df)
    print(f"  ✓ Added feature columns: speed_drop, congestion_ratio, humidity_temp_interaction, etc.")
    
    # Save all datasets
    save_datasets(traffic_df, aqi_df, weather_df, merged_df)
    
    # Create model config
    create_model_config()
    
    # Print summary
    print_summary_stats(merged_df)
    
    print("\n" + "="*60)
    print("PIPELINE COMPLETE! ✓")
    print("="*60)
    print(f"\nReady for model training with {len(merged_df):,} training samples.")


if __name__ == "__main__":
    main()

