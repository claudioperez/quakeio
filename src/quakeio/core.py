import re
from pathlib import Path


import numpy as np


class RealNumber(float):
    def __new__(cls, value, units=None):
        return float.__init__(cls, value)

    def __init__(self, value, units=None, time=None):
        self.units = units


class GroundMotionEvent(dict):
    """
    Container of GroundMotionRecord objects
    """

    def __init__(self, key, *args, event_date=None, **kwds):
        dict.__init__(self, **{record[key]: record for record in args})
        self.event_date = event_date

    def serialize(self) -> None:
        for record in self.values():
            record.serialize()


class GroundMotionRecord(dict):
    def __init__(self, accel, veloc, displ, meta={}):
        self.accel = accel
        self.displ = displ
        self.veloc = veloc
        dict.__init__(self, **meta)

    def serialize(self) -> None:
        self["accel"] = self.accel
        self["veloc"] = self.veloc
        self["displ"] = self.displ


class GroundMotionSeries(np.ndarray):
    def __new__(cls, input_array, metadata={}):
        obj = np.asarray(input_array).view(cls)
        for k,v in metadata.items():
            if not hasattr(obj,k):
                setattr(obj,k,v)
        return obj

    def __array_finalize__(self, obj):
        for k,v in self.__dict__.items():
            setattr(obj,k,v)

    def plot(self, ax=None, fig=None):
        import matplotlib.pyplot as plt

        if ax is None:
            fig, ax = plt.subplots()
        ax.plot(self)
