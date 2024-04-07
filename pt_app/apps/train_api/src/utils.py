from datetime import timedelta

from redis import Redis
from rq import Queue
from rq.command import send_stop_job_command
from rq.exceptions import *
from rq.job import Job

from apps.train_api.src.tasks import train
from pkg.utils import get_elapsed_time
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


async def check_train_state() -> dict:
    redis = get_redis_client()
    try:
        job = Job.fetch(id=job_name, connection=redis)
        status = job.get_status()
        if status != "started":
            end_time = job.get_meta().get("end_time")
            train_time = end_time
        else:
            start_time = job.get_meta().get("start_time")
            train_time = str(timedelta(seconds=get_elapsed_time(start_time)))[:-4]
        return dict(state=job.get_status(),
                    training_time=train_time,
                    )
    except NoSuchJobError:
        return dict(error="no such job, training was not started")

