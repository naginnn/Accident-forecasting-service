import io
import os
from datetime import datetime
from zipfile import ZipFile
import pandas as pd
from fastapi import APIRouter, Depends, UploadFile
from redis import Redis
from rq import Queue, get_current_job
from xlsx2csv import Xlsx2csv

from apps.train_api.src.utils import start_train, check_train_state
from settings.db import sync_db
from settings.rd import get_redis_client

train_router = APIRouter(tags=["train"],
                         prefix="/api/v1/train",
                         responses=None)


@train_router.post("/", status_code=200)
async def train_model() -> dict:
    result = await start_train()
    return result


@train_router.post("/state", status_code=200)
async def check_state() -> dict:
    result = await check_train_state()
    return result


@train_router.post("/upload", status_code=200)
async def upload(file: UploadFile):
    """ Загрузка Zip файла """
    contents = await file.read()
    bts = io.BytesIO(contents)
    # q = Queue(connection=Redis(host=os.environ.get('REDIS_HOST'),
    #                            port=int(os.environ.get('REDIS_PORT')))
    #           )
    await upload_files(bts)
    job = q.enqueue(upload_files, bts, job_timeout=50000)
    return {'id': job.id}


async def upload_files(bts: io.BytesIO):
    """ Переодическая задача, разбор архива и вызов парсинга """
    # job = get_current_job()
    # Загрузка файлов
    # job.meta['stage'] = 'init_files'
    # job.save_meta()

    files = {}
    with ZipFile(bts, "r") as zip_file:
        for xlxs_file in zip_file.filelist:
            if not '__MACOSX' in xlxs_file.filename:
                # or read csv -> faster
                files[xlxs_file.filename] = pd.read_excel(
                    io=io.BytesIO(zip_file.open(xlxs_file.filename).read()),
                    sheet_name=None,
                )
                x = files[xlxs_file.filename]['Sheet1'].to_sql(name='users', con=sync_db, if_exists='replace', index=False)
                # files[xlxs_file.filename].to_parquet("xlxs_file.filename.parquet", compression=None)
                # files[xlxs_file.filename] = io.BytesIO(zip_file.open(xlxs_file.filename).read())
                # main_df = pd.read_excel(io=files[xlxs_file.filename])
                # sheet_name=main_sheet,
                # skiprows=range(1, 2), dtype=str)
                # print(files[xlxs_file.filename])

    # start(files)
