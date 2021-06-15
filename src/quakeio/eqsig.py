import numpy as np

from quakeio.core import (
    GroundMotionSeries,
    GroundMotionRecord
)
from quakeio.utils.parseutils import open_quake


def read(read_file, **kwds):
    with open_quake(read_file, "r") as f:
        time_step = next(next(f))
        accel = np.genfromtxt(f, skip_header=1, delimiter=",", usecols=0)
    return GroundMotionRecord(
        GroundMotionSeries(accel), meta={"accel.time_step": time_step}
    )


def write(write_file, motion: GroundMotionSeries, label="eqsig data", **kwds):
    print(dir(motion.accel))
    print(dir(motion))
    time_step = motion.accel.time_step
    data = [label, f"{len(motion.accel)} {time_step}", *map(str, motion.accel)]
    with open_quake(write_file, "w") as f:
        f.write("\n".join(data))


FILE_TYPES = {"eqsig": {"read": read, "write": write}}
