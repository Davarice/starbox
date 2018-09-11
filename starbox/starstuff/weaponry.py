print("    Loading Small Arms...")
import collections
from .celestial import u,c
import random as r

"""
### TODO ###
Stub module for WEAPON classes
"""

## COMPONENTS ##
class Component:
    def __init__(self, qual=0, damage=0):
        self.level = qual
        self.dmg = damage

    def damage(n=1):
        self.dmg += n




## PLASMA COMPONENTS ##
class Cylinder(Component):
    # The attribute that determines what "slot" of a weapon this component occupies
    slot = "" # (This one is blank because this component has specific variants for pistols vs rifles)

    def __init__(self, qual=0, damage=0):
        super().__init__(qual,damage)
        self.contents = []

    def capacity(self):
        return self.qualCap[self.level]

    def fillWithAir(self):
        while len(self.contents) < self.capacity():
            self.contents.append(None)

    def spin(self):
        self.fillWithAir()
        for i in range(1,r.randint(6,36)):
            self.contents.append(self.contents.pop(0))
        print("The cylinder spins...")

    def load(self,ammo):
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










## GUNS ##
class Firearm:
    def __init__(self):
        self.parts = {}

    def isComplete(self):
        for need in self.partsNeeded:
            try:
                if self.parts[need] == None or self.parts[need].slot != need:
                    return False
            except AttributeError:
                return False
        return True

class gunPlasma(Firearm):
    def install(self, comp):
        self.parts[comp.slot] = comp

    def __init__(self,inputGun={},inputParts=[]):
        super().__init__()
        self.partsNeeded = ["cylinder","pressurizer","ignition","containment",
                            "grip","barrel","receiver"]
        for slot in self.partsNeeded: # Initialize an empty weapon frame
            self.parts.update({slot:None})
        self.parts.update(inputGun) # 
        for comp in inputParts:
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

print("     Small Arms Locked and Loaded")
