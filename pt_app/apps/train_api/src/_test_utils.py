from datetime import datetime
from functools import wraps


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        def message(end=False, value=None, delta_ts=None):
            dt = datetime.now()
            if delta_ts:
                x = f"LOG:\t{dt} dt: ({delta_ts}) - {func.__name__}({args}, {kwargs})"
            else:
                x = f"LOG:\t{dt} - {func.__name__}({args}, {kwargs})"
            if end:
                x = f"{x} Result -> {value}\n"
            return dt, "... ...".join(([x], [x[:100], x[-100:]])[len(x) > 200])

        dt_start, msg = message()
        print(msg)
        result = func(*args, **kwargs)
        _, msg = message(end=True, value=result, delta_ts=datetime.now()-dt_start)
        print(msg)
        return result

    return wrapper
