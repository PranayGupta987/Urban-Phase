import numpy as np
import pandas as pd
from typing import Tuple

def generate_synthetic_data(n_samples: int = 1000) -> pd.DataFrame:
    np.random.seed(42)

    hour = np.random.randint(0, 24, n_samples)
    day_of_week = np.random.randint(0, 7, n_samples)
    temperature = np.random.normal(20, 10, n_samples)
    humidity = np.random.uniform(30, 90, n_samples)
    is_rush_hour = ((hour >= 7) & (hour <= 9) | (hour >= 17) & (hour <= 19)).astype(int)
    is_weekend = (day_of_week >= 5).astype(int)

    traffic_base = 50 + 30 * is_rush_hour - 20 * is_weekend
    traffic_noise = np.random.normal(0, 10, n_samples)
    traffic_volume = np.clip(traffic_base + traffic_noise, 0, 100)

    aqi_base = 80 + 0.5 * traffic_volume - 0.3 * temperature + 0.2 * humidity
    aqi_noise = np.random.normal(0, 15, n_samples)
    aqi = np.clip(aqi_base + aqi_noise, 0, 500)

    df = pd.DataFrame({
        'hour': hour,
        'day_of_week': day_of_week,
        'temperature': temperature,
        'humidity': humidity,
        'is_rush_hour': is_rush_hour,
        'is_weekend': is_weekend,
        'traffic_volume': traffic_volume,
        'aqi': aqi
    })

    return df

def split_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    from sklearn.model_selection import train_test_split

    feature_cols = ['hour', 'day_of_week', 'temperature', 'humidity', 'is_rush_hour', 'is_weekend']
    X = df[feature_cols]
    y = df['aqi']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test
