import numpy as np
from quakeio.core import QuakeComponent, QuakeSeries

class ResponseSpectrum:
    def __init__(self, *args, motion=None, **kwds):
        self.motions = [motion]

    def accel(self):
        pass

    def time(self):
        pass

    def plot(self):
        pass

def transfer_function(pairs, *args, **kwds):
    s1,s2 = spectrum(pairs[0], **kwds), spectrum(pairs[1], **kwds)
    t = s2/s1
    t[0,:] = s1[0,:]
    return t

def spectrum(*args, **kwds):
    return _accel_spectrum(*args, **kwds)

def _accel_spectrum(accel,dt=None,damping=0.0,per=None,gama=1/2,beta=1/4):
    from scipy.interpolate import interp1d
    from numpy import pi
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
    
    numper=len(per)
    m = 1.0
    numdata=len(accel)
    t=np.arange(0,(numdata)*dt,dt)
    
    u0,v0 = 0.0, 0.0
    SA = np.zeros((1+len(damping),numper))

    for i in range(numper):
        for j,dmp in enumerate(damping):
            if dt/per[i]>0.02:
                dtp=per[i]*0.02;
                dtpx=np.arange(0,max(t),dtp)
                dtpx=dtpx
                accfrni=interp1d(t, accel)(dtpx);
                accfrn=accfrni[1:len(accfrni)-1];
                numdatan=len(accfrn);
                p=-m*accfrn;
            else:
                dtp=dt;
                accfrn = accel;
                p = -m*accfrn;
                numdatan=numdata;

            u = np.zeros((numdatan))
            v = np.zeros((numdatan))
            a = np.zeros((numdatan))

            k = 4*pi**2*m/per[i]**2;
            c = 2*dmp*np.sqrt(k*m);
            kstar = k + gama*c/(beta*dtp) + m/(beta*dtp**2.0)
            acons = m/(beta*dtp) + gama*c/beta
            bcons = m/(2*beta) + dtp*(gama/(2*beta)-1)*c
            u[0] = u0;
            v[0] = v0;
            a[0] = (p[0]-c*v[0]-k*u[0])/m;
            for j in range(1,numdatan):
                deltap=p[j]-p[j-1];
                deltaph=deltap+acons*v[j-1]+bcons*a[j-1];
                deltau=deltaph/kstar;
                deltav=gama*deltau/(beta*dtp)-gama*v[j-1]/beta+dtp*(1-gama/(2*beta))*a[j-1];
                deltaa=deltau/(beta*dtp**2)-v[j-1]/(beta*dtp)-a[j-1]/(2*beta);
                u[j]=u[j-1] + deltau;
                v[j]=v[j-1] + deltav;
                a[j]=a[j-1] + deltaa;
            atot=a+accfrn;
            SA[0,i]=per[i]
            SA[1+j,i]=abs(max(atot, key=abs));
    return SA

