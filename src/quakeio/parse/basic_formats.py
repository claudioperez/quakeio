import json
from copy import copy
from pathlib import Path

from quakeio.core import QuakeComponent, QuakeCollection, QuakeSeries
from quakeio.utils.parseutils import open_quake


class Unused:
    pass

def write_text(write_file, ground_motion, **kwds):
    import numpy
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
        numpy.savetxt(f, accel, fmt="%.8f", delimiter="\n")


class QuakeEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "tolist"):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def read_basic(data:dict):
    if "motions" in data:
        for motion in data["motions"]:
            for component in motion["components"]:
                pass
    else:
        raise ValueError()
    pass

def create_series(data):
    series = data.pop("data")
    return QuakeSeries(series, meta=data)

def read_json(read_file, **kwds: Unused):

    return json.load(read_file)


def write_json(write_file, ground_motion, indent=4, summarize=False, **kwds):
    ground_motion = ground_motion.serialize(serialize_data=not summarize)
    try:
        with open_quake(write_file, "w") as f:
            json.dump(ground_motion, f, indent=indent, cls=QuakeEncoder)
    except BrokenPipeError:
        pass

def dumps_json(ground_motion, indent=4, summarize=False, **kwds):
    ground_motion = ground_motion.serialize(serialize_data=not summarize)
    return json.dumps(ground_motion, indent=indent, cls=QuakeEncoder)


def read_yaml(read_file, **k):
    import yaml

    return yaml.load(read_file, Loader=yaml.Loader)


def write_yaml(write_file, ground_motion, summarize=False, **kwds):
    import yaml

    ground_motion = ground_motion.serialize(serialize_data=not summarize)
    # if not summarize:
    #     ground_motion = ground_motion.serialize()

    with open_quake(write_file, "w") as f:
        yaml.dump(ground_motion, f)


FILE_TYPES = {
    "txt":  {"write": write_text},
    "json": {"read": read_json, "write": write_json},
    "yaml": {"read": read_yaml, "write": write_yaml},
    "quake.json": {"read": read_json, "write": write_json},
    "quake.yaml": {"read": read_yaml, "write": write_yaml},
}
