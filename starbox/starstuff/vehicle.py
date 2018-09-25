#print("    Loading Vehicles...", end='')
import collections
from .celestial import u,c
import numpy as np

"""
### TODO ###
Stub module for VEHICLE classes
"""

class Hyperdrive:
    def __init__(self,freq=63288,mrange=30,gran=3,draw=10,effPeak=80,effFall=0.1,tolerance=30):
        self.freq=freq*u.Hz # The frequency of oscillation at which the hyperdrive is at its Efficiency Peak
        self.mrange=mrange*u.lyr # The maximum distance a given hyperdrive is capable of covering on a single charge
        self.gran=gran # A measure of precision; how many significant digits can be applied to the frequency setting
        self.draw=(draw*u.W)/(u.Hz*u.tonne) # Power draw, in Watts, per Hertz-Ton
        self.effPeak=effPeak/100 # The maximum energy efficiency the hyperdrive can attain
        self.effFall=effFall/100 # The percentage deducted from the Peak Efficiency for each Hz difference between frequency and Ideal Frequency
        self.tolerance=tolerance*(u.au/u.solMass2015) # The maximum distance from a massive body at which the hyperdrive can arrive, and the minimum distance away from which it can depart

        self.freqset = self.freq # Actual frequency setting

    def __repr__(self):
        return f"Hyperdrive(freq={int(self.freq.value)},mrange={self.mrange.value},gran={self.gran},effPeak={self.effPeak*100},effFall={self.effFall*100},tolerance={self.tolerance.value})"

    @property
    def Frequency(self): # Real operational frequency, adjusted for precision capability (Hz)
        return self.freq.round(self.gran-5)
    @property
    def LuminalFactor(self): # Luminal Factor: Similar function to Warp Factor (dimensionless)
        return self.Frequency.value/10000
    @property
    def LuminalCoeff(self): # A multiple of c, representing actual velocity (dimensionless)
        return np.power(self.LuminalFactor,5)
    @property
    def Velocity(self): # Travel velocity itself, presented in lightyears per hour (lyr/h)
        return (self.LuminalCoeff*c.c).to(u.lyr/u.hour)


class Voidcraft:
    def __init__(self,name,mass=1,engine=None):
        self.name=name
        self.mass=mass*u.tonne
        self.engine=engine

    @property
    def powerHyperdrive(self):
        try:
            return (self.engine.draw*self.engine.Frequency*self.mass).to(u.W)
        except:
            return 0*u.W



#print("Done")
