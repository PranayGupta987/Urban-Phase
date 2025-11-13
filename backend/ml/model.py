import pickle
import numpy as np
from pathlib import Path
from typing import Dict, Any

class AQIPredictor:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        model_path = Path(__file__).parent / "models" / "aqi_model.pkl"
        if model_path.exists():
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            print("AQI model loaded successfully")
        else:
            print("Warning: AQI model not found. Run train.py first.")

    def predict(self, features: Dict[str, Any]) -> float:
        if self.model is None:
            return self._fallback_prediction(features)

        feature_array = np.array([[
            features.get('hour', 12),
            features.get('day_of_week', 3),
            features.get('temperature', 20),
            features.get('humidity', 60),
            features.get('is_rush_hour', 0),
            features.get('is_weekend', 0)
        ]])

        prediction = self.model.predict(feature_array)[0]
        return float(np.clip(prediction, 0, 500))

    def _fallback_prediction(self, features: Dict[str, Any]) -> float:
        base_aqi = 100
        if features.get('is_rush_hour', 0):
            base_aqi += 30
        if features.get('is_weekend', 0):
            base_aqi -= 20

        temp_factor = (features.get('temperature', 20) - 20) * -0.5
        humidity_factor = (features.get('humidity', 60) - 60) * 0.2

        return float(np.clip(base_aqi + temp_factor + humidity_factor, 0, 500))

predictor = AQIPredictor()
