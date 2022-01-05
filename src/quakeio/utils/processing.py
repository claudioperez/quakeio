# Claudio Perez
# 2021

import numpy as np
import scipy.integrate


def get_time_step(series, time_series=None, time_step: float = None) -> float:
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


def get_time_series(series, time_series, time_step):
    """
    If both `time_series` and `time_step` are None,
    `series` is checked for a `time_series` or `time_step` attribute.
    """
    if time_series:
        return time_series
    elif time_step:
        return np.cumsum([time_step] * len(series))
    else:
        if hasattr(series, "time_series"):
            return series.time_series
        elif hasattr(series, "time_step"):
            return np.cumsum([series.time_step] * len(series))
        else:
            msg = "Unable to deduce time series"
            raise TypeError(msg)


def rotate_series_in_place(series, sn=None, cs=None):
    series *= np.sin(sn or (np.pi / 2 * cs))


def arias_intensity(
    series, start_level=0.0, end_level=1.0, time_series=None, time_step=None
):
    time = get_time_series(series, time_series, time_step)
    arias_factor = np.pi / 2.0
    husid = integrate_husid(series, time)
    # Normalize
    husid_norm = husid / husid[-1]
    idx = np.where(np.logical_and(husid_norm >= start_level, husid_norm <= end_level))[
        0
    ]
    if len(idx) < len(series):
        husid = integrate_husid(series[idx], time)

    raise NotImplementedError("Not implemented")
    return arias_factor * husid[-1]


def integrate_husid(series, time_series=None, time_step=None):
    time = get_time_series(series, time_series, time_step)
    return scipy.integrate.cumtrapz(series ** 2.0, time)

