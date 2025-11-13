class PlaceholderModel:
    def __init__(self):
        self.model_name = "UrbanPulse Simulation Model v1.0"

    def predict_traffic(self, vehicle_reduction: float):
        speed_increase = vehicle_reduction * 0.5
        congestion_decrease = vehicle_reduction * 0.8

        return {
            "speed_improvement": speed_increase,
            "congestion_reduction": congestion_decrease
        }

    def predict_aqi(self, vehicle_reduction: float):
        aqi_improvement = vehicle_reduction * 0.4

        return {
            "aqi_improvement": aqi_improvement,
            "pm25_reduction": vehicle_reduction * 0.6
        }
