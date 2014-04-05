import time


def timer_decorator(f):
    def wrap(*args, **kwargs):
        startTime = time.time()
        f(*args, **kwargs)
        print('Function {0} execution time: {1:.5f}'.format(f.__name__, time.time() - startTime))
    return wrap


@timer_decorator
def func():
    time.sleep(3)


func()