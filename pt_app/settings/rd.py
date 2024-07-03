import os
import redis

RD_HOST = os.environ.get('REDIS_HOST')
RD_PORT = os.environ.get('REDIS_PORT')
RD_DB = os.environ.get('REDIS_DB')

# url = f"redis://{RD_HOST}:{RD_PORT}/{RD_DB}"
url = f"redis://{RD_HOST}:{RD_PORT}"


def get_redis_client():
    return redis.Redis.from_url(url)


