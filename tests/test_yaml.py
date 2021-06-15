import tempfile

import quakeio

from .test_csmip import test_read

def dict_equal(d1,d2):
    pass

def test_round_trip():
    motion = test_read()
    with tempfile.TemporaryFile("w+") as fp:
        quakeio.write(fp, motion, "yaml", summarize=True)
        fp.seek(0)
        motion_2 = quakeio.read(fp, "yaml")
    

