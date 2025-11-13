import httpx
import json
from typing import Dict, Any
from pathlib import Path
from app.config import settings

class APIClient:
    def __init__(self):
        self.demo_mode = settings.DEMO_MODE
        self.demo_path = Path(__file__).parent.parent / "demo"

    async def _load_demo_data(self, filename: str) -> Any:
        file_path = self.demo_path / filename
        with open(file_path, 'r') as f:
            return json.load(f)

class TrafficClient(APIClient):
    async def get_traffic_data(self) -> Dict[str, Any]:
        if self.demo_mode:
            return await self._load_demo_data("traffic.json")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.example.com/traffic",
                    params={
                        "lat": settings.CITY_LAT,
                        "lon": settings.CITY_LON,
                        "apikey": settings.TRAFFIC_API_KEY
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Traffic API error: {e}, falling back to demo data")
            return await self._load_demo_data("traffic.json")

class AQIClient(APIClient):
    async def get_aqi_data(self) -> Dict[str, Any]:
        if self.demo_mode:
            return await self._load_demo_data("aqi.json")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.example.com/aqi",
                    params={
                        "lat": settings.CITY_LAT,
                        "lon": settings.CITY_LON,
                        "apikey": settings.AQI_API_KEY
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"AQI API error: {e}, falling back to demo data")
            return await self._load_demo_data("aqi.json")

class WeatherClient(APIClient):
    async def get_weather_data(self) -> Dict[str, Any]:
        if self.demo_mode:
            return await self._load_demo_data("weather.json")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.example.com/weather",
                    params={
                        "lat": settings.CITY_LAT,
                        "lon": settings.CITY_LON,
                        "apikey": settings.WEATHER_API_KEY
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Weather API error: {e}, falling back to demo data")
            return await self._load_demo_data("weather.json")

traffic_client = TrafficClient()
aqi_client = AQIClient()
weather_client = WeatherClient()
