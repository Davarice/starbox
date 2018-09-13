from starbox.starstuff.celestial import u,c
"""
The Time Gem module slots into everything else in the StarBox and provides a single instance of a single class, which can be added to anything in the universe to let it power everything.

Potential adverse effects of this remain to be seen.
"""

class Clock:
    bodyType = "Quantum Coalescence"
    # Something thematic but exotic, so if it ever shows up, a dev/maintainer can tell something is not right, but an end user might not

    def __init__(self, time=0):
        self.TIME = time * u.hour

    def update(self, obj):
        """This method needs to be very flexible and adaptable...We shall see how that goes"""
        rho = obj.PosRho

    def tick(self, inc):
        fmt = type(inc)
        if fmt == u.Quantity:
            self.TIME = self.TIME + inc
        elif fmt == int or fmt == float:
            self.TIME = self.TIME + inc*u.hour