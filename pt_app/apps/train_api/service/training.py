import os
import pickle
import pandas as pd
from catboost import CatBoostClassifier, Pool
from settings.db import sync_db
from settings.rd import get_redis_client


class TrainService:
    """
    *** This class is responsible for receiving training a model  **
    :param fields str objects ids example: objId1, objId2, objId3, objId4
    :param model_name str name of model name
    :return a TrainerService object
    """
    def __init__(self, fields: str, model_name: str = 'default'):
        self.fields = fields
        self.name = model_name
        self.table_name = os.getenv('MODEL_TABLE', 'mytableindb')
        self.storage = os.getenv('MODEL_PLACEMENT', 'fs')
        self.conn = sync_db
        self.redis = get_redis_client()
        self.params = {
            'loss_function': 'MultiClass',
            'eval_metric': 'Accuracy',
            'iterations': 100,
            'verbose': False,
            'learning_rate': 0.05,
            'depth': 10,
            'random_seed': 42
        }
        self.model = CatBoostClassifier(**self.params)

    def get_features(self) -> pd.DataFrame:
        """
        :return a pd.DataFrame features
        """
        query = f"""SELECT {','.join(self.fields)} FROM {self.table_name}"""
        return pd.read_sql(sql=query, con=self.conn)

    def prepare_features(self, df: pd.DataFrame) -> Pool:
        """
        :param df pd.DataFrame
        :return a catboost.Pool
        """
        return Pool(data=df[df.columns[1:]], label=df['x'])

    def train(self, train_pool: Pool):
        """
        :param train_pool catboost.Pool
        :return None
        """
        self.model.fit(train_pool)

    def test_model(self):
        """"test trained model
        :returns
        dict test metrics
        """
        pass

    def save_model(self):
        """"
        save trained model
        :returns None
        """
        if self.storage == 'fs':
            self.model.save_model(f"{os.getenv('MODEL_FS_PATH')}/{self.name}", format="cbm")
        elif self.storage == 'redis':
            "save_to_redis"
            self.redis.set(self.name, pickle.dumps(self.model))

# if __name__ == '__main__':
#     ts = TrainerService()
#     # ts.get_features(table="features_table", fields=["x", "y"])
#     df = pd.DataFrame({"x": [1, 2, 3, 4], "y": [1, 2, 3, 4]})
#     pool = ts.prepare_features(df)
#     ts.train(train_pool=pool)
#     ts.save_model(storage='fs')
#     ts.get_model(storage='fs')
#     print(ts.model.predict(df))
# ts.save_model()
