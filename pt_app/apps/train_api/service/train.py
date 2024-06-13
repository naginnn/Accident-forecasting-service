import os
from typing import Tuple

import pandas as pd
from catboost import CatBoostClassifier, Pool, cv
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def train_model(train_df: pd.DataFrame) -> tuple[CatBoostClassifier, float, dict]:
    test_dataset = train_df.copy()[:10000]
    train_dataset = train_df.copy()[10000:]

    X = train_dataset.drop(columns='event_class').copy()
    y = train_dataset['event_class']
    x, x_test, y, y_test = train_test_split(X, y, test_size=0.2, random_state=4212)
    params_cb = {
        'loss_function': 'MultiClass',
        'eval_metric': 'Accuracy',
        'iterations': 500,
    }
    model = CatBoostClassifier(**params_cb)
    train_pool = Pool(
        data=x,
        label=y
    )
    test_pool = Pool(
        data=x_test,
        label=y_test
    )
    model.fit(
        train_pool,
        eval_set=test_pool,
        verbose=False,
        # plot=True,
        use_best_model=True,
    )

    feature_names = x.columns
    feature_importances = model.get_feature_importance()
    feature_importances_dict = {"feature_importances": []}
    for score, name in sorted(zip(feature_importances, feature_names), reverse=True):
        feature_importances_dict["feature_importances"].append({"name": name, "score": round(score, 2)})

    pred_y = model.predict(test_dataset.drop(columns='event_class'))
    test_y = test_dataset['event_class']
    accuracy = accuracy_score(test_y, pred_y)
    model.save_model("events.cbm")

    return model, accuracy, feature_importances_dict


class TrainModer:

    @staticmethod
    def train_model(df: pd.DataFrame) -> pd.DataFrame:
        return df
