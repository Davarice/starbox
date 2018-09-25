#print("    Loading Vehicles...", end='')
import collections
from .celestial import u,c

"""
### TODO ###
Stub module for VEHICLE classes
"""

class Hyperdrive:
    def __init__(self,freq=63288,mrange=30,gran=3,effPeak=80,effFall=0.1,tolerance=30):
        self.freq=freq*u.Hz # The frequency of oscillation at which the hyperdrive is at its Efficiency Peak
        self.mrange=mrange*u.lyr # The maximum distance a given hyperdrive is capable of covering on a single charge
        self.gran=gran # A measure of precision; how many significant digits can be applied to the frequency setting
        self.effPeak=effPeak/100 # The maximum energy efficiency the hyperdrive can attain
        self.effFall=effFall/100 # The percentage deducted from the Peak Efficiency for each Hz difference between frequency and Ideal Frequency
        self.tolerance=tolerance*(u.au/u.solMass2015) # The maximum distance from a massive body at which the hyperdrive can arrive, and the minimum distance away from which it can depart

        self.Frequency = self.freq # Actual frequency setting

    def __repr__(self):
        return f"Hyperdrive(freq={int(self.freq.value)},mrange={self.mrange.value},gran={self.gran},effPeak={self.effPeak*100},effFall={self.effFall*100},tolerance={self.tolerance.value})"

    @property
    def Velocity(self):
        pass


#print("Done")
