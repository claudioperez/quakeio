import numpy as np

import quakeio

def test_mul():
    from .test_csmip import test_read_event
    event = test_read_event()


    pass

def test_rotate():
    # pick an arbitrary time
    time = 23
    angle = 21/7/3
    rotation = np.array([
        [ np.cos(angle), np.sin(angle)],
        [-np.sin(angle), np.cos(angle)]
    ])

    # read event
    from .test_csmip import test_read_event
    event = test_read_event()
    assert type(event) == quakeio.core.GroundMotionEvent

    rec = event["bent_4_north_column_grnd_level"]
    assert type(rec) == quakeio.core.GroundMotionRecord


    a_long, a_tran = rec["long"].accel[time], rec["tran"].accel[time]
    
    # Apply rotation to record
    rec.rotate(angle) 
    A_long_rot, A_tran_rot = rec["long"].accel, rec["tran"].accel

    # Ensure that rotation does not alter object types
    assert type(A_long_rot) == quakeio.core.GroundMotionSeries
    assert type(A_tran_rot) == quakeio.core.GroundMotionSeries

    # manually calculate values 
    a_calc_long, a_calc_tran = rotation @ np.array([[a_long],[a_tran]])

    # Assert rotation matches manual calc
    assert np.isclose(float(A_long_rot[time]), float(a_calc_long))
    assert np.isclose(float(A_tran_rot[time]), float(a_calc_tran))


