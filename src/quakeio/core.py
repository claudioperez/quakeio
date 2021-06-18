# Claudio Perez
# 2021
import numpy as np


#class RealNumber(float):
#    def __new__(cls, value, units=None):
#        return float.__init__(cls, value)
#
#    def __init__(self, value, units=None, time=None):
#        self.units = units

class GroundMotionParser:
    pass

class GroundMotionEvent(dict):
    """
    Container of GroundMotionRecord objects
    """

    def __init__(self, key, records, event_date=None, **kwds):
        dict.__init__(self, **{record[key]: record for record in records})
        #self.update({
        #    "event_accel_peak": max([r["accel_peak"] for r in self.values()])
        #})
        self.event_date = event_date

    def serialize(self, serialize_data=True) -> dict:
        return {k: v.serialize() for k,v in self.items()}

class GroundMotionRecord(dict):
    def __init__(self, accel, veloc, displ, meta={}):
        self.accel = accel
        self.displ = displ
        self.veloc = veloc
        dict.__init__(self, **meta)

    def serialize(self, serialize_data=True) -> dict:
        ret = dict(self)
        ret.update({
            **self.accel.serialize("accel", serialize_data=serialize_data),
            **self.veloc.serialize("veloc", serialize_data=serialize_data),
            **self.displ.serialize("displ", serialize_data=serialize_data)
        })
        return ret
        

class GroundMotionSeries(np.ndarray):
    def __new__(cls, input_array, metadata={}):
        obj = np.asarray(input_array).view(cls)

        for k, v in metadata.items():
            if not hasattr(obj, k):
                setattr(obj, k, v)
        return obj

    def serialize(self,key=None,serialize_data=True):
        if key is None:
            key = self.series_type
        attributes =  {
            ".".join((key, k)): v
                for k,v in self.__dict__.items() if k[0] != "_"
        }
        if serialize_data:
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

