import io
from datetime import timedelta
from zipfile import ZipFile

import pandas as pd
from redis import Redis
from rq import Queue
from rq.command import send_stop_job_command
from rq.exceptions import *
from rq.job import Job, get_current_job

from apps.train_api.service.training_test import prepare_dataset
from apps.train_api.src.tasks import train
from pkg.utils import get_elapsed_time, FakeJob
from settings.rd import get_redis_client

job_name = "train_job"


# states = ["queued", "started", "deferred", "finished", "stopped", "scheduled", "canceled", "failed"]


async def start_train() -> dict:
    redis = get_redis_client()
    q = Queue(connection=redis, default_timeout=-1)
    try:
        send_stop_job_command(redis, job_name)
        job = q.enqueue(f=train, job_id=job_name)
    except NoSuchJobError:
        job = q.enqueue(f=train, job_id=job_name)
    except Exception as e:
        return dict(error=str(e))
    status = job.get_status()
    if status in ["started", "queued"]:
        return dict(state="started")
    else:
        return dict(state=job.get_status())


async def check_train_state(job_name='upload_files') -> dict:
    redis = get_redis_client()
    try:
        job = Job.fetch(id=job_name, connection=redis)
        return dict(**job.get_meta())
    except NoSuchJobError:
        return dict(error="no such job, training was not started")


# async def check_train_state(job_name='upload_files') -> dict:
#     redis = get_redis_client()
#     try:
#         job = Job.fetch(id=job_name, connection=redis)
#         status = job.get_status()
#         if status != "started":
#             end_time = job.get_meta().get("end_time")
#             train_time = end_time
#         else:
#             start_time = job.get_meta().get("start_time")
#             train_time = str(timedelta(seconds=get_elapsed_time(start_time)))[:-4]
#         return dict(state=job.get_status(),
#                     training_time=train_time,
#                     )
#     except NoSuchJobError:
#         return dict(error="no such job, training was not started")


async def upload_files(bts: io.BytesIO):
    """ Переодическая задача, разбор архива и вызов парсинга """
    # job = get_current_job()
    job = FakeJob.get_current_job()
    # Загрузка файлов
    job.meta['stage'] = 0.0
    job.save_meta()

    files = {}
    with ZipFile(bts, "r") as zip_file:
        for xlxs_file in zip_file.filelist:
            if not '__MACOSX' in xlxs_file.filename:
                # or read csv -> faster
                # files[xlxs_file.filename] = pd.read_excel(
                #     io=io.BytesIO(zip_file.open(xlxs_file.filename).read()),
                #     sheet_name=None,
                # )

                files[xlxs_file.filename] = pd.ExcelFile(
                    io.BytesIO(zip_file.open(xlxs_file.filename).read()),
                )
                job.meta['stage'] += 5
                job.save_meta()
                # df1 = pd.read_excel(files.get(xlxs_file.filename), 'Sheet1')
                # # df1 = files.get(xlxs_file.filename).get('Sheet1')
                # x = files[xlxs_file.filename]['Sheet1'].to_sql(name='users', con=sync_db, if_exists='replace',
                #                                                index=False)
        prepare_dataset(files=files)