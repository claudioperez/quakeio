
#set col_a bent_4_north_column_grnd_level
#set col_b bent_4_south_column_grnd_level
#
#set motion_rotation [format "%s,%s" $col_a $col_b]
#puts $motion_rotation

set motion_file "../../dat/58658_007_20210426_10.09.54.P/chan001.v2"
set motion [exec quakeio $motion_file -t opensees]

puts $motion

