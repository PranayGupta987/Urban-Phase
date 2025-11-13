"""
Prediction Router for UrbanPulse API
Provides endpoint for congestion level prediction
"""
from fastapi import APIRouter, HTTPException
from models.schemas_predict import PredictRequest, PredictResponse
from ml.model_loader import predict_from_dict

router = APIRouter()


@router.post("/predict", response_model=PredictResponse)
async def predict_congestion(request: PredictRequest):
    """
    Predict congestion level from input features
    
    Args:
        request: PredictRequest with feature values
    
    Returns:
        PredictResponse with predicted congestion level
    """
    try:
        # Convert Pydantic model to dict
        input_dict = request.dict(exclude_none=True)
        
        # Make prediction
        prediction = predict_from_dict(input_dict)
        
        return PredictResponse(prediction=prediction)
        
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Model not trained",
                "message": str(e)
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid input",
                "message": str(e)
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Prediction failed",
                "message": str(e)
            }
        )

