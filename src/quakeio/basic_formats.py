import json
from copy import copy
from pathlib import Path

from quakeio.core import QuakeComponent, QuakeCollection, QuakeSeries
from quakeio.utils.parseutils import open_quake


class Unused:
    pass


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
    "json": {"read": read_json, "write": write_json},
    "yaml": {"read": read_yaml, "write": write_yaml},
    "quake.json": {"read": read_json, "write": write_json},
    "quake.yaml": {"read": read_yaml, "write": write_yaml},
}
