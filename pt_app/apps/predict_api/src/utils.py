import sqlalchemy

from apps.predict_api.src.service.prediction import PredictionService


async def get_recommendations(fields: str, model_name: str) -> list[dict]:
    p = PredictionService(fields, model_name)
    features = p.get_features()
    pool = p.prepare_features(features)
    predicts = p.get_predict(pool)
    return predicts
