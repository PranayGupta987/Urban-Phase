from fastapi import APIRouter, HTTPException
from app.clients import traffic_client, aqi_client, weather_client
from app.cache import cache

router = APIRouter()

@router.get("/traffic")
async def get_traffic():
    cache_key = "traffic_data"
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        data = await traffic_client.get_traffic_data()
        cache.set(cache_key, data)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch traffic data: {str(e)}")

@router.get("/aqi")
async def get_aqi():
    cache_key = "aqi_data"
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        data = await aqi_client.get_aqi_data()
        cache.set(cache_key, data)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch AQI data: {str(e)}")

@router.get("/weather")
async def get_weather():
    cache_key = "weather_data"
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        data = await weather_client.get_weather_data()
        cache.set(cache_key, data)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather data: {str(e)}")
