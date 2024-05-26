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

from apps.train_api.src.tasks import upload_files
from apps.train_api.src.utils import start_task, check_task_state
from pkg.auth import Authorization
from settings.db import sync_db, get_sync_session
from settings.rd import get_redis_client

train_router = APIRouter(tags=["train"],
                         prefix="/api/v1/train",
                         responses=None)


# @train_router.get("/get_recommendations", status_code=200,
#                   dependencies=[Depends(Authorization(role='rw'))])

@train_router.post("/upload", status_code=200)
async def upload_data(file: UploadFile):
    """ Загрузка Zip файла """
    res, ok = await check_task_state(job_id='upload_files')
    if ok:
        return {'result': res, 'state': ok}

    contents = await file.read()
    bts = io.BytesIO(contents)
    res, ok = await start_task(f=upload_files, job_id='upload_files', bts=bts)
    return {'result': res, 'state': ok}


@train_router.get("/upload_state", status_code=200)
async def upload_state():
    """ Загрузка Zip файла """
    res, ok = await check_task_state(job_id='upload_files')
    return {'result': res, 'state': ok}