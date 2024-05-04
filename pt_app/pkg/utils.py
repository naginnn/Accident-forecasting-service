import time


def get_elapsed_time(start_time: float):
    return round(time.time() - start_time, 2)


class FakeJob:
    meta = {}

    @staticmethod
    def get_current_job():
        return FakeJob()

    def save_meta(self):
        pass
