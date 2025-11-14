from fastapi import APIRouter, HTTPException
from api_clients.traffic_api import fetch_live_traffic
from api_clients.aqi_api import fetch_live_aqi
from api_clients.weather_api import fetch_live_weather
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/traffic")
async def get_traffic_data():
    """Get live traffic data - returns valid GeoJSON FeatureCollection"""
    try:
        data = fetch_live_traffic()
        # Validate structure
        if not isinstance(data, dict) or data.get("type") != "FeatureCollection":
            logger.error("Invalid GeoJSON structure from traffic API")
            raise HTTPException(status_code=500, detail="Invalid data format")
        if "features" not in data:
            data["features"] = []
        logger.info(f"Returning {len(data.get('features', []))} traffic features")
        return data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_traffic_data: {e}", exc_info=True)
        try:
            fallback = fetch_live_traffic()
            if isinstance(fallback, dict) and fallback.get("type") == "FeatureCollection":
                logger.info(
                    f"Returning fallback traffic data with {len(fallback.get('features', []))} features"
                )
                return fallback
        except Exception as inner:
            logger.error(f"Fallback traffic fetch failed: {inner}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch traffic data: {str(e)}"
        )

@router.get("/aqi")
async def get_aqi_data():
    """Get live AQI data - returns valid GeoJSON FeatureCollection"""
    try:
        data = fetch_live_aqi()
        # Validate structure
        if not isinstance(data, dict) or data.get("type") != "FeatureCollection":
            logger.error("Invalid GeoJSON structure from AQI API")
            raise HTTPException(status_code=500, detail="Invalid data format")
        if "features" not in data:
            data["features"] = []
        logger.info(f"Returning {len(data.get('features', []))} AQI features")
        return data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_aqi_data: {e}", exc_info=True)
        try:
            fallback = fetch_live_aqi()
            if isinstance(fallback, dict) and fallback.get("type") == "FeatureCollection":
                logger.info(
                    f"Returning fallback AQI data with {len(fallback.get('features', []))} features"
                )
                return fallback
        except Exception as inner:
            logger.error(f"Fallback AQI fetch failed: {inner}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch AQI data: {str(e)}"
        )

@router.get("/weather")
async def get_weather_data():
    """Get live weather data - returns JSON object"""
    try:
        data = fetch_live_weather()
        return data
    except Exception as e:
        logger.error(f"Error in get_weather_data: {e}", exc_info=True)
        try:
            return fetch_live_weather()
        except:
            raise HTTPException(status_code=500, detail=f"Failed to fetch weather data: {str(e)}")
