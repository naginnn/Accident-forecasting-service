from fastapi import APIRouter
from apps.predict_api.src.utils import get_recommendations

predict_router = APIRouter(
    tags=["predict"],
    prefix="/api/v1/predict",
    responses=None,
)


@predict_router.get("/", status_code=200)
async def predict_model(fields: str, model_name: str = 'default') -> list[dict]:
    rec = await get_recommendations(fields, model_name)
    return rec
