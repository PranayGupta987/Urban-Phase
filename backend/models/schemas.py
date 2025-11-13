from pydantic import BaseModel, Field
from typing import Dict, Any

class SimulationRequest(BaseModel):
    vehicle_reduction: float = Field(
        ...,
        ge=0,
        le=100,
        description="Percentage of vehicle reduction (0-100)"
    )

class Metrics(BaseModel):
    avg_speed: float
    congestion_index: float
    co2_reduction: float
    aqi_improvement: float

class SimulationResponse(BaseModel):
    before: Dict[str, Any]
    after: Dict[str, Any]
    metrics: Dict[str, Metrics]
