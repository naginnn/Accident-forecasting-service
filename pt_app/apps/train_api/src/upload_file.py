import io
import os
from zipfile import ZipFile

import pandas as pd
import rq
from apps.train_api.src.tasks import prepare_dataset
from joblib import Parallel, delayed
from rq.job import Job, get_current_job
from sqlalchemy import create_engine


def upload_files_new(conn_str: str, bts: io.BytesIO) -> None:
    """ Переодическая задача, разбор архива и вызов парсинга. """  # noqa: D210
    db = create_engine(conn_str)
    job = get_current_job()
    # Загрузка файлов
    job.meta['stage'] = 0.0
    job.save_meta()

    with ZipFile(bts, 'r') as zip_file:
        res = Parallel(n_jobs=-2, verbose=10)(delayed(loop_for_file)
                                              (io.BytesIO(zip_file.open(xlxs_file.filename).read()), xlxs_file.filename)
                                              for xlxs_file in zip_file.filelist if
                                              '__MACOSX' not in xlxs_file.filename)
        files = {}
        for r in res:
            files.update(r)
        prepare_dataset(db,
                        files=files,
                        is_save_view=True,
                        is_agr_counter=True,
                        is_agr_train=True,
                        is_agr_predict=True,
                        is_predict=True,
                        is_weather_update=True)
        # prepare_dataset(db,
        #                 files=files,
        #                 is_save_view=True,
        #                 is_agr_counter=True,
        #                 is_agr_train=True,
        #                 is_agr_predict=True,
        #                 is_predict=True,
        #                 is_weather_update=True)


def loop_for_file(xlsx, filename):  # noqa: ANN001, ANN201
    match filename:
        case '13.xlsx':
            s = {filename: pd.read_excel(xlsx, usecols=[
                'geoData', 'geodata_center', 'UNOM'
            ])}
        case '12.xlsx':
            s = {filename: pd.read_excel(xlsx,
                                         usecols=["Департамент", "Класс энергоэффективности здания",
                                                  "Фактический износ здания, %",
                                                  "Год ввода здания в эксплуатацию"
                                                  ])}
        case '5.xlsx':
            s = {filename: pd.read_excel(xlsx, sheet_name='Выгрузка')}
        case '5.1.xlsx':
            s = {filename: pd.read_excel(xlsx, sheet_name='Выгрузка')}
        case '11.xlsx':
            s = {}
            s.update({filename + '_1': pd.read_excel(xlsx, sheet_name='Sheet 1')})
            s.update({filename + '_2': pd.read_excel(xlsx, sheet_name='Sheet 2')})
            s.update({filename + '_W': pd.read_excel(xlsx, sheet_name='Справочник Ошибки (W)')})
        case _:
            s = {filename: pd.read_excel(xlsx)}
    return s
