import time
from datetime import timedelta
from rq import get_current_job
from pkg.utils import get_elapsed_time


def train():
    job = get_current_job()
    job.meta["start_time"] = time.time()
    job.save_meta()
    i = 0
    while i < 10:
        time.sleep(1)
        i += 1
        print(i)
    job.meta["end_time"] = str(timedelta(seconds=get_elapsed_time(job.meta.get("start_time"))))[:-4]
    job.save_meta()
