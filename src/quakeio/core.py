# Claudio Perez
# 2021
import json
from copy import copy
from pathlib import Path
import warnings

import numpy as np

DIRECTIONS = ["long", "tran", "up"]


class GroundMotionEvent(dict):
    """
    Container for a collection of GroundMotionRecord objects
    """

    def __init__(self, records, event_date=None, **kwds):
        dict.__init__(self, **records)
        self.event_date = event_date

    def serialize(self, serialize_data=True, **kwds) -> dict:
        return {k: v.serialize(**kwds) for k, v in self.items()}

    def get_component(self, **kwds):
        for record in self.values():
            for component in record.values():
                if all(component[k] == v for k, v in kwds.items()):
                    return component


class GroundMotionRecord(dict):
    """
    A container of `GroundMotionComponent` objects.
    """

    def __init__(self, records: dict = {}, event=None, **kwds):
        self._event = event
        dict.__init__(self, **records)

    def serialize(self, serialize_data=True, **kwds) -> dict:
        return {k: v.serialize(**kwds) for k, v in self.items()}

    def rotate(self, angle=None, rotation=None):
        rx, ry = (
            np.array([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]])
            if not rotation else rotation
        )
        try:
            for attr in ["accel", "veloc", "displ"]:
                x = getattr(self["long"], attr)
                y = getattr(self["tran"], attr)
                X = np.array([x, y])
                x[:] = np.dot(rx, X)
                y[:] = np.dot(ry, X)

                x, y = map(lambda d: self[d][f"peak_{attr}"], ["long", "tran"])
                X = np.array([x, y])
                self["long"][f"peak_{attr}"] = float(np.dot(rx, X))
                self["tran"][f"peak_{attr}"] = float(np.dot(ry, X))
        except KeyError as e:
            raise AttributeError("Attempt to rotate a record that"\
                    f"does not have a '{e.args[0]}' component")

        return self

    def resultant(self):
        displ, veloc, accel = [GroundMotionSeries(
          sum(
            getattr(self[dirn],vect) ** 2
            for dirn in ["long", "tran", "up"] if dirn in self and self[dirn]
          )
        ) for vect in ("displ", "veloc", "accel")]
        return GroundMotionComponent(accel, veloc, displ)

    def __sub__(self, other):
        ret = copy(self)
        for dirn in DIRECTIONS:
            ret[dirn] = (
                self[dirn] - other[dirn] if dirn in other and dirn in self else None
            )
        return ret


class GroundMotionComponent(dict):
    schema_dir = Path(__file__).parents[2] / "etc/schemas"
    schema_file = schema_dir / "component.schema.json"

    def __init__(self, accel, veloc, displ, record=None, meta={}):
        self.accel = accel
        self.displ = displ
        self.veloc = veloc
        self._record = record
        dict.__init__(self, **meta)

    def serialize(
        self,
        ljust=0,
        serialize_data=True,
        serialize_series=True,
        humanize_keys=False,
        **kwds,
    ) -> dict:
        if humanize_keys:
            key_name = get_schema_key_map(self.schema_file)
            ret = {key_name(k).ljust(ljust, "."): val for k, val in self.items()}
        else:
            ret = dict(self)
        if serialize_series:
            ret.update(
                {
                    **self.accel.serialize(
                        "accel", serialize_data=serialize_data, **kwds
                    ),
                    **self.veloc.serialize(
                        "veloc", serialize_data=serialize_data, **kwds
                    ),
                    **self.displ.serialize(
                        "displ", serialize_data=serialize_data, **kwds
                    ),
                }
            )
        return ret

    def __sub__(self, other):
        ret = copy(self)
        if isinstance(other, GroundMotionComponent):
            for k in ["accel", "veloc", "displ"]:
                setattr(ret, k, getattr(other, k) - getattr(self, k))

        elif isinstance(other, (float, int)):
            for k in ["accel", "veloc", "displ"]:
                setattr(ret, k, other - getattr(self, k))
        return ret

    def __add__(self, other):
        ret = copy(self)
        if isinstance(other, GroundMotionComponent):
            for k in ["accel", "veloc", "displ"]:
                setattr(ret, k, getattr(other, k) + getattr(self, k))

        elif isinstance(other, (float, int)):
            for k in ["accel", "veloc", "displ"]:
                setattr(ret, k, other + getattr(self, k))
        return ret

    def __mul__(self, other):
        ret = copy(self)
        if isinstance(other, GroundMotionComponent):
            for k in ["accel", "veloc", "displ"]:
                setattr(ret, k, getattr(other, k) * getattr(self, k))
        elif isinstance(other, (float, int)):
            for k in ["accel", "veloc", "displ"]:
                setattr(ret, k, other * getattr(self, k))

        return ret

    def __rmul__(self, other):
        return self.__mul__(other)


class GroundMotionSeries(np.ndarray):
    def __new__(cls, input_array, metadata={}):
        obj = np.asarray(input_array).view(cls)

        for k, v in metadata.items():
            if not hasattr(obj, k):
                setattr(obj, k, v)
        return obj

    def serialize(
        self, key=None, summarize=False, serialize_data=True, humanize_keys=False
    ):
        if key is None:
            key = self.series_type

        attributes = {
            ".".join((key, k)): v for k, v in self.__dict__.items() if k[0] != "_"
        }
        if serialize_data and not summarize:
            attributes.update({key: list(self)})
        return attributes

    def __array_finalize__(self, obj):
        for k, v in self.__dict__.items():
            setattr(obj, k, v)

    def plot(self, ax=None, fig=None):
        import matplotlib.pyplot as plt

        if ax is None:
            fig, ax = plt.subplots()
        ax.plot(self)


def rotate(data, angle):
    output = copy(data)
    if isinstance(data, GroundMotionComponent):
        raise Exception("Unable to rotate single component")

    elif isinstance(data, GroundMotionEvent):
        for name, record in data.items():
            try:
                record.rotate(angle)
            except KeyError:
                warnings.warn(f"Not rotating record {name}")


def get_schema_key_map(schema_file):
    with open(schema_file, "r") as f:
        schema = json.load(f)["properties"]

    def get_name(key):
        return schema[key]["title"] if key in schema else key

    return get_name


def write_pretty(data):
    output = copy(data)
    schema_dir = Path(__file__).parents[2] / "etc/schemas"
    schema_file = schema_dir / "component.schema.json"
    with open(schema_file, "r") as f:
        schema = json.load(f)["properties"]
    if isinstance(data, GroundMotionComponent):
        for k in data:
            if k in schema and "units" not in k:
                output[schema[k]["title"]] = output.pop(k)
            else:
                pass

    elif isinstance(data, GroundMotionEvent):
        for name, record in data.items():
            output[name] = copy(record)
            for dirn, component in record.items():
                output[name][dirn] = copy(component)
                for k, v in component.items():
                    if k in schema and "units" not in k:
                        output[name][dirn][schema[k]["title"]] = output[name][dirn].pop(
                            k
                        )
                    else:
                        pass

    return output
