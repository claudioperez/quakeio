import json
from copy import copy
from pathlib import Path

from quakeio.core import GroundMotionRecord, GroundMotionEvent
from quakeio.utils.parseutils import open_quake

class Unused: pass

class QuakeEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "tolist"):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def read_json(read_file, **kwds: Unused):

    return json.load(read_file)


def write_json(write_file, ground_motion, indent=4, summarize=True, **kwds):
    ground_motion = ground_motion.serialize(serialize_data = not summarize)
    with open_quake(write_file, "w") as f:
        json.dump(ground_motion, f, indent=indent, cls=QuakeEncoder)


def read_yaml(read_file, **k):
    import yaml

    return yaml.load(read_file, Loader=yaml.Loader)


def write_yaml(write_file, ground_motion, summarize=True, **kwds):
    import yaml

    ground_motion = write_pretty(ground_motion)
    ground_motion = ground_motion.serialize(serialize_data = not summarize)
    # if not summarize:
    #     ground_motion = ground_motion.serialize()


    with open_quake(write_file, "w") as f:
        yaml.dump(ground_motion, f)



def write_pretty(data):
    output = copy(data)
    schema_dir = Path(__file__).parents[2]/"etc/schemas"
    schema_file = schema_dir/"record.schema.json"
    with open(schema_file,"r") as f:
        schema = json.load(f)["properties"]
    if isinstance(data, GroundMotionRecord):
        for k in data:
            if k in schema and "units" not in k:
                output[schema[k]["title"]] = output.pop(k)
    elif isinstance(data, GroundMotionEvent):
        for name, event in data.items():
            print(event)
            output[name] = copy(event)
            for k,v in event.items():
                if k in schema and "units" not in k:
                    output[name][schema[k]["title"]] = output[name].pop(k)

    return output


FILE_TYPES = {
    "json": {"read": read_json, "write": write_json},
    "yaml": {"read": read_yaml, "write": write_yaml},
    "quake.json": {"read": read_json, "write": write_json},
    "quake.yaml": {"read": read_yaml, "write": write_yaml},
}
