#print("    Loading Small Arms...", end='')
"""
/starbox/weaponry.py

Class module for:
    Guns and gun parts. Modular firearms.

By @Davarice
"""

import collections
from .celestial import u,c
import random as r

#==============#
## COMPONENTS ##
#==============#

class GunJam(Exception):
    """Firearm error"""
    pass

class Component:
    def __init__(self, qual=0, damage=0):
        self.level = qual
        self.dmg = damage

    def damage(self, n=1):
        self.dmg += n




## PLASMA COMPONENTS ##
class RoundPlasma(Component):
    dDiceMap = ["d6", "d8", "2d6", "2d8", "2d12"]
    dTypeMap = ["fire", "fire", "necrotic", "necrotic", "necrotic"]
    dColrMap = ["red", "orange", "green", "blue", "violet"]

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.Loaded = True
        self.DamageDice = self.dDiceMap[self.level]
        self.DamageType = self.dTypeMap[self.level]
        self.FXColor = self.dColrMap[self.level]

    def describe(self):
        return {True:f"gas capsule filled with {self.FXColor} vapor",
                False:"discharged gas capsule"}[self.Loaded]


class Cylinder(Component):
    slot = "" # The attribute that determines what "slot" of a weapon this component occupies
    # (This one is blank because this component has specific variants for pistols vs rifles)

    def __init__(self, qual=0, damage=0):
        super().__init__(qual, damage)
        self.contents = []

    def capacity(self):
        return self.qualCap[self.level]

    def fillWithAir(self):
        while len(self.contents) < self.capacity():
            self.contents.append(None)

    def spin(self):
        self.fillWithAir()
        for i in range(1,r.randint(10,50)): # For a random number of times...
            self.contents.append(self.contents.pop(0)) # ...Move the first item to the end
        print("The cylinder spins...")

    def load(self, ammo):
        self.fillWithAir()
        if ammo in self.contents: # If this ever occurs naturally, something has gone horribly wrong
            print("The cylinder already contains that round...")
            return
        try: # Find the first empty slot
            n = self.contents.index(None)
        except ValueError: # No slot is "None"
            print("The cylinder has no empty slots!")
            return
        else: # Stick it in ( ͡° ͜ʖ ͡°)
            self.contents[n] = ammo
class CylinderPistol(Cylinder): # Subclass variant used by pistols
    slot = "cylinder"
    qualCap = [4,5,6,7,8] # The list of ammunition capacities at various quality levels
class CylinderRifle(Cylinder): # Subclass variant used by rifles
    slot = "cylinder"
    qualCap = [8,16,20] # The list of ammunition capacities at various quality levels


class Pressurizer(Component):
    slot = "pressurizer" # The attribute that determines what "slot" of a weapon this component occupies

    def __init__(self, qual=0, damage=0):
        super().__init__(qual,damage)


class Ignition(Component):
    slot = "ignition" # The attribute that determines what "slot" of a weapon this component occupies

    def __init__(self, qual=0, damage=0):
        super().__init__(qual,damage)


class Containment(Component):
    slot = "containment" # The attribute that determines what "slot" of a weapon this component occupies

    def __init__(self, qual=0, damage=0):
        super().__init__(qual,damage)










#========#
## GUNS ##
#========#
class Firearm:
    partsNeeded = []
    gunClass = "generic"
    gunType = 0

    def __init__(self):
        self.parts = {}

    def install(self, comp):
        self.parts[comp.slot] = comp

    def isComplete(self):
        for need in self.partsNeeded:
            try:
                if self.parts[need] == None or self.parts[need].slot != need:
                    return False
            except:
                return False
        return True


class GunPlasma(Firearm):
    partsNeeded = ["cylinder","pressurizer","ignition","containment",
                   "grip","barrel","receiver"]

    def __init__(self,inputGun={},inputParts=[]):
        super().__init__()
        for slot in self.partsNeeded: # Initialize an empty weapon frame
            self.parts.update({slot:None})
        self.parts.update(inputGun) # If an existing gun has been supplied, put all its parts onto this one
        for comp in inputParts: # And finally, if any loose parts have been supplied, try to install them
            self.install(comp)

    def fire(self,target=None):
        if not self.isComplete():
            print("Nothing happens.")
            return
        ammo = self.parts["cylinder"].contents[0]
        if ammo == None:
            print("*click*")
            return
        print("From the front of the weapon extends a small flag reading, \"This feature is not yet complete\"")


class WeaponsRack():
    pass

#print("Done")
