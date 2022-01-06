try:
    import jax.numpy as jnp
except:
    import numpy as jnp

import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
from quakeio.core import QuakeComponent, QuakeSeries

def _plot_func(plot):
    plt.style.use("berkeley")

    def __call__(self, *args, **kwds):
        if "ax" in kwds:
            self.ax = kwds.pop("ax")
            self.fig = self.ax.figure
        else:
            self.fig, self.ax = plt.subplots()
            
        if "title" in kwds:
            self.ax.set_title(kwds.pop("title"))

        plot(self, *args, **kwds)
        return self.ax
    return __call__


class Spectrum:
    def __init__(self, accel, *args, **kwds):
        self._accel = accel
        self.kwds = kwds

    def accel(self):
        pass

    def time(self):
        pass

    def spect(self,accel=None,dt=None,damping=None,per=None,gamma=1/2,beta=1/4,interp=None):
        if interp is None:
            from scipy.interpolate import interp1d as interp
        if damping is None:
            damping = ("damping" in self.kwds and self.kwds.pop("damping")) or 0.0
        if isinstance(accel, QuakeComponent):
            dt = accel.accel["time_step"]
            accel = accel.accel.data
        elif isinstance(accel, QuakeSeries):
            dt = accel["time_step"]
            accel = accel.data
        if isinstance(damping, float):
            damping = [damping]

        if per is None:
            per = np.arange(0.02, 1.0, 0.01)

        return _accel_spectrum(
            accel=accel,
            dt=dt,
            per=per,
            gamma=gamma,
            beta=beta,
            damping=damping,
            interp=interp
        )
    

    @_plot_func
    def plot(self, **kwds):
        #sa = spectrum(self._accel, **kwds)
        tsa = self.spect(self._accel, **kwds)
        if len(tsa) > 2:
            for sa in tsa[1:]:
                self.ax.plot(tsa[0], sa)
        self.ax.set_title(self._accel["location_name"])


class TransferFunction:
    pass


def transfer_function(pairs, *args, **kwds):
    s1,s2 = spectrum(pairs[0], **kwds), spectrum(pairs[1], **kwds)
    t = s2/s1
    t[0,:] = s1[0,:]
    return t

def spectrum(*args, **kwds):
    return _accel_spectrum(*args, **kwds)

def _accel_spectrum(accel,dt,damping,per,gamma=1/2,beta=1/4,interp=None):
    numper=len(per)
    m = 1.0
    numdata=len(accel)
    t=np.arange(0,(numdata)*dt,dt)
    
    u0,v0 = 0.0, 0.0
    SA = np.zeros((1+len(damping),numper))
    SA[0,:] = per[:]

    for di,dmp in enumerate(damping):
        for i in range(numper):
            if dt/per[i]>0.02:
                dtp = per[i]*0.02
                dtpx = np.arange(0,max(t),dtp)
                dtpx = dtpx
                accfrni = interp(t, accel)(dtpx)
                accfrn = accfrni[1:len(accfrni)-1]
                numdatan = len(accfrn)
                p = -m*accfrn
            else:
                dtp=dt;
                accfrn = accel;
                p = -m*accfrn;
                numdatan=numdata;

            u = np.zeros((numdatan))
            v = np.zeros((numdatan))
            a = np.zeros((numdatan))

            k = 4*pi**2*m/per[i]**2;
            c = 2*dmp*np.sqrt(k/m);
            kstar = k + gamma*c/(beta*dtp) + m/(beta*dtp**2.0)
            acons = m/(beta*dtp) + gamma*c/beta
            bcons = m/(2*beta) + dtp*(gamma/(2*beta)-1)*c
            u[0] = u0
            v[0] = v0
            a[0] = (p[0]-c*v[0]-k*u[0])/m
            for j in range(1,numdatan):
                deltap = p[j]-p[j-1]
                deltaph = deltap+acons*v[j-1]+bcons*a[j-1]
                deltau = deltaph/kstar
                deltav = gamma*deltau/(beta*dtp)-gamma*v[j-1]/beta+dtp*(1-gamma/(2*beta))*a[j-1]
                deltaa = deltau/(beta*dtp**2)-v[j-1]/(beta*dtp)-a[j-1]/(2*beta)
                u[j] = u[j-1] + deltau
                v[j] = v[j-1] + deltav
                a[j] = a[j-1] + deltaa
            atot = a + accfrn
            SA[1+di,i] = abs(max(atot, key = abs));
    return SA

