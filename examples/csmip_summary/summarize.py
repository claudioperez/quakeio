# Claudio Perez
"""
This script generates a text summary of a given CSMIP zip file.

The variables `ground_channels` and `bridge_channels` must be changed
in order to use this script with different bridges.

Installation
============
This script depends on external libraries which may be installed by
running the following commands from any standard command line shell
(e.g. Bash on Linux, Powershell on Windows)

>> python -m pip install --upgrade pip

>> python -m pip install --upgrade quakeio


Using the Script
================
This script can be invoked from any modern command line shell as 
follows:

>> python Path_to_this_file Path_to_data.zip > Summary.txt


For example, if the contents of the current working directory
is the following:
.
├── 58658_003_20210628_18.29.26.P.zip
└── summarize.py


Then the script would be invoked as follows to create a summary
named `Summary.txt` in the same directory.

>> python summarize.py 58658_003_20210628_18.29.26.P.zip > Summary.txt

"""

# standard library imports; these are installed by default
import re
import sys
from pathlib import Path
from functools import cmp_to_key
from collections import defaultdict

# depencencies
import yaml
import numpy as np

import quakeio

ground_channels = [1, 2, 3, 6, 7, 17, 18, 24, 25]
bridge_channels = [11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23]


class YamlDumper(yaml.SafeDumper):
    # This class handles formatting of some datatypes
    # when generating YAML output
    def write_line_break(self,data=None):
        super().write_line_break(data)
        if len(self.indents) == 1:
            super().write_line_break()

    def process_tag(self, *args, **kwds):
        pass

def float_representer(dumper, value):
    # This function causes floating point numbers to be 
    # printed with a uniform width in YAML output
    return dumper.represent_scalar("tag:yaml.org,2002:float", f"{value:10.4f}")

YamlDumper.add_representer(float, float_representer)

# Some simple utility functions
dump_yaml = lambda x: yaml.dump(x, Dumper=YamlDumper,sort_keys=False)
align = lambda strng: strng.ljust(30,".")


def consolidate_records(data):
    g = 9.80665 # m/s^2
    summary = defaultdict(dict)
    for loc, record in data.items():
        for component in record.values():
            del component["instr_period"]
            del component["instr_period.units"]
            del component["peak_accel.units"]
            del component["peak_veloc.units"]
            del component["peak_displ.units"]
            del component["init_veloc.units"]
            del component["init_displ.units"]
            del component["filter.bandpass.point.units"]
            del component["filter.bandpass.limit.units"]
            del component["station.channel"]
            del component["channel"]
            component["peak_accel"] *= 1/(g*100)
            chan          = component.pop("file_name").split(".")[0]
            station_no    = component.pop("station.no")
            station_coord = component.pop("station.coord")
            filter_low    = component.pop("filter.bandpass.limit_low")
            filter_high   = component.pop("filter.bandpass.limit_high")
            filter_point  = component.pop("filter.bandpass.point")
            time_step     = component.accel.time_step
            loc  = component.pop("location") 
            comp = component.pop("component")
            chan = str(int(chan[4:]))
            summary[loc][comp+f" (Chan {chan})"] = \
                    component.serialize(
                            ljust=35, 
                            serialize_series=False,
                            humanize_keys=True, 
                            summarize=True
                    )
        summary[loc]["chan"] = chan
    
    station_data = {
        align("Station Number"): station_no,
        align("Station Coordinates"): station_coord,
        #align("Filter bandwidth"): filter_point,
        align("Filter low cut"): filter_low,
        align("Filter high cut"): filter_high,
        align("Record time step, dt"): time_step
    }
    return station_data, dict(summary)


def update_peaks(peaks, record):
    """
    Helper function which updates peaks in `peak` with
    values from `record`
    """
    for attr in ["peak_accel", "peak_veloc", "peak_displ"]:
        peaks[attr] = max(record[attr], peaks[attr], key=abs)

def extract_peaks(data, bridge_channels, ground_channels):
    # create a data structure whose default field is another data
    # structure whose default field is zero
    bridge_records = defaultdict(lambda: defaultdict(lambda: 0.0))
    ground_records = defaultdict(lambda: defaultdict(lambda: 0.0))

    for name, location in data.items():
        for dirn, record in location.items():
            channel = int(record["file_name"].split(".")[0][4:])
            if channel in bridge_channels:
                update_peaks(bridge_records[dirn], record)
            else:
                update_peaks(ground_records[dirn], record)

    return bridge_records, ground_records

def summarize(file_name, station, brdg, grnd, records):
    g = 9.80665 # m/s^2
    return f"""
# Summary for event file `{Path(file_name).name}`

```yml
{yaml.dump(station, sort_keys=False)}
```

## Bridge Channel Peaks

----------------------------------------------------------
Component         Acceleration\    Velocity   Displacement  
                              g        cm/s             cm        
--------------- --------------- ----------- -------------- 
Longitudinal     {1/(g*100)*brdg["long"]["peak_accel"]:14.4f} {brdg["long"]["peak_veloc"]:11.4f} {brdg["long"]["peak_displ"]:14.4f} 

Transverse       {1/(g*100)*brdg["tran"]["peak_accel"]:14.4f} {brdg["tran"]["peak_veloc"]:11.4f} {brdg["tran"]["peak_displ"]:14.4f} 

Vertical         {1/(g*100)*brdg["up"]["peak_accel"]:14.4f} {brdg["up"]["peak_veloc"]:11.4f} {brdg["up"]["peak_displ"]:14.4f} 
----------------------------------------------------------


## Site Channel Peaks

----------------------------------------------------------
Component         Acceleration\    Velocity   Displacement  
                              g        cm/s             cm        
--------------- --------------- ----------- -------------- 
Longitudinal     {1/(g*100)*grnd["long"]["peak_accel"]:14.4f} {grnd["long"]["peak_veloc"]:11.4f} {grnd["long"]["peak_displ"]:14.4f} 

Transverse       {1/(g*100)*grnd["tran"]["peak_accel"]:14.4f} {grnd["tran"]["peak_veloc"]:11.4f} {grnd["tran"]["peak_displ"]:14.4f} 

Vertical         {1/(g*100)*grnd["up"]["peak_accel"]:14.4f} {grnd["up"]["peak_veloc"]:11.4f} {grnd["up"]["peak_displ"]:14.4f} 
----------------------------------------------------------



## Records

```yml
{dump_yaml(records)}
```

"""

if __name__ == "__main__":
    # These are the procedures that are run when this file 
    # is invoked as a script from the command line.
    if len(sys.argv) == 2:
        file_name = sys.argv[-1]
    else:
        print("usage: python summarize.py ZIP_FILE")
        sys.exit()

    event = quakeio.read(file_name, "csmip.zip", summarize=True)
    brdg, grnd = extract_peaks(event, bridge_channels, ground_channels)
    station, records = consolidate_records(event)

    # Sort records:
    sorted_records = dict(
        sorted(
            records.items(),
            key = lambda pair: int(pair[1].pop("chan")) not in ground_channels
        )
    )

    print(summarize(file_name, station, brdg, grnd, sorted_records))

