import collections
import astropy
from astropy import constants as c
from astropy import units as u

#__all__ = ["Minor","DwarfPlanet","Planet","GiantPlanet","Star","BlackHole","Belt","System","Galaxy"]

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

M_e = c.iau2015.M_earth # Earth masses: Mass unit used by typical planets
M_j = c.iau2015.M_jup # Jovian masses: Mass unit used by gas giants and small stars
M_s = c.iau2015.M_sun # Solar masses: Mass unit used by stars

### Superclasses:

class Body:
    """
    Superclass for most natural celestial objects
    """
    def __init__(self, name, # Identity information
                 mass=1, # Physical information
                 ruler=None, space=None): # Social information
        self.name = name
        self.orbitals = [] # Natural bodies orbiting this body; Moons, rings, etc.
        self.satellites = [] # Synthetic structures orbiting this body; Typically a station

        # Physical characteristics
        self.mass = mass * self.massUnit # Mass of the planet
        self.radius = None # Distance from the center to the surface

        # Positional characteristics
        self.posPhi = None # Position of the body relative to its parent
        self.posRho = None # Distance from the body to its parent body

        self.ruler = ruler
        self.sites = [] # Locations on the surface of the world, synthetic or geographical
        self.nations = [] # Entities controlling territory on this world (typically subservient to the ruler)

    def system(self):
        try:
            return self.parent.system()
        except AttributeError:
            return None

    def getSubs(self, par=True, nat=True, syn=True):
        lnat = self.orbitals
        lsyn = self.satellites
        lout = []
        if par:
            lout.append(self.parent)
        if nat:
            lout = lout + lnat
        if syn:
            lout = lout + lsyn
        return lout

    def subList(self):
        oput = "Current Location: {} ({})".format(self.name, self.bodySubtype)
        n = 0
        oput = oput + "\n    Adjacent locations:"
        for subloc in self.getSubs():
            oput = oput + "\n    :[\033[96m{}\033[0m] {} ({})".format(n, subloc.name, subloc.bodySubtype)
            n += 1
        return oput

    def subAssign(self, childNew):
        try:
            self.orbitals.append(childNew)
            childNew.parent = self
            childNew.bodyRank = self.bodyRank + 1
            #if self.system() != None:
                #self.system().subAssign(childNew)
        except AttributeError:
            return



class Grouping:
    """
    Superclass for organizational entities such as star clusters and debris fields
    """
    def __init__(self, name, # Identity information
                 ruler=None, space=None): # Social information
        self.name = name
        self.orbitals = [] # Natural bodies orbiting this body; Moons, rings, etc.
        self.satellites = [] # Synthetic structures orbiting this body; Typically a station

        # Positional characteristics
        self.posPhi = None # Position of the body relative to its parent
        self.posRho = None # Distance from the body to its parent body

        self.ruler = ruler
        self.sites = [] # Locations on the surface of the world, synthetic or geographical
        self.nations = [] # Entities controlling territory on this world (typically subservient to the ruler)

    def system(self):
        try:
            return self.parent.system()
        except AttributeError:
            return None

    def getSubs(self, par=True, nat=True, syn=True):
        lnat = self.orbitals
        lsyn = self.satellites
        lout = []
        if par and self.parent != None:
            lout.append(self.parent)
        if nat:
            lout = lout + lnat
        if syn:
            lout = lout + lsyn
        return lout

    def subList(self):
        oput = "Current Location: {} ({})".format(self.name, self.bodySubtype)
        n = 0
        oput = oput + "\n    Adjacent locations:"
        for subloc in self.getSubs():
            oput = oput + "\n    :[\033[96m{}\033[0m] {}".format(n, subloc) #.name, subloc.bodySubtype)
            n += 1
        return oput

    def subAssign(self, childNew):
        try:
            self.orbitals.append(childNew)
            childNew.parent = self
            childNew.bodyRank = self.bodyRank
            #if self.system() != None:
                #self.system().subAssign(childNew)
        except AttributeError:
            return



### Primary Classes:
## Body-type

class Planet(Body):
    """
    Planet: Most ubiquitous celestial body
    name, str: Common designation
    parent, obj: The object around which this body orbits; If None, planet is Rogue
    composition, str: Type of planet (Rock, ice, gas).
    ruler, obj: The governing entity, if any, with total control over this body
    """
    bodyType = "Planet"
    bodySubtype = "Planet"
    massUnit = M_e

    def __init__(self, name, parent=None, # Identity information
                 mass=1, composition="Rock", # Physical information
                 ruler=None, space=None, dayLength=24): # Social information
        super().__init__(name=name, mass=mass, ruler=ruler)
        #self.name = name
        self.parent = parent
        self.composition = composition
        self.orbitals = [] # Natural bodies orbiting this body; Typically another planet
        self.satellites = [] # Synthetic structures orbiting this body; Typically a station

        # Physical characteristics
        self.radius = None # Distance from the center to the surface
        self.Gravity = 1 # Strength of surface gravity, relative to Earth

        # Temporal characteristics
        self.periodRotation = dayLength # Number of hours taken to rotate
        self.periodOrbital = None # Number of hours in a year

        self.bodyRank = 3
        try:
            self.parent.subAssign(self) # If the parent body has a specific method to integrate me, use it
        except AttributeError:
            pass

    def __str__(self):
        return f"{self.name} ({self.composition} {self.bodySubtype})"

