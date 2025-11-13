import json
import os

class AQIService:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "..", "data", "aqi.geojson")

    def get_aqi_geojson(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r') as f:
                return json.load(f)

        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-0.1278, 51.5074]
                    },
                    "properties": {
                        "aqi": 65,
                        "category": "Moderate",
                        "pm25": 22.5,
                        "pm10": 35.2,
                        "station": "Central Station"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-0.1398, 51.5134]
                    },
                    "properties": {
                        "aqi": 85,
                        "category": "Unhealthy for Sensitive Groups",
                        "pm25": 35.8,
                        "pm10": 52.1,
                        "station": "Industrial Zone"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-0.1158, 51.5014]
                    },
                    "properties": {
                        "aqi": 45,
                        "category": "Good",
                        "pm25": 12.3,
                        "pm10": 18.7,
                        "station": "Park Sensor"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-0.1208, 51.5094]
                    },
                    "properties": {
                        "aqi": 72,
                        "category": "Moderate",
                        "pm25": 28.1,
                        "pm10": 41.5,
                        "station": "City Center"
                    }
                }
            ]
        }
