import inspect


import quakeio


modules = [quakeio.csmip, quakeio.nga]


def validate_read_signature(read_func):
    sig = inspect.signature(read_func)


for m in modules:
    pass
