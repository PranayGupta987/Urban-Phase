from fastapi import APIRouter
from services.traffic_service import TrafficService
from services.aqi_service import AQIService

router = APIRouter()
traffic_service = TrafficService()
aqi_service = AQIService()

@router.get("/traffic")
async def get_traffic_data():
    return traffic_service.get_traffic_geojson()

@router.get("/aqi")
async def get_aqi_data():
    return aqi_service.get_aqi_geojson()
