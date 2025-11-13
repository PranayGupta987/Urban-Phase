import json
import os

class TrafficService:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "..", "data", "traffic.geojson")

    def get_traffic_geojson(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r') as f:
                return json.load(f)

        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            [-0.1278, 51.5074],
                            [-0.1268, 51.5084],
                            [-0.1258, 51.5094]
                        ]
                    },
                    "properties": {
                        "speed": 25,
                        "congestion": "moderate",
                        "volume": 1200
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            [-0.1258, 51.5094],
                            [-0.1248, 51.5104],
                            [-0.1238, 51.5114]
                        ]
                    },
                    "properties": {
                        "speed": 15,
                        "congestion": "high",
                        "volume": 2400
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            [-0.1298, 51.5064],
                            [-0.1288, 51.5074],
                            [-0.1278, 51.5074]
                        ]
                    },
                    "properties": {
                        "speed": 40,
                        "congestion": "low",
                        "volume": 800
                    }
                }
            ]
        }