class GiantPlanet(Planet):
    bodySubtype = "Giant"
    massUnit = M_j

class DwarfPlanet(Planet):
    bodySubtype = "Dwarf Planet"


class Star(Body):
    """
    Star: Standard, very bright, celestial body; Core of most Systems
    """
    bodyType = "Star"
    bodySubtype = "Star"
    massUnit = M_s

    def __init__(self, name, parent=None, # Identity information
                 mass=1, stellarClass="D", subtype="Main Sequence", # Physical information
                 ruler=None, space=None): # Social information
        super().__init__(name=name, mass=mass, ruler=ruler)
        self.name = name # STR: Common designation
        self.parent = parent # OBJ: Object around which this body orbits
        self.mass = mass # FLOAT: Mass of the star, given in Solar Masses
        self.stellarClass = stellarClass
        self.stellarSubtype = subtype
        self.ruler = ruler
        self.orbitals = [] # Natural bodies orbiting this body; Typically planets and belts
        self.satellites = [] # Synthetic structures orbiting this body; Typically a station
        self.bodyRank = 2
        try:
            self.parent.subAssign(self) # If the parent body has a specific method to integrate me, use it
        except AttributeError:
            pass

    def system(self):
        try:
            return self.parent.system()
        except AttributeError:
            return None

    def getSubs(self, par=True, nat=True, syn=True):
        lnat = self.orbitals
        lsyn = self.satellites
        lout = []
        if par:
            lout.append(self.parent)
        if nat:
            lout = lout + lnat
        if syn:
            lout = lout + lsyn
        return lout

    def subAssign(self, childNew):
        try:
            self.orbitals.append(childNew)
            childNew.parent = self
            childNew.bodyRank = self.bodyRank + 1
            #if self.parent.bodyType == "System":
                #self.parent.subAssign(childNew)
        except AttributeError:
            return

    def __str__(self):
        return f"{self.name} (Class {self.stellarClass} {self.bodySubtype})"

class BlackHole(Star):
    bodySubtype = "Black Hole"


class Minor(Body):
    """
    Minor: An object too small to be gravitationally spherical
    Asteroids, meteors, comets, etc.
    """
    massUnit = u.kg
    bodyType = "Minor"

    def __init__(self, name, parent=None, # Identity information
                 mass=1, composition="Rock", # Physical information
                 ruler=None, space=None, stype="Asteroid"): # Social information
        super().__init__(name=name, mass=mass, ruler=ruler)
        self.parent = parent
        self.composition = composition
        self.bodySubtype = stype

        self.bodyRank = 4
        try:
            self.parent.subAssign(self) # If the parent body has a specific method to integrate me, use it
        except AttributeError:
            pass

    def __str__(self):
        return f"{self.name} ({self.composition} {self.bodySubtype})"



## Grouping-type

class Galaxy(Grouping):
    """
    System: Standard designation for a grouping of bodies, typically 1-3 stars or 2 planets
    Represents a significant gravitational point, and is composed of a core as well as orbitals
    """
    bodyType = "Galaxy"

    def __init__(self, name, parent=None, # Identity information
                 posPhi=0, posRho=0, mapCoords="", # Physical information
                 ruler=None, space=None, rank=1): # Social information
        super().__init__(name=name, ruler=ruler)
        self.parent = parent # OBJ: Object around which this body orbits
        self.posPhi = posPhi
        self.posRho = posRho
        self.mapCoords = mapCoords
        self.core = [] # Massive objects at the core of the galaxy; Typically supermassive black holes
        self.bodySubtype = "Galaxy"

        self.ruler = ruler

        self.bodyRank = rank
        try:
            self.parent.subAssign(self) # If the parent body has a specific method to integrate me, use it
        except AttributeError:
            pass

    def system(self):
        return self

    def getSubs(self, par=True, nat=True, syn=True):
        lcor = self.core
        lnat = self.orbitals
        lsyn = [] #self.satellites
        lout = []
        if par and self.parent != None:
            lout.append(self.parent)
        if nat:
            lout = lout + lcor
            lout = lout + lnat
        if syn:
            lout = lout + lsyn
        return lout

    def subsList(self):
        oput = "{}: {}".format(self.bodySubtype, self.name)
        oput = oput + "\n    Core:"
        for subloc in self.heads:
            oput = oput + "\n    --{} ({})".format(subloc.name, subloc.bodySubtype)
        oput = oput + "\n    Orbitals:"
        for subloc in self.bodies:
            oput = oput + "\n    --{} ({})".format(subloc.name, subloc.bodySubtype)
        return oput

    def subAssign(self, childNew):
        try:
            childNew.parent = self
            if childNew.bodyRank > self.bodyRank:
                self.orbitals.append(childNew)
            elif childNew.bodyRank == self.bodyRank:
                self.core.append(childNew)
        except AttributeError:
            pass

    def __dict__(self):
        return {"heads" : self.core, "bodies" : self.orbitals}

    def __str__(self):
        return f"{self.name} ({self.bodySubtype})"

