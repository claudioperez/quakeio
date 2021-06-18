from collections import defaultdict
import numpy as np
import quakeio


def update_peaks(peaks, record):
    for attr in ["peak_accel", "peak_veloc", "peak_displ"]:
        peaks[attr] = max(record[attr], peaks[attr], key=abs)

def summarize(file_name, bridge_channels, ground_channels):
    data = quakeio.read(file_name, "csmip.zip", summarize=True)

    bridge_records = defaultdict(lambda: defaultdict(lambda: 0))
    ground_records = defaultdict(lambda: defaultdict(lambda: 0))

    for name, components in data.items():
        for dirn, record in components.items():
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

def gen_summary(file_name, brdg, site): 
    return f"""
# Summary for event file `{file_name}`

## Bridge Channels

| Component    | Acceleration | Velocity  | Displacement |
|--------------|--------------|-----------|--------------|
| Longitudinal | {brdg["long"]["peak_accel"]:12.4f} | {brdg["long"]["peak_veloc"]:9.4f} | {brdg["long"]["peak_displ"]:12.4f} |
| Transverse   | {brdg["tran"]["peak_accel"]:12.4f} | {brdg["tran"]["peak_veloc"]:9.4f} | {brdg["tran"]["peak_displ"]:12.4f} |
| Vertical     | {brdg["vert"]["peak_accel"]:12.4f} | {brdg["vert"]["peak_veloc"]:9.4f} | {brdg["vert"]["peak_displ"]:12.4f} |

## Site Channels

| Component    | Acceleration | Velocity  | Displacement |
|--------------|--------------|-----------|--------------|
| Longitudinal | {grnd["long"]["peak_accel"]:12.4f} | {grnd["long"]["peak_veloc"]:9.4f} | {grnd["long"]["peak_displ"]:12.4f} |
| Transverse   | {grnd["tran"]["peak_accel"]:12.4f} | {grnd["tran"]["peak_veloc"]:9.4f} | {grnd["tran"]["peak_displ"]:12.4f} |
| Vertical     | {grnd["vert"]["peak_accel"]:12.4f} | {grnd["vert"]["peak_veloc"]:9.4f} | {grnd["vert"]["peak_displ"]:12.4f} |

"""


if __name__ == "__main__":
    ground_channels = [1, 2, 3, 6, 7, 17, 18, 24, 25],
    bridge_channels = [11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23]

    file_name = "58658_007_20210426_10.09.54.P.zip"
    brdg, grnd = summarize(file_name, bridge_channels, ground_channels)

    print(gen_summary(file_name, brdg, grnd))

