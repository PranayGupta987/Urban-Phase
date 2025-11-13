from fastapi import APIRouter, HTTPException
from api_clients.traffic_api import fetch_live_traffic
from api_clients.aqi_api import fetch_live_aqi
from api_clients.weather_api import fetch_live_weather

router = APIRouter()

@router.get("/traffic")
async def get_traffic_data():
    """
    Get live traffic data from HERE Maps API
    Falls back to mock data if API fails or API key is missing
    """
    try:
        data = fetch_live_traffic()
        return data
    except Exception as e:
        # Even if fetch_live_traffic fails, it should return mock data
        # But if something really goes wrong, return error
        raise HTTPException(status_code=500, detail=f"Failed to fetch traffic data: {str(e)}")

@router.get("/aqi")
async def get_aqi_data():
    """
    Get live AQI data from OpenAQ API
    Falls back to mock data if API fails
    """
    try:
        data = fetch_live_aqi()
        return data
    except Exception as e:
        # Even if fetch_live_aqi fails, it should return mock data
        # But if something really goes wrong, return error
        raise HTTPException(status_code=500, detail=f"Failed to fetch AQI data: {str(e)}")

@router.get("/weather")
async def get_weather_data():
    """
    Get live weather data from OpenWeather API
    Falls back to mock data if API fails or API key is missing
    Returns JSON with temp, humidity, and description
    """
    try:
        data = fetch_live_weather()
        return data
    except Exception as e:
        # Even if fetch_live_weather fails, it should return mock data
        # But if something really goes wrong, return error
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather data: {str(e)}")
