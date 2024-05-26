import io
import sys
from zipfile import ZipFile

import rq
import pandas as pd
import numpy as np
from sklearn import preprocessing
from rq.job import Job, get_current_job
from sqlalchemy import text as sa_text, select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Connection, create_engine, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from apps.train_api.service.agregate import agr_for_view, agr_for_train
from apps.train_api.service.receive import (collect_data, predict_data, save_unprocessed_data,
                                            get_unprocessed_data, get_processed_data)
from apps.train_api.service.train import train_model
from apps.train_api.service.update import save_for_view, save_for_predict, save_predicated, save_model_info
from apps.train_api.service.utils import (get_word, MultiColumnLabelEncoder,
                                          reverse_date, check_in_type, alpabet)
from pkg.utils import FakeJob
import os


def update_progress(job: Job, progress: float, msg: str):
    job.meta['stage'] = progress
    job.meta['msg'] = msg
    job.save_meta()


async def upload_files(bts: io.BytesIO):
    """ Переодическая задача, разбор архива и вызов парсинга """
    job = get_current_job()
    # job = FakeJob.get_current_job()
    # Загрузка файлов
    # job.meta['stage'] = 0.0
    # job.save_meta()

    files = {}
    update_progress(job=job, progress=10, msg="Чтение архива")
    with ZipFile(bts, "r") as zip_file:
        for xlxs_file in zip_file.filelist:
            if '__MACOSX' not in xlxs_file.filename:
                files[xlxs_file.filename] = pd.ExcelFile(
                    io.BytesIO(zip_file.open(xlxs_file.filename).read()),
                )

        prepare_dataset(files=files)


def prepare_dataset(**kwargs) -> None:
    PG_USR = os.getenv('POSTGRES_USER', 'username')
    PG_PWD = os.getenv('POSTGRES_PASSWORD', 'password')
    PG_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    PG_PORT = os.getenv('POSTGRES_PORT', '5432')
    PG_DB_NAME = os.getenv('POSTGRES_DB', 'postgres')
    db = create_engine(f'postgresql://{PG_USR}:{PG_PWD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}')
    session = Session(db)
    files = kwargs.get('files')
    # job = FakeJob.get_current_job()
    job = get_current_job()
    # session = get_sync_session()
    if files:
        save_unprocessed_data(db=db, files=files)
        update_progress(job=job, progress=15, msg="Сохранение необработанных данных")
    update_progress(job=job, progress=25, msg="Получение необработанных данных")
    tables = get_unprocessed_data(db=db)
    #
    update_progress(job=job, progress=35, msg="Агрегация и чистка данных для представления")
    agr_view_tables = agr_for_view(tables=tables)
    update_progress(job=job, progress=45, msg="Сохранение данных")
    save_for_view(session=session, tables=agr_view_tables)
    #
    update_progress(job=job, progress=55, msg="Загрузка агрегированных данных")
    processed = get_processed_data(db=db)
    #
    update_progress(job=job, progress=65, msg="Агрегация и анализ данных для модели")
    agr_predict_df, agr_train_df = agr_for_train(tables=processed)
    update_progress(job=job, progress=75, msg="Сохранение данных")
    save_for_predict(db=db, df_predict=agr_predict_df)
    #
    update_progress(job=job, progress=80, msg="Обучение модели и оценка точности")
    model, accuracy_score, feature_importances = train_model(train_df=agr_train_df)
    update_progress(job=job, progress=85, msg="Сохранение модели и метаинформации")
    save_model_info(session=session, model=model, accuracy_score=accuracy_score,
                    feature_importances=feature_importances)
    #
    update_progress(job=job, progress=90, msg="Расчет предсказаний")
    predicated_df = predict_data(model=model, predict_df=agr_predict_df)
    update_progress(job=job, progress=95, msg="Сохранение предсказаний")
    save_predicated(session=session, predicated_df=predicated_df, events_df=processed.get('event_types'))

    update_progress(job=job, progress=100, msg="Выполнено успешно")


if __name__ == '__main__':
    files = {}
    # processed_data = pd.read_excel('test.xlsx', sheet_name='full')
    # files["test.xlsx"] = pd.ExcelFile("../../../autostart/test.xlsx", )
    # prepare_dataset(files=files)
    prepare_dataset(files=None)
