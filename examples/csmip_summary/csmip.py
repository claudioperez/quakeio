# Claudio Perez

import sys
from collections import defaultdict

import yaml
import numpy as np

import quakeio

def consolidate_records(data):
    #summary = defaultdict(lambda: defaultdict(dict))
    summary = defaultdict(dict)
    for loc, record in data.items():
        for component in record.values():
            del component["file_name"]
            del component["instr_period"]
            del component["instr_period.units"]
            del component["peak_accel.units"]
            del component["peak_veloc.units"]
            del component["peak_displ.units"]
            del component["init_veloc.units"]
            del component["init_displ.units"]
            del component["filter.bandpass.point.units"]
            del component["filter.bandpass.limit.units"]
            chan          = component.pop("channel")
            station_chan  = component.pop("station.channel")
            chan = station_chan if station_chan else chan
            station_no    = component.pop("station.no")
            station_coord = component.pop("station.coord")
            filter_low    = component.pop("filter.bandpass.limit_low")
            filter_high   = component.pop("filter.bandpass.limit_high")
            filter_point  = component.pop("filter.bandpass.point")
            loc  = component.pop("location") 
            comp = component.pop("component")
            summary[loc][comp+f" (Chan {chan})"] = \
                    component.serialize(
                            ljust=35, 
                            serialize_series=False,
                            humanize_keys=True, 
                            summarize=True
                    )

    station_data = {}
    station_data["Station Number"] = station_no
    station_data["Station Coordinates"] = station_coord
    station_data["Filter point"] = filter_point
    station_data["Filter low cut"] = filter_low
    station_data["Filter high cut"] = filter_high
    return f"""
{yaml.dump(station_data)}

## Records

```yaml
{yaml.dump(dict(summary))}
```

"""


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
            # Not all .v2 files have a station channel
            if record["station.channel"]:
                if int(record["station.channel"]) in bridge_channels:
                    update_peaks(bridge_records[dirn], record)
                else:
                    update_peaks(ground_records[dirn], record)

            else:
                if int(record["channel"]) in bridge_channels:
                    update_peaks(bridge_records[dirn], record)
                else:
                    update_peaks(ground_records[dirn], record)

    return bridge_records, ground_records

def summary_B(file_name, brdg, grnd):
    g = 9.80665 # m/s^2
    return f"""
# Summary for event file `{file_name}`

## Bridge Channels

| Component    | Acceleration | Velocity  | Displacement |
|              |      g       |   cm/s    |     cm       |
|--------------|--------------|-----------|--------------|
| Longitudinal | {1/(g*100)*brdg["long"]["peak_accel"]:12.4f} | {brdg["long"]["peak_veloc"]:9.4f} | {brdg["long"]["peak_displ"]:12.4f} |
| Transverse   | {1/(g*100)*brdg["tran"]["peak_accel"]:12.4f} | {brdg["tran"]["peak_veloc"]:9.4f} | {brdg["tran"]["peak_displ"]:12.4f} |
| Vertical     | {1/(g*100)*brdg["up"]["peak_accel"]:12.4f} | {brdg["up"]["peak_veloc"]:9.4f} | {brdg["up"]["peak_displ"]:12.4f} |

## Site Channels

| Component    | Acceleration | Velocity  | Displacement |
|              |      g       |   cm/s    |     cm       |
|--------------|--------------|-----------|--------------|
| Longitudinal | {1/(g*100)*grnd["long"]["peak_accel"]:12.4f} | {grnd["long"]["peak_veloc"]:9.4f} | {grnd["long"]["peak_displ"]:12.4f} |
| Transverse   | {1/(g*100)*grnd["tran"]["peak_accel"]:12.4f} | {grnd["tran"]["peak_veloc"]:9.4f} | {grnd["tran"]["peak_displ"]:12.4f} |
| Vertical     | {1/(g*100)*grnd["up"]["peak_accel"]:12.4f} | {grnd["up"]["peak_veloc"]:9.4f} | {grnd["up"]["peak_displ"]:12.4f} |

"""

if __name__ == "__main__":
    # These are the procedures that are run 
    # when this file is invoked as a script
    if len(sys.argv) > 2:
        file_name = sys.argv[-1]
    else:
        file_name = "58658_007_20210426_10.09.54.P.zip"
    ground_channels = [1, 2, 3, 6, 7, 17, 18, 24, 25],
    bridge_channels = [11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23]

    event = quakeio.read(file_name, "csmip.zip", summarize=True)
    brdg, grnd = extract_peaks(event, bridge_channels, ground_channels)

    print(summary_B(file_name, brdg, grnd))
    print(consolidate_records(event))

