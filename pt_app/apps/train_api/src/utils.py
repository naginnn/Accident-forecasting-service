import io
import os
import threading
from datetime import timedelta
from typing import Tuple, Dict, Any, Callable
from zipfile import ZipFile

import pandas as pd
from redis import Redis
from rq import Queue
from rq.command import send_stop_job_command
from rq.exceptions import *
from rq.job import Job, get_current_job

from apps.train_api.src.tasks import update_progress, prepare_dataset
from pkg.utils import get_elapsed_time, FakeJob
from settings.rd import get_redis_client

job_name = "train_job"


# states = ["queued", "started", "deferred", "finished", "stopped", "scheduled", "canceled", "failed"]


async def start_task(f: Callable, job_id: str, **kwargs) -> Tuple[dict, bool]:
    redis = get_redis_client()
    q = Queue(connection=redis, default_timeout=-1)
    try:
        send_stop_job_command(redis, job_id)
        job = q.enqueue(f=f, job_id=job_id, **kwargs)
    except NoSuchJobError:
        job = q.enqueue(f=f, job_id=job_id, **kwargs)
    except Exception as e:
        return dict(error=str(e)), False
    update_progress(job=job, progress=5, msg="Подготовка")
    status = job.get_status()
    if status in ["started", "queued"]:
        return job.get_meta(), True
    else:
        return dict(state=job.get_status()), False


async def check_task_state(job_id: str) -> Tuple[dict, str] | Tuple[None, str]:
    redis = get_redis_client()
    try:
        job = Job.fetch(id=job_id, connection=redis)
        return job.get_meta(), job.get_status()
    except NoSuchJobError:
        return None, "finished"
        # return dict(error="no such job, job was not started"), False



# async def check_train_state(job_name='upload_files') -> dict:
#     redis = get_redis_client()
#     mo
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


# async upload_sync():
