#bent_4_north_column_top Claudio Perez
import numpy as np
import quakeio
import quakeio.utils.processing as proc

inches_to_cm = 2.54

file_name = "./dat/58658_007_20210426_10.09.54.P.zip"
height = 47.0*12.0 * inches_to_cm

event = quakeio.read(file_name, "csmip.zip")

top = event.at(key="bent_4_north_column_top")
bot = event.at(key="bent_4_north_column_grnd_level")

series = bot.long.accel
sa = proc.respspec(series["time_step"], 0.0, np.arange(0.02, 1.0, 0.01), series.data)

