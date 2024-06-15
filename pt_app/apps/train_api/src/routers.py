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
from apps.train_api.src.upload_file import upload_files_new
from apps.train_api.src.utils import start_task, check_task_state
from pkg.auth import Authorization
from settings.db import sync_db, get_sync_session, conn_str
from settings.rd import get_redis_client

train_router = APIRouter(tags=["train"],
                         prefix="/api/v1/train",
                         responses=None)


# @train_router.get("/get_recommendations", status_code=200,
#                   dependencies=[Depends(Authorization(role='rw'))])

@train_router.post("/upload", status_code=200)
async def upload_data(file: UploadFile):
    """ Загрузка Zip файла """
    res, status = await check_task_state(job_id='upload_files')
    if status == "started":
        return {'result': res, 'state': status}

    contents = await file.read()
    bts = io.BytesIO(contents)
    res, ok = await start_task(f=upload_files_new, job_id='upload_files', conn_str=conn_str, bts=bts)
    return {'result': res, 'state': ok}


@train_router.get("/upload_state", status_code=200)
async def upload_state():
    """ Статус процесса"""
    res, status = await check_task_state(job_id='upload_files')
    return {'result': res, 'state': status}