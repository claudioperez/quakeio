import numpy as np

from quakeio.core import QuakeSeries, QuakeComponent
from quakeio.utils.parseutils import open_quake


def read(read_file, **kwds):
    with open_quake(read_file, "r") as f:
        time_step = next(next(f))
        accel = np.genfromtxt(f, skip_header=1, delimiter=",", usecols=0)
    return QuakeComponent(
        QuakeSeries(accel), meta={"accel.time_step": time_step}
    )


def write(write_file, motion, label="eqsig data", **kwds):
    if isinstance(motion,QuakeSeries):
        accel = motion
    elif isinstance(motion,QuakeComponent):
        accel = motion.accel
    time_step = accel["time_step"]
    data = [label, f"{len(accel)} {time_step}", *map(str, accel.data)]
    with open_quake(write_file, "w") as f:
        f.write("\n".join(data))


FILE_TYPES = {"eqsig": {"read": read, "write": write}}

