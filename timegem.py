from starbox.starstuff.celestial import u,c
import numpy as np
import math
"""
The Time Gem module slots into everything else in the StarBox and provides a single instance of a single class, which can be added to anything in the universe to let it power everything.

Potential adverse effects of this remain to be seen.
"""

class Clock:
    bodyType = "Quantum Coalescence"
    # Something thematic but exotic, so if it ever shows up, a dev/maintainer can tell something is not right, but an end user might not

    def __init__(self, time=0):
        self.TIME = time * 60 * u.minute

    def update(self, obj):
        """This method needs to be very flexible and adaptable...We shall see how that goes"""
        try:
            try:
                for o2 in obj.orbitals:
                    try:
                        self.update(o2)
                        #o2.Clock = self
                    except:
                        pass
            except:
                pass
            try:
                if obj.Clock != self:
                    obj.Clock = self
            except:
                pass
            yr = obj.lengthOrbit
            timeIntoYear = np.mod(self.TIME.to(u.hour),yr)
            phiNew = (-timeIntoYear/yr)*math.tau * u.rad
            obj.posPhi = phiNew
        except:
            pass

    def tick(self, inc):
        fmt = type(inc)
        if fmt == u.Quantity:
            self.TIME = self.TIME + inc
        elif fmt == int or fmt == float:
            self.TIME = self.TIME + inc*u.minute

    def toaster(self, plus=0*u.minute):
        t = self.TIME + plus
        t0 = f"{int(t.to(u.hour).value)}:{int(np.mod(t.value,60))}"
        if t0[-2] == ":":
            t0 = t0 + "0"
        t1 = t0.zfill(8)
        t2 = t1[0:-7] + "." + t1[-7:]
        return t2

    def __str__(self):
        return self.toaster()
