from fastapi import APIRouter

from style.predict.servable.serve import get_servable

router = APIRouter()


@router.get("/")
async def index():
    return {"success": True, "message": "Predictions Router is working!"}


@router.get("/predict")
async def predict(text: str, model_name):
    servable = get_servable(model_name)
    prediction = servable.run_inference(text)
    return {"success": True, "prediction": prediction}


@router.get("/predicts")
async def predicts(text: str, model_name):
    servable = get_servable(model_name)
    predictions = servable.run_inference_multiclass(text)
    return {"success": True, "predictions": predictions}
