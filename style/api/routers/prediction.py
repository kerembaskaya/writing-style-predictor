from fastapi import APIRouter

from style.predict.servable.serve import get_model

router = APIRouter()


@router.get("/")
async def index():
    return {"success": True, "message": "Predictions Router is working!"}


@router.get("/predict")
async def predict(text: str):
    # model = get_model()
    # predictions = model.run_inference etc.
    return {
        "success": True,
        "predictions": {"Bon jovi": 0.15, "Kerem": 0.55, "Osman": 0.30},
    }
