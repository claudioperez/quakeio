import quakeio

csmip_event = quakeio.read("dat/58658_007_20210426_10.09.54.P.zip")
record = csmip_event["bent_4_north_column_grnd_level"]
component = record["long"]
series = component.accel
series.plot()
#
#csmip_event["chan001"].plot()
#
#csmip_event["chan001"].plot_spect()


