import numpy as np
import quakeio
import quakeio.utils.processing as proc

inches_to_cm = 2.54

file_name = "./dat/58658_007_20210426_10.09.54.P.zip"

collection = quakeio.read(file_name, "csmip.zip")

collection.transfer_function((
    "bent_4_north_column_top", "bent_4_north_column_grnd_level"
))


top = collection.at(key="bent_4_north_column_top")
bot = collection.at(key="bent_4_north_column_grnd_level")

proc.transfer_function((top,bot)).plot()

