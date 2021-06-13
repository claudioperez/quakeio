import json

from quakeio.utils.parseutils import open_quake

class QuakeEncoder(json.JSONEncoder):
    def default(self,obj):
        if hasattr(obj,"tolist"):
            return obj.tolist()
        return json.JSONEncoder.default(self,obj)

def read_json(read_file, **k):

    return json.load(read_file)


def write_json(write_file, ground_motion, indent=4, summarize=True, **kwds):
    if not summarize:
        ground_motion.serialize()
    with open_quake(write_file,"w") as f:
        json.dump(ground_motion, f, indent=indent, cls=QuakeEncoder)


def read_yaml(read_file, **k):
    import yaml

    return yaml.load(read_file, loader=yaml.Loader)


def write_yaml(write_file, ground_motion, summarize=True, **kwds):
    import yaml
    if not summarize:
        ground_motion.serialize()

    with open_quake(write_file,"w") as f:
        yaml.dump(ground_motion, f)


FILE_TYPES = {
    "json": {"write": write_json},
    "yaml": {"write": write_yaml},
    "json.record": {"read": read_json, "write": write_json},
    "yaml.record": {"read": read_yaml, "write": write_yaml},
}
