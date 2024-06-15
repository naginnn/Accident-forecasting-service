import io
import multiprocessing
import pickle
import sys
import threading
import time
from zipfile import ZipFile
from catboost import CatBoostClassifier
import requests
from joblib import Parallel, delayed
import rq
import pandas as pd
import numpy as np
from sklearn import preprocessing
from rq.job import Job, get_current_job
from sqlalchemy import text as sa_text, select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Connection, create_engine, NullPool, Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from apps.train_api.service.receive import (predict_data, save_unprocessed_data,
                                            get_unprocessed_data, get_processed_data, get_model)
from apps.train_api.service.train import train_model
from apps.train_api.service.update import save_for_view, save_for_predict, save_predicated, save_model_info
from apps.train_api.service.utils import (get_word, MultiColumnLabelEncoder,
                                          reverse_date, check_in_type, alpabet)
from pkg.utils import FakeJob
import os

# from settings.db import get_sync_session
# from settings.rd import get_redis_client

from apps.train_api.src._test_utils import log
from apps.train_api.service.aggregate.agr_unprocessed import AgrUnprocessed
from apps.train_api.service.aggregate.agr_view import AgrView
from apps.train_api.service.aggregate.agr_train import AgrTrain
from apps.train_api.service.aggregate.agr_event_counter import agr_events_counters


def update_progress(job: Job, progress: float, msg: str):
    job.meta['stage'] = progress
    job.meta['msg'] = msg
    job.save_meta()


@log
def get_data_from_excel() -> dict[str, pd.ExcelFile]:
    path_to_excel = "../../../autostart"
    return {
        filename: pd.ExcelFile(f"{path_to_excel}/{filename}", )
        for filename in os.listdir(path_to_excel)
    }


@log
def prepare_dataset(
        db: Engine,
        *,
        files: dict = None,
        is_save_view: bool = True,
        is_agr_counter: bool = True,
        is_agr_train: bool = True,
        is_agr_predict: bool = True,
        is_predict: bool = True,
        is_weather_update: bool = True,
) -> None:
    session = Session(db)
    # job = FakeJob.get_current_job()
    job = get_current_job()
    if files:
        update_progress(job=job, progress=15, msg="Сохранение необработанных данных")
        # 1. собираем и пред агрегируем входные данные
        tables = AgrUnprocessed.execute(tables=files)
        # 2. Сохраняем в схему unprocessed
        save_unprocessed_data(db=db, tables=tables)
        update_progress(job=job, progress=15, msg="Сохранено")
    if is_save_view:
        update_progress(job=job, progress=25, msg="Получение необработанных данных")
        # 3. Получаем все таблицы из схемы unprocessed
        tables = get_unprocessed_data(db=db)
        update_progress(job=job, progress=35, msg="Агрегация и чистка данных для представления")
        # 4. Пред агрегируем данные для записи в нормальную структуру
        agr_view_tables = AgrView.execute(tables=tables)
        update_progress(job=job, progress=45, msg="Сохранение данных")
        # 5. Записываем
        save_for_view(session=session, tables=agr_view_tables)
    # 1410 seconds = 18 minute
    if is_agr_counter:
        update_progress(job=job, progress=50, msg="Агрегация данных инцидент - счетчик")
        # агрегация показаний счетчика с потребителем и инцидентами
        agr_events_counters(db=db)
    update_progress(job=job, progress=55, msg="Загрузка агрегированных данных")
    # 6. Получаем все таблицы из схемы public
    processed = get_processed_data(db=db)

    if is_agr_train:
        update_progress(job=job, progress=60, msg="Агрегация и анализ данных для модели")
        agr_predict_df, agr_train_df = AgrTrain.execute(tables=processed)
        update_progress(job=job, progress=65, msg="Обучение модели и оценка точности")
        model, accuracy_score, feature_importances = train_model(train_df=agr_train_df)
        update_progress(job=job, progress=70, msg="Сохранение модели и метаинформации")
        save_model_info(session=session, model=model, accuracy_score=accuracy_score,
                        feature_importances=feature_importances)
        if is_agr_predict:
            is_agr_predict = False
            update_progress(job=job, progress=75, msg="Загрузка модели")
            save_for_predict(db=db, df_predict=agr_predict_df)
            if is_predict:
                update_progress(job=job, progress=85, msg="Предсказание и сохранение данных")
                predicated_df = predict_data(model=model, predict_df=agr_predict_df)
                save_predicated(session=session, predicated_df=predicated_df, events_df=processed.get('events_classes'))

    if is_agr_predict:
        update_progress(job=job, progress=75, msg="Загрузка модели")
        model = get_model(session=session)
        update_progress(job=job, progress=80, msg="Агрегация данных для предсказания")
        ## add custom agregate
        agr_predict_df, _ = AgrTrain.execute(tables=processed)
        save_for_predict(db=db, df_predict=agr_predict_df)
        if is_predict:
            update_progress(job=job, progress=85, msg="Предсказание и сохранение данных")
            predicated_df = predict_data(model=model, predict_df=agr_predict_df)
            save_predicated(session=session, predicated_df=predicated_df, events_df=processed.get('events_classes'))

    if is_weather_update:
        update_progress(job=job, progress=90, msg="Обновление данных о погодных условиях")
        update_weather_data()
        update_weather_consumers_fall_go()
    update_progress(job=job, progress=100, msg="Успешно")
    print("Все охуенно")


def loop(path, file_name):
    print(f"{path}/{file_name}")
    match file_name:
        case "13.xlsx":
            s = {file_name: pd.read_excel(f"{path}/{file_name}", usecols=[
                'geoData', 'geodata_center', 'UNOM'
            ])}
        case '12.xlsx':
            s = {file_name: pd.read_excel(f"{path}/{file_name}",
                                          usecols=["Департамент", "Класс энергоэффективности здания",
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


def upload_xlsx_faster(bytes: str):
    path = "/Users/sergeyesenin/GolandProjects/services01/pt_app/autostart"
    list_files = os.listdir(path)
    res = Parallel(n_jobs=-2, verbose=10)(delayed(loop)
                                          (path, file_name)
                                          for file_name in list_files)
    files = {}
    for r in res:
        files.update(r)
    return files


def update_weather_data():
    r = requests.post(
        url=f"http://{os.getenv('API_OBJ_HOST')}:{os.getenv('API_OBJ_PORT')}/api/v1/obj/weather/update"
    )
    return r.status_code


def update_weather_consumers_fall():
    r = requests.post(
        url=f"http://{os.getenv('API_OBJ_HOST')}:{os.getenv('API_OBJ_PORT')}/api/v1/obj/weather/calculate"
    )
    return r.status_code


def update_weather_consumers_fall_go():
    r = requests.post(
        url=f"http://{os.getenv('API_OBJ_HOST')}:{os.getenv('API_OBJ_PORT')}/api/v1/obj/weather/calculate_go"
    )
    return r.status_code


# if __name__ == '__main__':
#     from settings.db import sync_db
#
#     prepare_dataset(sync_db,
#                     files=None,
#                     is_save_view=False,
#                     is_agr_counter=False,
#                     is_agr_train=True,
#                     is_agr_predict=True,
#                     is_predict=True,
#                     is_weather_update=True
#                     )
