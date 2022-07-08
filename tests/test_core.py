import numpy as np

import quakeio

def test_mul():
    from .test_csmip import test_read_event
    event = test_read_event()

def test_rotate():
    # pick an arbitrary time
    time = 23
    angle = 21/7/3
    rotation = np.array([
        [ np.cos(angle),-np.sin(angle)],
        [ np.sin(angle), np.cos(angle)]
    ])

    # read event
    from .test_csmip import test_read_event
    event = test_read_event()
    assert type(event) == quakeio.core.QuakeCollection

    mot = event.motions["bent_4_north_column_grnd_level"]
    assert type(mot) == quakeio.core.QuakeMotion


    a_long, a_tran = mot.long.accel.data[time], mot.tran.accel.data[time]
    
    # Apply rotation to record
    mot.rotate(angle) 
    A_long_rot, A_tran_rot = mot.long.accel, mot.tran.accel

    # Ensure that rotation does not alter object types
    assert type(A_long_rot) == quakeio.core.QuakeSeries
    assert type(A_tran_rot) == quakeio.core.QuakeSeries

    # manually calculate values 
    a_calc_long, a_calc_tran = rotation @ np.array([[a_long],[a_tran]])

    # Assert rotation matches manual calc
    assert np.isclose(float(A_long_rot.data[time]), float(a_calc_long))
    assert np.isclose(float(A_tran_rot.data[time]), float(a_calc_tran))


def test_rotate_displ():
    # pick an arbitrary time
    time = 23
    angle = 21/7/3
    rotation = np.array([
        [ np.cos(angle),-np.sin(angle)],
        [ np.sin(angle), np.cos(angle)]
    ])

    # read event
    from .test_csmip import test_read_event
    event = test_read_event()
    assert type(event) == quakeio.core.QuakeCollection

    mot = event.motions["bent_4_north_column_grnd_level"]
    assert type(mot) == quakeio.core.QuakeMotion


    a_long, a_tran = mot.long.displ.data[time], mot.tran.displ.data[time]
    
    # Apply rotation to record
    mot.rotate(angle) 
    D_long_rot, D_tran_rot = mot.long.displ, mot.tran.displ

    # Ensure that rotation does not alter object types
    assert type(D_long_rot) == quakeio.core.QuakeSeries
    assert type(D_tran_rot) == quakeio.core.QuakeSeries

    # manually calculate values 
    a_calc_long, a_calc_tran = rotation @ np.array([[a_long],[a_tran]])

    # Assert rotation matches manual calc
    assert np.isclose(float(D_long_rot.data[time]), float(a_calc_long))
    assert np.isclose(float(D_tran_rot.data[time]), float(a_calc_tran))

