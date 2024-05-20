from quakeio.core import QuakeSeries, QuakeComponent, QuakeCollection
from quakeio.utils.parseutils import open_quake
import numpy


def read(read_file, **kwds):
    with open_quake(read_file) as f:
        pass


def write(write_file, ground_motion, **kwds):
    # print(type(ground_motion))
    if isinstance(ground_motion, QuakeComponent):
        dt = ground_motion.accel["time_step"]
        accel = numpy.asarray(ground_motion.accel.data)[:, None]
    elif isinstance(ground_motion, QuakeSeries):
        dt = ground_motion["time_step"]
        accel = numpy.asarray(ground_motion.data)[:, None]
    else:
        raise ValueError(
            f"Cannot conver motion of type `{type(ground_motion)}` to QuakeComponent"
        )
    with open_quake(write_file, "w") as f:
        #numpy.savetxt(f, accel, fmt="%.8f")  # delimiter="\n")
        f.write(f"-dt {dt} -values {{")
        numpy.savetxt(f, accel, fmt="%.8f", delimiter=" ")
        f.write("}")

def write_tcl(write_file, ground_motion, **kwds):
    if isinstance(ground_motion, QuakeComponent):
        series = ground_motion.accel
    elif isinstance(ground_motion, QuakeSeries):
        series = ground_motion
    else:
        raise ValueError(
            f"Cannot conver motion of type `{type(ground_motion)}` to QuakeComponent"
        )
    with open_quake(write_file, "w") as f:
        f.write(f"dt {series['time_step']} ")
        for k,v in series.items():
            if isinstance(v,(str,int,float)):
                f.write(f"{k} {v} ")
        f.write(f"values {{")
        numpy.savetxt(f, series.data, fmt="%.8f", delimiter=" ")
        f.write("}")


FILE_TYPES = {
    "opensees": {"write": write, "type": "any"},
    "tcl":      {"write": write_tcl, "type": "any"}
}
