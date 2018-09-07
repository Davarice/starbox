#!/usr/bin/python3.7
import collections
import decimal
from scipy import constants

__all__ = ["Planet","Star"]

"""
/starbox/celestial.py

Class module for:
    Celestial bodies: Stars, black holes, planets, etc.
    Locations on and around bodies: Settlements, elevators, stations, etc.
    Celestial structures composed of bodies: Star systems, sectors, galaxies, etc.


bodyRank: Hierarchy of mass of celestials
    0: Universal center (Great Attractor)
    1: Galactic center (SMBH, quasar)
    2: Galactic child (BH, star, IS vessel)
    3: Stellar child (Planet, belt, IP vessel)
    4: Planetary child (Moon, belt, orbital vessel)
    5: Planetary grandchild (Orbital vessel around a moon)

"""

class Planet:
    """
    Planet: Most ubiquitous celestial body
    name, str: Common designation
    parent, obj: The object around which this body orbits; If None, planet is Rogue
    composition, str: Type of planet (Rock, ice, gas).
    ruler, obj: The governing entity, if any, with total control over this body
    """
    bodyType = "Planet"

    def __init__(self, name, parent=None, # Identity information
                 composition="Rock", # Physical information
                 ruler=None, space=None): # Social information
        self.name = name
        self.parent = parent
        self.composition = composition
        self.ruler = ruler
        self.moons = [] # Natural bodies orbiting this body; Typically another planet
        self.satellites = [] # Synthetic structures orbiting this body; Typically a station
        self.sites = [] # Locations on the surface of the world, synthetic or geographical
        self.nations = [] # Entities controlling territory on this world (typically subservient to the ruler)
        self.bodyRank = 3
        try:
            self.parent.subAssign(self) # If the parent body has a specific method to integrate me, use it
        except AttributeError:
            return None

    def __str__(self):
        return '"{}": A {} {} in the {} system'.format(self.name, self.composition.lower(), self.bodyType.lower(), self.system())

    def system(self):
        try:
            return self.parent.system()
        except AttributeError:
            return None

    def subAssign(self, childNew):
        try:
            self.moons.append(childNew)
            childNew.parent = self
            childNew.bodyRank = self.bodyRank + 1
        except AttributeError:
            return


class Star:
    """
    Star: Standard, very bright, celestial body; Core of most Systems
    """
    bodyType = "Star"

    def __init__(self, name, parent=None, # Identity information
                 mass=1, stellarClass="D", subtype="Main Sequence", # Physical information
                 ruler=None, space=None): # Social information
        self.name = name # STR: Common designation
        self.parent = parent # OBJ: Object around which this body orbits
        self.mass = mass # DEC: Mass of the star, given in Solar Masses
        self.stellarClass = stellarClass
        self.stellarSubtype = subtype
        self.ruler = ruler
        self.planets = [] # Natural bodies orbiting this body; Typically planets and belts
        self.satellites = [] # Synthetic structures orbiting this body; Typically a station
        self.bodyRank = 2

    def system(self):
        return self.system

    def subAssign(self, childNew):
        try:
            self.planets.append(childNew)
            childNew.parent = self
            childNew.bodyRank = self.bodyRank + 1
        except AttributeError:
            return

class MainSequence(Star):
    pass

class DwarfStar(Star):
    pass

class Pulsar(Star):
    pass

class NeutronStar(Star):
    pass

class BlackHole(Star):
    pass















