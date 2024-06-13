import io
import multiprocessing
import pickle
import sys
import threading
import time
from zipfile import ZipFile
from joblib import Parallel, delayed
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
from apps.train_api.service.receive import (collect_data, predict_data, save_unprocessed_data,
                                            get_unprocessed_data, get_processed_data)
from apps.train_api.service.train import train_model
from apps.train_api.service.update import save_for_view, save_for_predict, save_predicated, save_model_info
from apps.train_api.service.utils import (get_word, MultiColumnLabelEncoder,
                                          reverse_date, check_in_type, alpabet)
from pkg.utils import FakeJob
import os

from settings.db import get_sync_session
from settings.rd import get_redis_client

from apps.train_api.src._test_utils import log
from apps.train_api.service.aggregate.agr_unprocessed import AgrUnprocessed
from apps.train_api.service.aggregate.agr_view import AgrView
from apps.train_api.service.aggregate.agr_train import AgrTrain
from apps.train_api.service.aggregate.agr_event_counter import agr_events_counters


def update_progress(job: Job, progress: float, msg: str):
    print(progress, msg)
    job.meta['stage'] = progress
    job.meta['msg'] = msg
    job.save_meta()


async def upload_files(bts: io.BytesIO):
    """ Переодическая задача, разбор архива и вызов парсинга """
    # job = get_current_job()
    job = FakeJob.get_current_job()
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


# def load_data(files: dict, filename: str):
#     files[filename] = pd.ExcelFile(f"../../../autostart/{filename}", )


@log
def get_data_from_excel() -> dict[str, pd.ExcelFile]:
    path_to_excel = "../../../autostart"
    return {
        filename: pd.ExcelFile(f"{path_to_excel}/{filename}", )
        for filename in os.listdir(path_to_excel)
    }


@log
def prepare_dataset(**kwargs) -> None:
    PG_USR = os.getenv('POSTGRES_USER', 'username')
    PG_PWD = os.getenv('POSTGRES_PASSWORD', 'password')
    PG_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    PG_PORT = os.getenv('POSTGRES_PORT', '5432')
    PG_DB_NAME = os.getenv('POSTGRES_DB', 'postgres')
    db = create_engine(f'postgresql://{PG_USR}:{PG_PWD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}')
    session = Session(db)
    files = kwargs.get('files')
    save_view = kwargs.get('save_view')
    agr_counter = kwargs.get('agr_counter')
    job = FakeJob.get_current_job()
    # job = get_current_job()
    session = get_sync_session()
    start = time.time()
    if files:
        update_progress(job=job, progress=15, msg="Сохранение необработанных данных")
        # 1. собираем и пред агрегируем входные данные
        tables = AgrUnprocessed.execute(tables=files)
        # 2. Сохраняем в схему unprocessed
        save_unprocessed_data(db=db, tables=tables)
        print('success')
        return

    if save_view:
        update_progress(job=job, progress=25, msg="Получение необработанных данных")
        # 3. Получаем все таблицы из схемы unprocessed
        tables = get_unprocessed_data(db=db)
        #
        update_progress(job=job, progress=35, msg="Агрегация и чистка данных для представления")
        # 4. Пред агрегируем данные для записи в нормальную структуру
        agr_view_tables = AgrView.execute(tables=tables)
        update_progress(job=job, progress=45, msg="Сохранение данных")
        # 5. Записываем
        save_for_view(session=session, tables=agr_view_tables)

    if agr_counter:
        agr_events_counters(db=db)
    #
    # update_progress(job=job, progress=55, msg="Загрузка агрегированных данных")
    # # 6. Получаем все таблицы из схемы public
    processed = get_processed_data(db=db)
    # # #
    # update_progress(job=job, progress=65, msg="Агрегация и анализ данных для модели")
    agr_predict_df, agr_train_df = AgrTrain.execute(tables=processed)

    update_progress(job=job, progress=75, msg="Сохранение данных")
    save_for_predict(db=db, df_predict=agr_predict_df)
    #
    update_progress(job=job, progress=80, msg="Обучение модели и оценка точности")
    model, accuracy_score, feature_importances = train_model(train_df=agr_train_df)
    update_progress(job=job, progress=85, msg="Сохранение модели и метаинформации")
    save_model_info(session=session, model=model, accuracy_score=accuracy_score,
                    feature_importances=feature_importances)
    #
    ### mock data
    # from catboost import CatBoostClassifier
    # agr_predict_df = pd.read_sql("""select * from data_for_prediction""", db).drop('event_class', axis=1)
    # model = CatBoostClassifier().load_model("events.cbm")
    ### mock data
    update_progress(job=job, progress=90, msg="Расчет предсказаний")
    predicated_df = predict_data(model=model, predict_df=agr_predict_df)
    update_progress(job=job, progress=95, msg="Сохранение предсказаний")
    save_predicated(session=session, predicated_df=predicated_df, events_df=processed.get('events_classes'))

    update_progress(job=job, progress=100, msg="Выполнено успешно")
    print(time.time() - start)


def loop(path, file_name):
    print(f"{path}/{file_name}")
    match file_name:
        case "13.xlsx":
            s = {file_name: pd.read_excel(f"{path}/{file_name}" , usecols=[
                'geoData', 'geodata_center', 'UNOM'
            ])}
        case '12.xlsx':
            s = {file_name: pd.read_excel(f"{path}/{file_name}", usecols=["Департамент", "Класс энергоэффективности здания",
                                                                  "Фактический износ здания, %",
                                                                  "Год ввода здания в эксплуатацию"
                                                                  ])}
        case '5.xlsx':
            s = {file_name: pd.read_excel(f"{path}/{file_name}", sheet_name='Выгрузка')}
        case '5.1.xlsx':
            s = {file_name: pd.read_excel(f"{path}/{file_name}", sheet_name='Выгрузка')}
        case '11.xlsx':
            s = {}
            s.update({file_name + '_1': pd.read_excel(f"{path}/{file_name}", sheet_name='Sheet 1')})
            s.update({file_name + '_2': pd.read_excel(f"{path}/{file_name}", sheet_name='Sheet 2')})
            s.update({file_name + '_W': pd.read_excel(f"{path}/{file_name}", sheet_name='Справочник Ошибки (W)')})
        case _:
            s = {file_name: pd.read_excel(f"{path}/{file_name}")}
    return s


if __name__ == '__main__':


    start = time.time()
    path = "/Users/sergeyesenin/GolandProjects/services01/pt_app/autostart"
    list_files = os.listdir(path)

    # files = ['/Users/sergeyesenin/GolandProjects/services01/pt_app/autostart/6.xlsx',
    #          '/Users/sergeyesenin/GolandProjects/services01/pt_app/autostart/7.xlsx']
    res = Parallel(n_jobs=-2, verbose=10)(delayed(loop)
                                          (path, file_name)
                                          for file_name in list_files)

    files = {}
    for r in res:
        files.update(r)
    # files = get_data_from_excel()
    # prepare_dataset(files=files)
    print(time.time() - start)
    prepare_dataset(files=files, save_view=False, agr_counter=False)
    # prepare_dataset(files=files, save_view=False, agr_counter=False)
