from fastapi import APIRouter
from models.schemas import SimulationRequest, SimulationResponse
from services.simulation_service import SimulationService

router = APIRouter()
simulation_service = SimulationService()

@router.post("/simulate", response_model=SimulationResponse)
async def run_simulation(request: SimulationRequest):
    return simulation_service.simulate(request)
