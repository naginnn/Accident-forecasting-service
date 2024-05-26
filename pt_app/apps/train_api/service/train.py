import os
from typing import Tuple

import pandas as pd
from catboost import CatBoostClassifier, Pool, cv
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def train_model(train_df: pd.DataFrame) -> tuple[CatBoostClassifier, float, dict]:
    train_df.dropna(axis=0, how='any', inplace=True)
    X = train_df.drop(columns='event_id').copy()
    y = train_df['event_id']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = CatBoostClassifier(
        iterations=1000,
        # learning_rate=0.05,
        # depth=5,
        loss_function='MultiClass',
        eval_metric='Accuracy',
    )
    train_pool = Pool(
        data=X,
        label=y
    )
    test_pool = Pool(
        data=X_test,
        label=y_test
    )
    model.fit(
        X=train_pool,
        eval_set=test_pool,
        verbose=False,
        # plot=True,
        use_best_model=True,
    )
    feature_names = X_train.columns
    feature_importances = model.get_feature_importance()
    feature_importances_dict = {"feature_importances": []}
    for score, name in sorted(zip(feature_importances, feature_names), reverse=True):
        feature_importances_dict["feature_importances"].append({"name": name, "score": round(score, 2)})
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    # model.save_model(os.getenv("MODEL_PATH") + "/events.cbm")
    model.save_model("events.cbm")

    return model, accuracy, feature_importances_dict


class TrainModer:

    @staticmethod
    def train_model(df: pd.DataFrame) -> pd.DataFrame:
        return df
