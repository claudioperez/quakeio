from pathlib import Path

import quakeio

csmip_archive = Path("dat/58658_007_20210426_10.09.54.P.zip")
csmip_dir = Path("dat/58658_007_20210426_10.09.54.P/")

#----------------------------------------------------------------------
# Record (.v2)
#----------------------------------------------------------------------
def test_read_event():
    return quakeio.csmip.read_event(csmip_archive)

def test_unique():
    event = test_read_event()
    all_records = [r for g in event.values() for r in g.values()]
    assert len(all_records) == 20

#----------------------------------------------------------------------
# Record (.v2)
#----------------------------------------------------------------------
def test_2():
    csmip_record = quakeio.csmip.read_record(csmip_dir / "chan001.v2")
    quakeio.write("-", csmip_record, "json")


def test_read():
    csmip_record = quakeio.read(csmip_dir / "chan001.v2")
    quakeio.write("-", csmip_record, "yaml", summarize=True)
    return csmip_record


def test_peak():
    csmip_record = test_read()
    assert csmip_record["peak_accel"] == 17.433
    assert csmip_record["peak_veloc"] == 0.205
    assert csmip_record["peak_displ"] == -0.004


def test_peak_time():
    csmip_record = test_read()
    assert csmip_record["peak_accel.time"] == 20.270
    assert csmip_record["peak_veloc.time"] == 20.290
    assert csmip_record["peak_displ.time"] == 20.270

def test_accel_data():
    csmip_record = test_read()
    assert csmip_record.accel[0]  == -0.000102
    assert csmip_record.accel[-1] ==  0.000105

def test_veloc_data():
    csmip_record = test_read()
    assert csmip_record.veloc[0]  == 0.0000950
    assert csmip_record.veloc[-1] == 0.0001009



# csmip_record = quakeio.GroundMotionComponent(csmip_dir/"chan001.v2")

# csmip_record.peak_accel

# csmip_record.plot_accel
