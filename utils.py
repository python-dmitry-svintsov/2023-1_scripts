import time
from functools import wraps


class SingeltonMeta(type):
    _cash_table = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._cash_table:
            instance = super().__call__(*args, **kwargs)
            cls._cash_table[cls] = instance
        return cls._cash_table[cls]


def time_decorator(func):
    @wraps(func)
    def wrapper(*arg, **kwargs):
        start = time.perf_counter()
        res = func(*arg, **kwargs)
        stop = time.perf_counter()
        total_time = stop - start
        print('time of {} is: {}'.format(wrapper.__name__, '%.2f'%(total_time)))
        return res
    return wrapper


@time_decorator
def test():
    print('print first function')


if __name__ == '__main__':
    print(test.__dict__)