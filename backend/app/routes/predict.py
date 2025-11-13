from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ml.model import predictor

router = APIRouter()

class PredictionRequest(BaseModel):
    hour: int
    day_of_week: int
    temperature: float
    humidity: float
    is_rush_hour: Optional[int] = 0
    is_weekend: Optional[int] = 0

class PredictionResponse(BaseModel):
    predicted_aqi: float
    category: str
    recommendation: str

def get_aqi_category(aqi: float) -> tuple:
    if aqi <= 50:
        return ("Good", "Air quality is satisfactory")
    elif aqi <= 100:
        return ("Moderate", "Air quality is acceptable")
    elif aqi <= 150:
        return ("Unhealthy for Sensitive Groups", "Sensitive groups should reduce outdoor activity")
    elif aqi <= 200:
        return ("Unhealthy", "Everyone should reduce outdoor activity")
    elif aqi <= 300:
        return ("Very Unhealthy", "Everyone should avoid outdoor activity")
    else:
        return ("Hazardous", "Everyone should remain indoors")

@router.post("", response_model=PredictionResponse)
async def predict_aqi(request: PredictionRequest):
    try:
        features = request.dict()
        predicted_aqi = predictor.predict(features)

        category, recommendation = get_aqi_category(predicted_aqi)

        return PredictionResponse(
            predicted_aqi=round(predicted_aqi, 2),
            category=category,
            recommendation=recommendation
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
