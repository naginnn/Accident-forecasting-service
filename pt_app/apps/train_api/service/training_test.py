import io
import sys

import pandas as pd
import numpy as np
from sklearn import preprocessing
from rq.job import Job, get_current_job
from sqlalchemy import text as sa_text, select
from sqlalchemy.orm import sessionmaker, Session

from apps.train_api.service.agregate import agr_for_view, agr_for_train
from apps.train_api.service.receive import (collect_data, predict_data, save_unprocessed_data,
                                            get_unprocessed_data, get_processed_data)
from apps.train_api.service.train import train_model
from apps.train_api.service.update import save_for_view, save_for_predict, save_predicated
from apps.train_api.service.utils import (get_word, MultiColumnLabelEncoder,
                                          reverse_date, check_in_type, alpabet)
from pkg.utils import FakeJob
from pkg.ya_api import get_one_coordinate
from settings.db import DB_URL, get_sync_session, sync_db as db


def prepare_dataset(files: dict = None) -> None:
    job = FakeJob.get_current_job()
    session = get_sync_session()
    if files:
        save_unprocessed_data(db=db, files=files)
    tables = get_unprocessed_data(db=db)
    #
    agr_view_tables = agr_for_view(tables=tables)
    save_for_view(session=session, tables=agr_view_tables)
    #
    processed = get_processed_data(db=db)
    #
    agr_predict_df, agr_train_df = agr_for_train(tables=processed)
    save_for_predict(db=db, df_predict=agr_predict_df)

    model, accuracy_score = train_model(train_df=agr_train_df)
    #
    predicated_df = predict_data(model=model, predict_df=agr_predict_df)
    save_predicated(session=session, predicated_df=predicated_df, events_df=processed.get('event_types'))

    # get_weather

    # drop_weather_data(session=session)
    # session.commit()


def drop_weather_data(session: Session):
    pass


#     session.execute(sa_text(f"truncate table {ObjConsumerWeather.__tablename__}"))
#     # session.commit()


if __name__ == '__main__':
    files = {}
    # processed_data = pd.read_excel('test.xlsx', sheet_name='full')
    # files["test.xlsx"] = pd.ExcelFile("test.xlsx", )
    # prepare_dataset(files=files)
    prepare_dataset(files=None)
