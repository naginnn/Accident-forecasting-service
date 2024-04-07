import os
import pickle
import pandas as pd
from catboost import CatBoostClassifier, Pool
from settings.db import sync_db
from settings.rd import get_redis_client


class PredictionService:
    """
    *** This class is responsible for receiving recommendations from the model  **
    :param model_name str name of model name
    :return a PredictionService object
    """

    def __init__(self, fields: str, model_name: str = 'default'):
        self.fields = fields
        self.name = model_name
        self.table_name = os.getenv('MODEL_TABLE', 'mytableindb')
        self.storage = os.getenv('MODEL_PLACEMENT', 'fs')
        self.conn = sync_db
        self.redis = get_redis_client()
        self.model = self.__load_model()

    def __load_model(self) -> CatBoostClassifier:
        """
        :return a CatBoostClassifier model or None
        """
        model = None
        if self.storage == 'fs':
            model = CatBoostClassifier().load_model(f"{os.getenv('MODEL_FS_PATH')}/{self.name}")
        elif self.storage == 'redis':
            model = pickle.loads(self.redis.get(self.name))
        return model

    def get_features(self) -> pd.DataFrame:
        """
        :return a pd.DataFrame features
        """
        query = f"SELECT * FROM {self.table_name} WHERE unom in ('{self.fields}')"
        return pd.read_sql(query, self.conn)

    def prepare_features(self, df: pd.DataFrame) -> Pool:
        """
        :param df pd.DataFrame
        :return a catboost.Pool
        """
        return Pool(data=df[df.columns[1:]])

    def get_predict(self, predict_pool: Pool) -> list:
        """
        :param predict_pool catboost.Pool
        :return a list of predictions float64 [[]]
        """
        if self.model:
            # return self.model.predict(predict_pool)
            return self.model.predict_proba(predict_pool)
        else:
            return []

    def get_predictions(self, predictions: list[float]) -> list:
        """
        :param predictions list[float]
        :return a list of reccomendations str []
        """
        print(predictions)
        return []


if __name__ == '__main__':
    p = PredictionService()
    # p.prepare_fields("12321,2132,3213,3213,3211")
    df = pd.DataFrame({"x": [1, 2, 3, 4], "y": [1, 2, 3, 4]})
    pool = p.prepare_features(df)
    p.get_predict(pool)
