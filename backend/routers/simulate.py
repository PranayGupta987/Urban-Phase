"""
Simulation Router for UrbanPulse API
Simulates traffic reduction scenarios using ML predictions
"""
from fastapi import APIRouter, HTTPException
from models.schemas_predict import SimulationRequest, SimulationResponse, Metrics
from ml.model_loader import predict_from_dict, get_model
from api_clients.traffic_api import fetch_live_traffic
from api_clients.aqi_api import fetch_live_aqi
from api_clients.weather_api import fetch_live_weather
import json
from typing import Dict, Any, List

router = APIRouter()


def _geojson_to_segments(geojson: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Convert GeoJSON FeatureCollection to list of segment dictionaries
    
    Args:
        geojson: GeoJSON FeatureCollection
    
    Returns:
        List of segment dictionaries with properties
    """
    segments = []
    
    if "features" not in geojson:
        return segments
    
    for idx, feature in enumerate(geojson["features"]):
        props = feature.get("properties", {})
        geometry = feature.get("geometry", {})
        
        # Extract segment ID or use index
        segment_id = props.get("segment_id", props.get("id", idx + 1))
        
        # Extract traffic properties
        avg_speed = props.get("speed", props.get("avg_speed", 30.0))
        vehicle_count = props.get("vehicle_count", props.get("volume", 100))
        congestion_level = props.get("congestion_level", props.get("congestion", 0.5))
        
        # Normalize congestion if it's a string
        if isinstance(congestion_level, str):
            congestion_map = {"low": 0.2, "moderate": 0.5, "high": 0.8}
            congestion_level = congestion_map.get(congestion_level.lower(), 0.5)
        
        segments.append({
            "segment_id": segment_id,
            "geometry": geometry,
            "avg_speed": float(avg_speed),
            "vehicle_count": int(vehicle_count),
            "congestion_level": float(congestion_level),
            "properties": props
        })
    
    return segments


def _create_geojson(segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create GeoJSON FeatureCollection from segments
    
    Args:
        segments: List of segment dictionaries
    
    Returns:
        GeoJSON FeatureCollection
    """
    features = []
    
    for seg in segments:
        feature = {
            "type": "Feature",
            "geometry": seg["geometry"],
            "properties": {
                **seg.get("properties", {}),
                "segment_id": seg["segment_id"],
                "avg_speed": seg["avg_speed"],
                "vehicle_count": seg["vehicle_count"],
                "congestion_level": seg["congestion_level"]
            }
        }
        features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "features": features
    }


def _get_aqi_value() -> float:
    """Get current AQI value from API or mock data"""
    try:
        aqi_data = fetch_live_aqi()
        if "features" in aqi_data and len(aqi_data["features"]) > 0:
            # Get average AQI from first few features
            aqi_values = [
                f.get("properties", {}).get("aqi", 75)
                for f in aqi_data["features"][:5]
                if "aqi" in f.get("properties", {})
            ]
            return float(sum(aqi_values) / len(aqi_values)) if aqi_values else 75.0
    except:
        pass
    return 75.0  # Default AQI


def _get_weather_data() -> Dict[str, float]:
    """Get current weather data"""
    try:
        weather = fetch_live_weather()
        return {
            "temperature": weather.get("temp", 25.0),
            "humidity": weather.get("humidity", 70.0),
            "wind_speed": weather.get("wind_speed", 10.0) if "wind_speed" in weather else 10.0,
            "rainfall": 0.0  # Weather API doesn't provide rainfall in current implementation
        }
    except:
        return {
            "temperature": 25.0,
            "humidity": 70.0,
            "wind_speed": 10.0,
            "rainfall": 0.0
        }


@router.post("/simulate", response_model=SimulationResponse)
async def run_simulation(request: SimulationRequest):
    """
    Simulate traffic reduction scenario
    
    Args:
        request: SimulationRequest with vehicle_reduction and optional segment_ids
    
    Returns:
        SimulationResponse with before/after GeoJSON and metrics
    """
    try:
        # Check if model is available
        try:
            get_model()
        except FileNotFoundError:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "Model not trained",
                    "message": "Please train the model first using 'python backend/ml/train_model.py'"
                }
            )
        
        # Load traffic data
        traffic_geojson = fetch_live_traffic()
        segments = _geojson_to_segments(traffic_geojson)
        
        if not segments:
            raise HTTPException(
                status_code=500,
                detail="No traffic segments found in data"
            )
        
        # Filter segments if segment_ids specified
        if request.segment_ids:
            segments = [s for s in segments if s["segment_id"] in request.segment_ids]
        
        if not segments:
            raise HTTPException(
                status_code=400,
                detail=f"No segments found matching IDs: {request.segment_ids}"
            )
        
        # Get weather and AQI data
        weather = _get_weather_data()
        aqi_before = _get_aqi_value()
        
        # Create BEFORE state
        before_segments = segments.copy()
        before_geojson = _create_geojson(before_segments)
        
        # Calculate BEFORE metrics
        avg_congestion_before = sum(s["congestion_level"] for s in before_segments) / len(before_segments)
        avg_speed_before = sum(s["avg_speed"] for s in before_segments) / len(before_segments)
        
        # Simulate AFTER state
        after_segments = []
        
        for seg in segments:
            # Apply vehicle reduction
            new_vehicle_count = int(seg["vehicle_count"] * (1 - request.vehicle_reduction))
            
            # Prepare input for ML prediction
            input_dict = {
                "avg_speed": seg["avg_speed"],
                "vehicle_count": new_vehicle_count,
                "pm25": aqi_before * 0.5,  # Rough conversion from AQI to PM2.5
                "temperature": weather["temperature"],
                "humidity": weather["humidity"],
                "wind_speed": weather["wind_speed"],
                "rainfall": weather["rainfall"],
                "segment_id": seg["segment_id"]
            }
            
            # Predict new congestion level
            try:
                new_congestion = predict_from_dict(input_dict)
            except:
                # Fallback: simple heuristic
                new_congestion = max(0.0, min(1.0, seg["congestion_level"] * (1 - request.vehicle_reduction * 0.5)))
            
            # Predict new speed: speed = max(old_speed * (1 - congestion), 5)
            new_speed = max(5.0, seg["avg_speed"] * (1 - new_congestion))
            
            # Create new segment
            new_seg = seg.copy()
            new_seg["avg_speed"] = new_speed
            new_seg["vehicle_count"] = new_vehicle_count
            new_seg["congestion_level"] = new_congestion
            
            after_segments.append(new_seg)
        
        # Create AFTER GeoJSON
        after_geojson = _create_geojson(after_segments)
        
        # Calculate AFTER metrics
        avg_congestion_after = sum(s["congestion_level"] for s in after_segments) / len(after_segments)
        avg_speed_after = sum(s["avg_speed"] for s in after_segments) / len(after_segments)
        
        # Predict new AQI: new_aqi = old_aqi * (1 + congestion_level * 0.2)
        avg_congestion_impact = (avg_congestion_before + avg_congestion_after) / 2
        aqi_after = aqi_before * (1 + avg_congestion_impact * 0.2)
        
        # Create metrics
        metrics = Metrics(
            avg_congestion_before=round(avg_congestion_before, 3),
            avg_congestion_after=round(avg_congestion_after, 3),
            avg_speed_before=round(avg_speed_before, 2),
            avg_speed_after=round(avg_speed_after, 2),
            aqi_before=round(aqi_before, 1),
            aqi_after=round(aqi_after, 1)
        )
        
        return SimulationResponse(
            before=before_geojson,
            after=after_geojson,
            metrics=metrics
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Simulation failed",
                "message": str(e)
            }
        )
