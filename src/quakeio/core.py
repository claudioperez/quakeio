# Claudio Perez
# 2021
import json
from copy import copy
from pathlib import Path
import warnings

import numpy as np

DIRECTIONS = ["long", "tran", "up"]


class QuakeCollection(dict):
    """
    Container for a collection of QuakeMotion objects
    """

    def __init__(self, motions, event_date=None, meta=None, **kwds):
        meta = meta if meta is not None else {}
        dict.__init__(self, **meta)
        self.motions = motions
        self.event_date = event_date

    def __repr__(self):
        return f"QuakeCollection({dict.__repr__(self)})"

    def serialize(self, serialize_data=True, **kwds) -> dict:
        #return {k: v.serialize(**kwds) for k, v in self.items()}
        return {"motions": [i.serialize(**kwds) for i in self.motions.values()]}

    def match(self, **kwds):
        pass

    def at(self,**kwds):
        for motion in self.motions.values():
            if all(k in motion and motion[k] == v for k, v in kwds.items()):
                return motion

        return self.get_component(**kwds)

    def get_component(self, **kwds):
        for motion in self.motions.values():
            for component in motion.components.values():
                if all(component[k] == v for k, v in kwds.items()):
                    return component


class QuakeMotion(dict):
    """
    A container of `QuakeComponent` objects.
    """
    def _update_components(f):
        def wrapped(*args, **kwds):
            res = f(*args, **kwds)
            [getattr(cmp,s)._refresh() 
                    for cmp in res.components.values()
                        for s in ["accel","veloc","displ"] if hasattr(cmp,s)]
            return res
        return wrapped

    def __init__(self, components: dict = None, meta:dict=None):
        dict.__init__(self)
        self.directions = ["long", "tran", "up"]
        self.components = components if components is not None else {}
        #for k,v in self.components.items():
        #    setattr(self,k,v)
        self.update(meta if meta is not None else {})

    @property
    def long(self):
        return self.components["long"]
    @property
    def tran(self):
        return self.components["tran"]

    def __repr__(self):
        #return f"QuakeMotion({dict.__repr__(self)})"
        return f"QuakeMotion({dict.__repr__(self)})"
    
    def __sub__(self, other):
        ret = copy(self)
        ret.components = {}
        for dirn in DIRECTIONS:
            if dirn in other.components and dirn in self.components:
                ret.components[dirn] = (
                    self.components[dirn] - other.components[dirn] 
                )
        return ret
    
    def __add__(self, other):
        ret = copy(self)
        ret.components = {}
        for dirn in DIRECTIONS:
            ret.components[dirn] = (
                self.components[dirn] + other.components[dirn] 
                if dirn in other.components and dirn in self.components else None
            )
        return ret
    
    def __rsub__(self, other):
        return self.__sub__(other)
    
    def __radd__(self, other):
        return self.__add__(other)


    def serialize(self, serialize_data=True, **kwds) -> dict:
        return {
            **self,
            "components": [c.serialize(**kwds) for c in self.components.values()]
        }

    @_update_components
    def rotate(self, angle=None, rotation=None):
        rx, ry = (
            np.array([[ np.cos(angle), np.sin(angle)], 
                      [-np.sin(angle), np.cos(angle)]])
            if not rotation else rotation
        )
        try:
            for attr in ["accel", "veloc", "displ"]:
                x = getattr(self.components["long"], attr).data
                y = getattr(self.components["tran"], attr).data
                X = np.array([x, y])
                x[:] = np.dot(rx, X)
                y[:] = np.dot(ry, X)

                #x, y = map(lambda d: self.components[d][f"peak_{attr}"], ["long", "tran"])
                #X = np.array([x, y])
                #self.components["long"][f"peak_{attr}"] = float(np.dot(rx, X))
                #self.components["tran"][f"peak_{attr}"] = float(np.dot(ry, X))

        except KeyError as e:
            raise AttributeError("Attempt to rotate a motion that"\
                    f"does not have a '{e.args[0]}' component")

        return self

    def resultant(self):
        # initialize
        series = {k:None for k in ("displ", "veloc", "accel")}
        for typ in series.keys():
            try:
                series[typ] = sum(
                    getattr(self.components[dirn],typ) ** 2
                    for dirn in self.directions 
                        if dirn in self.components and self.components[dirn]
                )
            except AttributeError as e:
                raise e
        return QuakeComponent(*series.values())


