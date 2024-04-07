import asyncio

from apps.train_api.src.utils import start_train, check_train_state
from settings.rd import get_redis_client

if __name__ == '__main__':
    # print(asyncio.run(start_train(redis=get_redis_client())))
    print(asyncio.run(check_train_state(redis=get_redis_client())))