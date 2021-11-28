import logging

from fastapi import FastAPI

from style.api.middleware import add_middleware
from style.api.routers import prediction
from style.config import settings

# from style.predict.servable.serve import get_model

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
add_middleware(app)

# get_model()


@app.get("/", tags=["Index"])
async def index():
    return {"success": True, "message": "Style Predictor is working!"}


app.include_router(
    prediction.router,
    prefix=settings.API_BASE_URL
    + "/Predictions",  # http://.../api/v1/Predictions/
    tags=["Predictions Router"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("style.main:app", host="0.0.0.0", reload=True, debug=True)
