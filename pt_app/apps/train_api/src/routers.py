import io
import os
import time
from datetime import datetime
from zipfile import ZipFile
import pandas as pd
import sqlalchemy
from fastapi import APIRouter, Depends, UploadFile
from redis import Redis
from rq import Queue, get_current_job
from pydantic import BaseModel
from apps.train_api.src.utils import start_train, check_train_state, upload_files
from pkg.auth import Authorization
from settings.db import sync_db, get_sync_session
from settings.rd import get_redis_client

train_router = APIRouter(tags=["train"],
                         prefix="/api/v1/train",
                         responses=None)


@train_router.get("/get_recommendations", status_code=200,
                  dependencies=[Depends(Authorization(role='rw'))])
async def train_model() -> dict:
    start = time.time()
    # result = await start_train()
    return {"adress": "Байкальская", "unom": 123332, "server_time": time.time() - start}


@train_router.post("/", status_code=200)
async def train_model() -> dict:
    result = await start_train()
    return result





@train_router.post("/state", status_code=200)
async def check_state() -> dict:
    result = await check_train_state()
    return result
    # return {}


@train_router.post("/upload", status_code=200)
async def upload_data(file: UploadFile):
    """ Загрузка Zip файла """
    contents = await file.read()
    bts = io.BytesIO(contents)
    q = Queue(connection=Redis(host=os.environ.get('REDIS_HOST'),
                               port=int(os.environ.get('REDIS_PORT')))
              )
    await upload_files(bts)
    # job = q.enqueue(upload_files, bts, job_timeout=50000, job_id='upload_files')
    # return {'id': job.id}
    return {'id': 'ok'}


