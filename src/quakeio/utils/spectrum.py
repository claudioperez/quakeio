import numpy as np
from scipy.integrate import solve_ivp


import quakeio
from quakeio.utils.processing import get_time_series, get_time_step
from .newmark import linear_accel_vector,linear_accel_scalar

class ResponseHistory:
    def __init__(self, accel, time_series=None, time_step=None):
        if isinstance(accel, (quakeio.core.GroundMotionSeries, np.ndarray)):
            self.accel = accel
        else:
            # a Ground motion record was supplied
            self.accel = accel.accel

        self.time_series = get_time_series(self.accel, time_series, time_step)
    
    def __call__(self, period, damping=1.0, R=1.0):
        #g = 386.4
        g = 9.80665*100.
        accel = self.accel
        omega = (2*np.pi)/period
        time = self.time_series
        t_span = (time[0], time[-1])
        u0 = (0.0, 0.0)

        def EOM(t, y):
            i = np.argmin(np.abs(time - t))
            D, dDdt = y
            dydt = [dDdt, -accel[i]*g-omega**2*D-2*damping*omega*dDdt]
            return dydt

        rtol = atol = 1e-8
        sol = solve_ivp(EOM, y0=u0, t_span=t_span, rtol=rtol, atol=atol)
        D = sol.y[0,:]
        t = sol.t
        return t, D

def response_spectrum(accel, periods=None, time_step=None, damping=1.0):
    import elle.transient
    import anabel, jax
    if periods is None:
        periods = np.linspace(0.1,5,100)
    mass = 1.0
    spect = []
    for period in periods: 
        k = (2.0*np.pi/period*np.sqrt(mass))**2
        integrator = linear_accel_scalar(
            df = k,
            dt = get_time_step(accel, time_step=time_step),
            mass = mass,
            damp = damping*2*np.sqrt(mass*k)
        )
        u_max = 0.0
        _, u, state = integrator.origin
        for a in accel:
            newstate, u = integrator(state, a)
            u_max = abs(u) if abs(u) > u_max else u_max
        spect.append(u_max)
    return np.array(spect).flatten()

 
