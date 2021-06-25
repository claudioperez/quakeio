# Claudio Perez
import sys

import numpy as np

import quakeio

inches_to_cm = 2.54

if __name__ == "__main__":
    file_name = sys.argv[-1]
    height = 84.0 * inches_to_cm


    event = quakeio.read(file_name, "csmip.zip")

    #--------------------------------
    col_1_top = event.get(file_name="chan020.v2")
    col_1_bot = event.get(file_name="chan018.v2")

    diff = col_1_top - col_1_bot

    max_displ = max(diff.displ, key=abs)

    print(max_displ/height)

    #--------------------------------
    top = event["bent_4_north_column_top"]
    bot = event["bent_4_north_column_grnd_level"]

    print(max((top - bot).norm().displ, key=abs)/height)