class System(Grouping):
    """
    System: Standard designation for a grouping of bodies, typically 1-3 stars or 2 planets
    Represents a significant gravitational point, and is composed of a core as well as orbitals
    """
    bodyType = "System"

    def __init__(self, name, parent=None, # Identity information
                 posPhi=0, posRho=0, mapCoords="", # Physical information
                 ruler=None, space=None, rank=2): # Social information
        super().__init__(name=name, ruler=ruler)
        self.parent = parent # OBJ: Object around which this body orbits
        self.posPhi = posPhi
        self.posRho = posRho
        self.mapCoords = mapCoords
        self.core = [] # Massive objects at the core of the system; Typically stars
        self.bodySubtype = "System"

        self.ruler = ruler

        self.bodyRank = rank
        try:
            self.parent.subAssign(self) # If the parent body has a specific method to integrate me, use it
        except AttributeError:
            pass

    def system(self):
        return self

    def getSubs(self, par=True, nat=True, syn=True):
        lcor = self.core
        lnat = self.orbitals
        lsyn = self.satellites
        lout = []
        if par and self.parent != None:
            lout.append(self.parent)
        if nat:
            lout = lout + lcor
            lout = lout + lnat
        if syn:
            lout = lout + lsyn
        return lout

    def refreshType(self):
        ret = "System"
        size = len(self.core)
        stars = 0
        others = 0
        planets = 0
        for obj in self.core:
            if "Star" in obj.bodySubtype:
                stars += 1
            elif "Planet" in obj.bodyType:
                planets += 1
            else:
                other += 1

        if others == 0 and planets == 0: # All items are stars
            ret = "Star " + ret
        if others == 0 and stars == 0: # All items are planets
            ret = "Planetary " + ret

        if size == 2:
            ret = "Binary " + ret
        if size == 3:
            ret = "Trinary " + ret
        if size > 3:
            ret = "Compound " + ret

        self.bodySubtype = ret

    def subsList(self):
        oput = "{}: {}".format(self.bodySubtype, self.name)
        oput = oput + "\n    Core:"
        for subloc in self.heads:
            oput = oput + "\n    --{} ({})".format(subloc.name, subloc.bodySubtype)
        oput = oput + "\n    Orbitals:"
        for subloc in self.bodies:
            oput = oput + "\n    --{} ({})".format(subloc.name, subloc.bodySubtype)
        return oput

    def subAssign(self, childNew):
        try:
            if childNew.bodyRank > self.bodyRank:
                self.orbitals.append(childNew)
            elif childNew.bodyRank == self.bodyRank:
                self.core.append(childNew)
            self.refreshType()
        except AttributeError:
            pass

    def __dict__(self):
        return {"heads" : self.core, "bodies" : self.orbitals}

    def __str__(self):
        self.refreshType()
        return f"{self.name} ({self.bodySubtype})"

class Belt(Grouping):
    """
    Belt: A region of debris in orbit around a body, forming a ring
    A belt has a Rho, but no Phi, because it exists at every value of Phi
    Unlike a System, a belt represents a disparate cloud of abstract objects rather than a single point
    As such, orbitals of a Belt represent objects found within the Belt, rather than in orbit of it
    """
    bodyType = "Belt"

    def __init__(self, name, parent=None, # Identity information
                 posRho=0, composition={"Rock":100.0}, # Physical information
                 ruler=None, space=None, rank=3): # Social information
        super().__init__(name=name, ruler=ruler)

        self.parent = parent # OBJ: Object around which this body orbits
        self.composition = composition

        self.bodyRank = rank
        try:
            self.parent.subAssign(self) # If the parent body has a specific method to integrate me, use it
        except AttributeError:
            pass

        if self.parent.bodyType == "System":
            self.bodySubtype = "Belt"
        elif self.parent.bodyType == "Planet":
            self.bodySubtype = "Ring"
        else:
            self.bodySubtype = "Cloud"

    def system(self):
        try:
            return self.parent.system()
        except AttributeError:
            return None

    def comp(self): # Calculate what the belt is "made of"
        return findLargestProportion(self.composition,True)

    def subAssign(self, childNew):
        try:
            self.orbitals.append(childNew)
            childNew.parent = self
            childNew.bodyRank = self.bodyRank + 1
            #if self.parent.bodyType == "System":
                #self.parent.subAssign(childNew)
        except AttributeError:
            pass

    def __str__(self):
        return f"{self.name} ({self.comp().capitalize()} {self.bodySubtype})"















