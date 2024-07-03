from collections.abc import Callable

from apps.train_api.src.tasks import update_progress
from rq import Queue
from rq.command import send_stop_job_command
from rq.exceptions import *  # noqa: F403
from rq.job import Job
from settings.rd import get_redis_client

job_name = 'train_job'




async def start_task(f: Callable, job_id: str, **kwargs) -> tuple[dict, bool]:  # noqa: D103, ANN003
    redis = get_redis_client()
    q = Queue(connection=redis, default_timeout=-1)
    try:
        send_stop_job_command(redis, job_id)
        job = q.enqueue(f=f, job_id=job_id, **kwargs)
    except NoSuchJobError:  # noqa: F405
        job = q.enqueue(f=f, job_id=job_id, **kwargs)
    except Exception as e:  # noqa: BLE001
        return {'error': str(e)}, False
    update_progress(job=job, progress=5, msg='Подготовка')
    status = job.get_status()
    if status in ['started', 'queued']:
        return job.get_meta(), True
    else:  # noqa: RET505
        return {'state': job.get_status()}, False


async def check_task_state(job_id: str) -> tuple[dict, str] | tuple[None, str]:  # noqa: D103
    redis = get_redis_client()
    try:
        job = Job.fetch(id=job_id, connection=redis)
        return job.get_meta(), job.get_status()
    except NoSuchJobError:  # noqa: F405
        return None, 'finished'


# async upload_sync():
