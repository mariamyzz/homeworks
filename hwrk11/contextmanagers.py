from time import time 
from contextlib import contextmanager

#1 
class Lock(object):
    def __init__(self):
        self.lock = False

@contextmanager
def set_lock_true(value): 
    value.lock = True
    yield

#2
@contextmanager
def no_exceptions():
    try:
        yield
    except Exception as error:
        print(error)

#3 
class TimeIt(object):
    def __init__(self, obj):
        self.obj = obj

    def __enter__(self):
        self.obj.start_time = time()
        return self.obj

    def __exit__(self, *args):
        self.obj.end_time = time()
        self.obj.time = self.obj.start_time - self.obj.end_time

# testing = Lock()

# with set_lock_true(testing):
#     print(testing.lock)

# with no_exceptions():
#     print(1/0)

# print('done')

# testing2 = Lock()

# with TimeIt(testing2) as t:
#     print('Hello World!')
#     print('Hello World!')
#     print('Hello World!')
#     print(2**66)

# print('Execution time was:', testing2.time)