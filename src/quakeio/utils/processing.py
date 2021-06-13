# Claudio Perez
# 2021

import numpy as np
import scipy.integrate


def _get_time_step(series, time_series, time_step: float) -> float:
    """
    If both `time_series` and `time_step` are None,
    `series` is checked for a `time_series` or `time_step` attribute.
    """
    if time_step:
        return time_step
    elif time_series:
        return np.diff(time_series) / len(time_series)
    else:
        if hasattr(series, "time_step"):
            return series.time_step
        elif hasattr(series, "time_series"):
            time = series.time_series
            return np.diff(time) / len(time)
        else:
            msg = "Unable to deduce time step"
            raise TypeError(msg)


def _get_time_series(series, time_series, time_step):
    """
    If both `time_series` and `time_step` are None,
    `series` is checked for a `time_series` or `time_step` attribute.
    """
    if time_series:
        return time_series
    elif time_step:
        return np.asarray([time_step] * len(series))
    else:
        if hasattr(series, "time_series"):
            return series.time_series
        elif hasattr(series, "time_step"):
            return np.asarray([series.time_step] * len(series))
        else:
            msg = "Unable to deduce time series"
            raise TypeError(msg)


def rotate_series_in_place(series, sn=None, cs=None):
    series *= np.sin(sn or (np.pi / 2 * cs))


def arias_intensity(series, time_series=None, time_step=None):
    time = _get_time_series(series, time_series, time_step)
    raise NotImplementedError("Not implemented")
    pass


def integrate_husid(series, time_series=None, time_step=None):
    time = _get_time_series(series, time_series, time_step)
    return scipy.integrate.cumtrapz(series ** 2.0, time)

