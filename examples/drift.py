#bent_4_north_column_top Claudio Perez
import numpy as np
import quakeio

inches_to_cm = 2.54

file_name = "./dat/58658_007_20210426_10.09.54.P.zip"
height = 47.0*12.0 * inches_to_cm

event = quakeio.read(file_name, "csmip.zip")

#--------------------------------

#col_1_top_x = event.get_component(file_name="chan020.v2")
#col_1_bot_x = event.get_component(file_name="chan018.v2")
#
#diff = col_1_top_x - col_1_bot_x
#
#max_displ = max(diff.displ, key=abs)
#
#print(max_displ/height)

#--------------------------------
top = event.at(key="bent_4_north_column_top")
bot = event.at(key="bent_4_north_column_grnd_level")

relative_resp = top - bot
print(relative_resp)
# relative_resp is a record with long,tran,vert series

print((top - bot).resultant().displ["peak_value"]/height)


