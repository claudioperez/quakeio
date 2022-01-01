# Claudio Perez
import sys

import numpy as np

import quakeio

if __name__ == "__main__":
    file_name = sys.argv[-1]


    event = quakeio.read(file_name, "csmip.zip")

    angle = 26.16

    # col_a: chan017, chan018
    col_a = event["bent_4_north_column_grnd_level"].rotate(angle)

    # col_b: chan017, chan018
    col_b = event["bent_4_south_column_grnd_level"].rotate(angle)

    print(col_b["long"].accel)

    avg = lambda dirn: (col_a[dirn] + col_b[dirn])*0.5
    long, tran = map(avg, ["long", "tran"])

    print(long.accel)
    quakeio.write(sys.stdout, long, "opensees")


