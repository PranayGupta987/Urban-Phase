import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() == "true"

    TRAFFIC_API_KEY: str = os.getenv("TRAFFIC_API_KEY", "")
    AQI_API_KEY: str = os.getenv("AQI_API_KEY", "")
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")

    CITY_LAT: float = float(os.getenv("CITY_LAT", "40.7128"))
    CITY_LON: float = float(os.getenv("CITY_LON", "-74.0060"))
    CITY_NAME: str = os.getenv("CITY_NAME", "NewYork")

    CACHE_TTL: int = 300

settings = Settings()
