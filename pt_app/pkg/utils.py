import time


def get_elapsed_time(start_time: float):
    return round(time.time() - start_time, 2)