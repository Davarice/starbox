#!/usr/bin/python3.7
import collections

"""
/starbox/celestial.py

Class module for:
    Celestial bodies: Stars, black holes, planets, etc.
    Locations on and around bodies: Settlements, elevators, stations, etc.
    Celestial structures composed of bodies: Star systems, sectors, galaxies, etc.
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

    def __init__(self, name, parent, composition="Rock", ruler=None):
        moons = [] # Natural bodies orbiting this body; Typically another planet
        satellites = [] # Synthetic structures orbiting this body; Typically a station
        sites = [] # Locations on the surface of the world, synthetic or geographical
        nations = [] # Entities controlling territory on this world (typically subservient to the ruler)

    def system():
        return self.parent.system()



