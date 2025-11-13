# API Clients for UrbanPulse
from .traffic_api import fetch_live_traffic
from .aqi_api import fetch_live_aqi
from .weather_api import fetch_live_weather

__all__ = ["fetch_live_traffic", "fetch_live_aqi", "fetch_live_weather"]

