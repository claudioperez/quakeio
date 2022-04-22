import json
from copy import copy
from pathlib import Path

from quakeio.core import QuakeComponent, QuakeCollection
from quakeio.utils.parseutils import open_quake


class Unused:
    pass

class QuakeEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "tolist"):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def read_json(read_file, **kwds: Unused):

    return json.load(read_file)


def record2vega(ground_motion, dump_json=True, **kwds):
    output = {
      "$schema": "https://vega.github.io/schema/vega/v5.json",
      "description": "A basic line chart example.",
      "width": 450,
      "height": 250,
      "padding": 5,

      "signals": [
        {
          "name": "interpolate",
          "value": "linear",
          "bind": {
            "input": "select",
            "options": [
              "basis",
              "cardinal",
              "catmull-rom",
              "linear",
              "monotone",
              "natural",
              "step",
              "step-after",
              "step-before"
            ]
          }
        }
      ],

      "scales": [
        {
          "name": "x",
          #"type": "point",
          "range": "width",
          "domain": {"data": "table", "field": "x"}
        },
        {
          "name": "y",
          "type": "linear",
          "range": "height",
          "nice": True,
          "zero": True,
          "domain": {"data": "table", "field": "y"}
        },
        {
          "name": "color",
          "type": "ordinal",
          "range": "category20",
          #"range": "linear",
          "domain": {"data": "table", "field": "c"}
        }
      ],

      "axes": [{"orient": "bottom", "scale": "x"}, {"orient": "left", "scale": "y"}],

      "marks": [
        {
          "type": "group",
          "from": {
            "facet": {"name": "series", "data": "table", "groupby": "c"}
          },
          "marks": [
            {
              "type": "line",
              "from": {"data": "series"},
              "encode": {
                "enter": {
                  "x": {"scale": "x", "field": "x"},
                  "y": {"scale": "y", "field": "y"},
                  "stroke": {"scale": "color", "field": "c"},
                  "strokeWidth": {"value": 2}
                },
                "update": {
                  "interpolate": {"signal": "interpolate"},
                  "strokeOpacity": {"value": 1}
                },
                "hover": {"strokeOpacity": {"value": 0.5}}
              }
            }
          ]
        }
      ]
    }
    #ground_motion = ground_motion.serialize(serialize_data=not summarize)
    dt = ground_motion.accel.time_step
    output.update({
      "data": [
        {
          "name": "table",
          "values": [
              {"x": i*dt, "y": y, "c": 0} for i, y in enumerate(ground_motion.accel)
          ]
        }
      ]
    })
    with open("aaa.json","w+") as f:
        json.dump(output,f,indent=2)
    return output

def write_json(write_file, ground_motion, indent=4, summarize=False, **kwds):
    pass

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
    "vega.json": {"read": read_json, "write": write_json},
    "vega.yaml": {"read": read_yaml, "write": write_yaml}
}
