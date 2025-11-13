from models.schemas import SimulationRequest, SimulationResponse, Metrics
from ml.placeholder_model import PlaceholderModel

class SimulationService:
    def __init__(self):
        self.model = PlaceholderModel()

    def simulate(self, request: SimulationRequest) -> SimulationResponse:
        reduction_factor = request.vehicle_reduction / 100.0

        before_geojson = {
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
                }
            ]
        }

        after_speed = 25 + (reduction_factor * 20)
        after_volume = 1200 * (1 - reduction_factor)

        after_geojson = {
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
                        "speed": round(after_speed, 2),
                        "congestion": "low" if reduction_factor > 0.3 else "moderate",
                        "volume": round(after_volume)
                    }
                }
            ]
        }

        metrics = {
            "before": Metrics(
                avg_speed=25.0,
                congestion_index=0.65,
                co2_reduction=0.0,
                aqi_improvement=0.0
            ),
            "after": Metrics(
                avg_speed=round(after_speed, 2),
                congestion_index=round(0.65 * (1 - reduction_factor), 2),
                co2_reduction=round(reduction_factor * 35.2, 2),
                aqi_improvement=round(reduction_factor * 15.5, 2)
            )
        }

        return SimulationResponse(
            before=before_geojson,
            after=after_geojson,
            metrics=metrics
        )
