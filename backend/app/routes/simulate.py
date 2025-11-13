from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import copy

router = APIRouter()

class SimulationRequest(BaseModel):
    traffic_reduction: float
    apply_green_zones: bool = False

class SimulationResponse(BaseModel):
    original_metrics: Dict[str, float]
    simulated_metrics: Dict[str, float]
    improvements: Dict[str, float]
    geojson_layers: Dict[str, Any]

def apply_traffic_reduction(traffic_data: Dict, reduction_percent: float) -> Dict:
    simulated = copy.deepcopy(traffic_data)

    if 'features' in simulated:
        for feature in simulated['features']:
            if 'properties' in feature and 'traffic_volume' in feature['properties']:
                original = feature['properties']['traffic_volume']
                feature['properties']['traffic_volume'] = original * (1 - reduction_percent / 100)
                feature['properties']['simulated'] = True

    return simulated

def calculate_aqi_improvement(traffic_reduction: float, green_zones: bool) -> float:
    aqi_improvement = traffic_reduction * 0.6

    if green_zones:
        aqi_improvement += 15

    return aqi_improvement

@router.post("", response_model=SimulationResponse)
async def run_simulation(request: SimulationRequest):
    try:
        from app.clients import traffic_client, aqi_client

        traffic_data = await traffic_client.get_traffic_data()
        aqi_data = await aqi_client.get_aqi_data()

        original_traffic = sum(
            f['properties'].get('traffic_volume', 0)
            for f in traffic_data.get('features', [])
        ) / max(len(traffic_data.get('features', [])), 1)

        original_aqi = sum(
            f['properties'].get('aqi', 0)
            for f in aqi_data.get('features', [])
        ) / max(len(aqi_data.get('features', [])), 1)

        simulated_traffic_data = apply_traffic_reduction(
            traffic_data,
            request.traffic_reduction
        )

        simulated_traffic = original_traffic * (1 - request.traffic_reduction / 100)

        aqi_reduction = calculate_aqi_improvement(
            request.traffic_reduction,
            request.apply_green_zones
        )
        simulated_aqi = max(0, original_aqi - aqi_reduction)

        simulated_aqi_data = copy.deepcopy(aqi_data)
        for feature in simulated_aqi_data.get('features', []):
            if 'properties' in feature:
                feature['properties']['aqi'] = max(
                    0,
                    feature['properties'].get('aqi', 0) - aqi_reduction
                )

        return SimulationResponse(
            original_metrics={
                "avg_traffic": round(original_traffic, 2),
                "avg_aqi": round(original_aqi, 2)
            },
            simulated_metrics={
                "avg_traffic": round(simulated_traffic, 2),
                "avg_aqi": round(simulated_aqi, 2)
            },
            improvements={
                "traffic_reduction": round(request.traffic_reduction, 2),
                "aqi_reduction": round(aqi_reduction, 2)
            },
            geojson_layers={
                "traffic": simulated_traffic_data,
                "aqi": simulated_aqi_data
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")