class QuakeComponent(dict):
    schema_dir = Path(__file__).parents[2] / "etc/schemas"
    schema_file = schema_dir / "component.schema.json"

    def __init__(self, accel, veloc, displ, record=None, meta=None):
        meta = meta if meta is not None else {}
        self.accel = accel
        self.displ = displ
        self.veloc = veloc
        self._record = record
        dict.__init__(self, **meta)

    def __repr__(self):
        return f"QuakeComponent({self['file_name']}) at {hex(id(self))}"

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
                    "accel": self.accel.serialize(
                        "accel", serialize_data=serialize_data, **kwds
                    ),
                    "veloc": self.veloc.serialize(
                        "veloc", serialize_data=serialize_data, **kwds
                    ),
                    "displ": self.displ.serialize(
                        "displ", serialize_data=serialize_data, **kwds
                    ),
                }
            )
        return ret

    def __sub__(self, other):
        ret = copy(self)
        if isinstance(other, QuakeComponent):
            for k in ["accel", "veloc", "displ"]:
                setattr(ret, k, getattr(other, k) - getattr(self, k))

        elif isinstance(other, (float, int)):
            for k in ["accel", "veloc", "displ"]:
                setattr(ret, k, other - getattr(self, k))
        return ret

    def __add__(self, other):
        ret = copy(self)
        if isinstance(other, QuakeComponent):
            for k in ["accel", "veloc", "displ"]:
                setattr(ret, k, getattr(other, k) + getattr(self, k))

        elif isinstance(other, (float, int)):
            for k in ["accel", "veloc", "displ"]:
                setattr(ret, k, other + getattr(self, k))
        return ret

    def __mul__(self, other):
        ret = copy(self)
        if isinstance(other, QuakeComponent):
            for k in ["accel", "veloc", "displ"]:
                setattr(ret, k, getattr(other, k) * getattr(self, k))
        elif isinstance(other, (float, int)):
            for k in ["accel", "veloc", "displ"]:
                setattr(ret, k,  other * getattr(self, k))
        return ret
    
    def __rsub__(self, other):
        return self.__sub__(other)
    
    def __radd__(self, other):
        return self.__add__(other)

    def __rmul__(self, other):
        return self.__mul__(other)


class QuakeSeries(dict):
    def _update_metadata(f):
        def wrapped(*args, **kwds):
            res = f(*args, **kwds)
            res._refresh()
            return res
        return wrapped

    def __init__(self, input_array, meta=None):
        self._data = np.asarray(input_array)
        assert len(self.data.shape) == 1
        self.update(meta if meta is not None else {})

    def _refresh(self):
        self["peak_value"] = max(self._data, key=abs)

    @property
    def data(self):
        return self._data

    def __repr__(self):
        return f"QuakeSeries({self['units']})" #{dict.__repr__(self)})"
    
    def serialize(
        self, key=None, summarize=False, serialize_data=True, humanize_keys=False
    ):

        attributes = {
            #".".join((key, k)): v for k,v in self.items() if k[0] != "_"
            k: v for k,v in self.items() if k[0] != "_"
        }
        if serialize_data and not summarize:
            attributes.update({"data": list(self.data)})
        return attributes

    @_update_metadata
    def __pow__(self, other):
        ret = copy(self)
        ret._data = ret.data**other
        return ret

    @_update_metadata
    def __sub__(self, other):
        ret = copy(self)
        if isinstance(other, QuakeSeries):
            ret._data = other.data - self.data

        elif isinstance(other, (float, int)):
            ret._data = other - self.data
        return ret

    @_update_metadata
    def __add__(self, other):
        ret = copy(self)
        if isinstance(other, QuakeSeries):
            ret._data += other.data

        elif isinstance(other, (float, int)):
            ret._data += other
        return ret
    
    @_update_metadata
    def __mul__(self, other):
        if isinstance(other, (float, int)):
            ret = copy(self)
            ret._data *= other
        else:
            raise TypeError()
        return ret
    
    def __rsub__(self, other):
        return self.__sub__(other)
    
    def __radd__(self, other):
        return self.__add__(other)

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def plot(self, ax=None, fig=None):
        import matplotlib.pyplot as plt

        if ax is None:
            fig, ax = plt.subplots()
        ax.plot(self.data)



def rotate(data, angle):
    output = copy(data)
    if isinstance(data, QuakeComponent):
        raise Exception("Unable to rotate single component")

    elif isinstance(data, QuakeCollection):
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
    if isinstance(data, QuakeComponent):
        for k in data:
            if k in schema and "units" not in k:
                output[schema[k]["title"]] = output.pop(k)
            else:
                pass

    elif isinstance(data, QuakeCollection):
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
