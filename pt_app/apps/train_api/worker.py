from rq import Worker

from settings.rd import get_redis_client

w = Worker(['default'], connection=get_redis_client())
w.work()
