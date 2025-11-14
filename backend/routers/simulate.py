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
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/simulate")

def _geojson_to_segments(geojson: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Convert GeoJSON FeatureCollection to list of segment dictionaries"""
    segments = []
    
    if not isinstance(geojson, dict) or geojson.get("type") != "FeatureCollection":
        logger.error("Invalid GeoJSON structure")
        return segments
    
    if "features" not in geojson:
        return segments
    
    for idx, feature in enumerate(geojson["features"]):
        if not isinstance(feature, dict) or feature.get("type") != "Feature":
            continue
            
        props = feature.get("properties", {})
        geometry = feature.get("geometry", {})
        
        if not geometry or geometry.get("type") != "LineString":
            continue
        
        segment_id = props.get("segment_id", props.get("id", props.get("link_id", idx + 1)))
        
        avg_speed = float(props.get("speed", props.get("avg_speed", 30.0)))
        vehicle_count = int(props.get("vehicle_count", props.get("volume", 100)))
        congestion_level = props.get("congestion_level")
        
        if congestion_level is None:
            congestion = props.get("congestion", "moderate")
            if isinstance(congestion, str):
                congestion_map = {"low": 0.2, "moderate": 0.5, "high": 0.8}
                congestion_level = congestion_map.get(congestion.lower(), 0.5)
            else:
                congestion_level = float(congestion)
        else:
            congestion_level = float(congestion_level)
        
        segments.append({
            "segment_id": int(segment_id),
            "geometry": geometry,
            "avg_speed": avg_speed,
            "vehicle_count": vehicle_count,
            "congestion_level": congestion_level,
            "properties": props
        })
    
    return segments

def _create_geojson(segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create GeoJSON FeatureCollection from segments - guaranteed valid"""
    features = []
    
    for seg in segments:
        congestion_level = seg["congestion_level"]
        if congestion_level < 0.4:
            congestion = "low"
        elif congestion_level < 0.7:
            congestion = "moderate"
        else:
            congestion = "high"
        
        feature = {
            "type": "Feature",
            "geometry": seg["geometry"],
            "properties": {
                "segment_id": seg["segment_id"],
                "avg_speed": seg["avg_speed"],
                "vehicle_count": seg["vehicle_count"],
                "congestion_level": seg["congestion_level"],
                "speed": seg["avg_speed"],
                "congestion": congestion,
                **{k: v for k, v in seg.get("properties", {}).items() if k not in ["segment_id", "avg_speed", "vehicle_count", "congestion_level", "speed", "congestion"]}
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
        if isinstance(aqi_data, dict) and "features" in aqi_data:
            aqi_values = [
                f.get("properties", {}).get("aqi", 75)
                for f in aqi_data["features"][:5]
                if isinstance(f, dict) and "aqi" in f.get("properties", {})
            ]
            if aqi_values:
                return float(sum(aqi_values) / len(aqi_values))
    except Exception as e:
        logger.error(f"Error getting AQI: {e}", exc_info=True)
    return 75.0

def _get_weather_data() -> Dict[str, float]:
    """Get current weather data"""
    try:
        weather = fetch_live_weather()
        return {
            "temperature": float(weather.get("temp", weather.get("temperature", 25.0))),
            "humidity": float(weather.get("humidity", 70.0)),
            "wind_speed": float(weather.get("wind_speed", 10.0)),
            "rainfall": float(weather.get("rainfall", 0.0))
        }
    except Exception as e:
        logger.error(f"Error getting weather: {e}", exc_info=True)
        return {
            "temperature": 25.0,
            "humidity": 70.0,
            "wind_speed": 10.0,
            "rainfall": 0.0
        }

@router.post("", response_model=SimulationResponse)
async def run_simulation(request: SimulationRequest):
    """Simulate traffic reduction scenario.

    vehicle_reduction may be provided either as:
    - a fraction in [0, 1]
    - a percentage in (1, 100], which will be converted to a fraction.
    """
    try:
        logger.info("Simulation request received", extra={
            "vehicle_reduction": request.vehicle_reduction,
            "segment_ids": request.segment_ids,
        })

        # Normalise vehicle_reduction into a fraction in [0, 1]
        raw_reduction = float(request.vehicle_reduction)
        if raw_reduction < 0:
            raise HTTPException(
                status_code=400,
                detail="vehicle_reduction must be non-negative",
            )

        if raw_reduction > 1:
            # Treat as percentage 0-100
            if raw_reduction > 100:
                raise HTTPException(
                    status_code=400,
                    detail="vehicle_reduction percentage cannot exceed 100",
                )
            reduction_factor = raw_reduction / 100.0
            logger.info(
                "vehicle_reduction provided as percent; normalised to fraction",
                extra={"raw": raw_reduction, "fraction": reduction_factor},
            )
        else:
            # Already a fraction 0-1
            reduction_factor = raw_reduction
            logger.info(
                "vehicle_reduction provided as fraction",
                extra={"fraction": reduction_factor},
            )
        
        # Check model availability (non-blocking)
        model = get_model()
        if model is None:
            logger.info("ML model not available, using heuristic predictions")
        
        # Load traffic data
        logger.info("Fetching live traffic data for simulation")
        traffic_geojson = fetch_live_traffic()
        segments = _geojson_to_segments(traffic_geojson)

        if not segments:
            logger.warning("No segments found in live traffic; retrying fallback")
            traffic_geojson = fetch_live_traffic()
            segments = _geojson_to_segments(traffic_geojson)
            if not segments:
                logger.error("Simulation has no traffic segments even after fallback")
                raise HTTPException(
                    status_code=500,
                    detail="No traffic segments found in data"
                )
        
        if request.segment_ids:
            segments = [s for s in segments if s["segment_id"] in request.segment_ids]
        
        if not segments:
            raise HTTPException(
                status_code=400,
                detail=f"No segments found matching IDs: {request.segment_ids}"
            )
        logger.info("Computing simulation with reduction factor", extra={
            "reduction_factor": reduction_factor,
        })

        weather = _get_weather_data()
        logger.info("Weather data for simulation", extra=weather)
        aqi_before = _get_aqi_value()
        logger.info("Baseline AQI for simulation", extra={"aqi_before": aqi_before})
        
        before_segments = [s.copy() for s in segments]
        before_geojson = _create_geojson(before_segments)
        
        avg_congestion_before = sum(s["congestion_level"] for s in before_segments) / len(before_segments)
        avg_speed_before = sum(s["avg_speed"] for s in before_segments) / len(before_segments)
        
        after_segments = []
        
        for seg in segments:
            new_vehicle_count = max(1, int(seg["vehicle_count"] * (1 - reduction_factor)))
            
            input_dict = {
                "avg_speed": seg["avg_speed"],
                "vehicle_count": new_vehicle_count,
                "pm25": aqi_before * 0.5,
                "temperature": weather["temperature"],
                "humidity": weather["humidity"],
                "wind_speed": weather["wind_speed"],
                "rainfall": weather["rainfall"],
                "segment_id": seg["segment_id"]
            }
            
            try:
                new_congestion = predict_from_dict(input_dict)
            except Exception as e:
                logger.warning(f"Prediction failed: {e}, using fallback")
                new_congestion = max(0.0, min(1.0, seg["congestion_level"] * (1 - reduction_factor * 0.5)))
            
            new_speed = max(5.0, seg["avg_speed"] * (1 - new_congestion * 0.3))
            
            new_seg = seg.copy()
            new_seg["avg_speed"] = new_speed
            new_seg["vehicle_count"] = new_vehicle_count
            new_seg["congestion_level"] = new_congestion
            
            after_segments.append(new_seg)
        
        after_geojson = _create_geojson(after_segments)
        
        avg_congestion_after = sum(s["congestion_level"] for s in after_segments) / len(after_segments)
        avg_speed_after = sum(s["avg_speed"] for s in after_segments) / len(after_segments)
        
        avg_congestion_impact = (avg_congestion_before + avg_congestion_after) / 2
        aqi_after = max(0, aqi_before * (1 - avg_congestion_impact * 0.1))
        
        metrics = Metrics(
            avg_congestion_before=round(avg_congestion_before, 3),
            avg_congestion_after=round(avg_congestion_after, 3),
            avg_speed_before=round(avg_speed_before, 2),
            avg_speed_after=round(avg_speed_after, 2),
            aqi_before=round(aqi_before, 1),
            aqi_after=round(aqi_after, 1)
        )
        
        logger.info(f"Simulation complete: {len(after_segments)} segments processed")
        
        return SimulationResponse(
            before=before_geojson,
            after=after_geojson,
            metrics=metrics
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Simulation error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Simulation failed",
                "message": str(e)
            }
        )
