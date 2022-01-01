import quakeio

csmip_event = quakeio.read("event.zip")
csmip_event["channel-01"].accel.plot()

csmip_event["chan001"].plot()

csmip_event["chan001"].plot_spect()


