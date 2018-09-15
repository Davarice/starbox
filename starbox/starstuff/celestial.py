#print("    Loading Celestial Objects...", end='')
import collections
import astropy, math, numpy as np
from astropy import constants as c
from astropy import units as u

__all__ = ["Minor","DwarfPlanet","Planet","GiantPlanet","Star","BlackHole","Belt","System","Galaxy"]

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
u.earthMass2015 = u.def_unit("Earth Masses", c.iau2015.M_earth)
M_e = u.earthMass2015 # Earth masses: Mass unit used by typical planets

u.jupiterMass2015 = u.def_unit("Jovian Masses", c.iau2015.M_jup)
M_j = u.jupiterMass2015 # Jovian masses: Mass unit used by gas giants and small stars

u.solMass2015 = u.def_unit("Solar Masses", c.iau2015.M_sun)
M_s = u.solMass2015 # Solar masses: Mass unit used by stars and heavier

def findLargestProportion(din,flavor=0):
    dsort = [(k, din[k]) for k in sorted(din, key=din.get, reverse=True)]
    if flavor == 0:
        return dsort[0][0]
    elif flavor == 1:
        return dsort[0][0]
    else:
        return dsort[0][0]

class CelestialError(Exception):
    """Flow control: If this shows up in the console, something that raised it was not properly completed"""
    pass

def GetRho(obj):
    try: # Do this block for BODIES that are NOT Stars
        if obj.bodyType == "Star":
            raise CelestialError
        par = obj.parent
        mu = par.mass * c.G
        T = obj.lengthOrbit
        #print(f"[{obj.name}]: T={T}, mu={mu}, G={c.G}")
    except CelestialError: # Do this for BODIES that are Stars
        obj.posRho = 0 * obj.distUnit
    except AttributeError: # Do this for things that are NOT Bodies (e.g. Groupings)
        obj.posRho = 0 * obj.distUnit
    else:
        a = np.cbrt(((np.power(T,2)*mu)/math.tau))
        obj.posRho = a
        #print(f"{obj.name} has a mass of {obj.mass} and orbits {obj.parent.name} at a distance of {a}")




### Superclasses:
#print("      Initializing superclasses...")

class Body:
    """Superclass for most natural celestial objects"""
    distUnit = u.au
    minSize = 2 # When rendered, objects of this type will always be at least this radius

    def __init__(self, name, # Identity information
                 mass=1, rho=1, orbit=365, radius=100, # Physical information
                 ruler=None, space=None): # Social information
        self.name = name # Common designation
        self.orbitals = [] # Natural bodies orbiting this body; Moons, rings, etc.
        self.satellites = [] # Synthetic structures orbiting this body; Typically a station

        self.color = "#554322"
        self.localGranularity = 20

        # Physical characteristics
        self.mass = mass * self.massUnit # Mass of the planet
        self.radius = radius * u.km # Distance from the center to the surface

        # Positional characteristics
        self.posPhi = 0 # Position of the body relative to its parent
        self.posRho = 0 * self.distUnit # Distance from the body to its parent body
        #self.posRho = rho * self.distUnit
        self.lengthOrbit = orbit*24*u.hour

        self.ruler = ruler # The governing entity, if any, with total control (military or political) over this body
        self.sites = [] # Locations on the surface of the world, synthetic or geographical
        self.nations = [] # Entities controlling territory on this world (typically subservient to the ruler)

    #def getmass(self):
        #"""Just in case this is ever called here accidentally"""
        #return self.mass

    def system(self):
        """Try to find the top level object this is within.
Basically just pass it upwards until meeting a System class, which will send itself all the way back down."""
        try:
            return self.parent.system()
        except AttributeError:
            return None

    def getSubs(self, par=True, nat=True, syn=True, incself=False):
        lnat = self.orbitals
        lsyn = self.satellites
        lout = []
        if par:
            lout.append(self.parent)
        if incself:
            lout.append(self)
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
            if subloc == self:
                oput = oput + "\n    :[\033[96m{}\033[0m] {} [[SELF]]".format(n, subloc.name, subloc.bodySubtype)
            elif subloc == self.parent:
                oput = oput + "\n    :[\033[96m{}\033[0m] {} [[PRNT]]".format(n, subloc.name, subloc.bodySubtype)
            else:
                oput = oput + "\n    :[\033[96m{}\033[0m] {}".format(n, subloc.name, subloc.bodySubtype)
            n += 1
        return oput

    def describe(self):
        """Return a string of what this thing IS. A single noun with qualifiers as necessary. A Dwarf Planet, or a Gas Giant, or an Ice Giant, etc.
If the object requires a descriptor based on its composition, this can be supported by inserting {c} into its bodySubtype, as in the case of Gas/Ice Giants.
THIS METHOD SHOULD BE OVERWRITTEN for any classes that do not have a composition, such as Stars."""
        return self.bodySubtype.format(c=self.composition)

    def printData(self):
        oput = f"{self.name} is a {self.describe()} in the {self.system().name} system.\n"
        oput = oput + self.__doc__
        if self.parent != None:
            oput = oput + f"\n{self.name} is in orbit around {self.parent.name}, a {self.parent.describe()}, at a distance of {self.posRho.to(u.au).round(3)}."
            oput = oput + f"\nIt has an orbital period of {self.lengthOrbit}"
            try:
                if self.lengthOrbit == self.lengthRotation:
                    oput = oput + f", and is tidally locked."
                else:
                    oput = oput + f", and a rotational period of {self.lengthRotation}."
            except:
                oput = oput + f"."
        oput = oput + f"\n  Mass: {self.mass}\n  Radius: {self.radius}\n  Controlling faction: {self.ruler}"
        if len(self.sites) > 0:
            oput = oput + f"\nThe following points of interest can be found on its surface:"
            for obj in self.sites:
                oput = oput + f"\n  :{obj.timeline()}"
        if len(self.orbitals) > 0:
            oput = oput + f"\nIt has the following natural bodies in orbit:"
            for obj in self.orbitals:
                oput = oput + f"\n  -The {obj.describe()}, {obj.name}"
        if len(self.satellites) > 0:
            oput = oput + f"\nIt has the following synthetic structures in orbit:"
            for obj in self.satellites:
                oput = oput + f"\n  -The {obj.utility} {obj.bodyType}, {obj.name}"
        return oput

    def subAssign(self, childNew, isCore=False):
        try:
            self.orbitals.append(childNew)
            childNew.parent = self
            childNew.bodyRank = self.bodyRank + 1
            GetRho(self)
            GetRho(childNew)
        except AttributeError:
            return



class Grouping:
    """Superclass for organizational entities such as star clusters and debris fields"""
    def __init__(self, name, # Identity information
                 ruler=None, space=None): # Social information
        self.name = name
        self.orbitals = [] # Natural bodies orbiting this body; Moons, rings, etc.
        self.satellites = [] # Synthetic structures orbiting this body; Typically a station

        self.localGranularity = 50

        # Positional characteristics
        self.posPhi = 0 # Position of the body relative to its parent
        #self.posRho = None # Distance from the body to its parent body
        self.posRho = 1.2*u.au
        self.lengthOrbit = 1*u.yr

        self.ruler = ruler
        self.nations = [] # Entities controlling territory in this area (Rulers of orbitals)

    @property
    def radius(self):
        mtotal = None
        for m in self.total:
            m2 = m.mass
            if mtotal == None:
                mtotal = 0*m2.unit
            mtotal += m2
        return mtotal

    @property
    def mass(self):
        mtotal = None
        # Total MUST be defined PER SUBCLASS; The subclass determines which of its components contribute to total mass
        for m in self.total:
            m2 = m.mass
            if mtotal == None:
                mtotal = 0*m2.unit
            mtotal += m2
        return mtotal

    def system(self):
        """Try to find the top level object this is within.
Basically just pass it upwards until meeting a System class, which will send itself all the way back down."""
        try:
            return self.parent.system()
        except AttributeError:
            return None

    def describe(self):
        """Return a string of what this thing IS. A single noun with qualifiers as necessary. A Star System, or a Dwarf Galaxy, or an Asteroid Field, etc.
Unlike for Bodies, the Grouping version of this may need explicit definition for every subclass."""
        return self.bodySubtype

    def printData(self):
        oput = f"{self.name} is a {self.describe()} in the {self.system().name} system.\n"
        oput = oput + self.__doc__
        if self.parent != None:
            oput = oput + f"\n{self.name} is in orbit around {self.parent.name}, a {self.parent.describe()}."
        oput = oput + f"\n  Mass: {self.mass.round(3)}\n  Controlling faction: {self.ruler}"
        if len(self.orbitals) > 0:
            oput = oput + f"\nIt has the following natural bodies in orbit:"
            for obj in self.orbitals:
                oput = oput + f"\n  -The {obj.describe()}, {obj.name}"
        if len(self.satellites) > 0:
            oput = oput + f"\nIt has the following synthetic structures in orbit:"
            for obj in self.satellites:
                oput = oput + f"\n  -The {obj.utility} {obj.bodyType}, {obj.name}"
        return oput

    def getSubs(self, par=True, nat=True, syn=True, incself=False):
        lnat = self.orbitals
        lsyn = self.satellites
        lout = []
        if par and self.parent != None:
            lout.append(self.parent)
        if incself:
            lout.append(self)
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
            if subloc == self:
                oput = oput + "\n    :[\033[96m{}\033[0m] {} [[SELF]]".format(n, subloc)
            elif subloc == self.parent:
                oput = oput + "\n    :[\033[96m{}\033[0m] {} [[PRNT]]".format(n, subloc)
            else:
                oput = oput + "\n    :[\033[96m{}\033[0m] {}".format(n, subloc)
            #oput = oput + "\n    :[\033[96m{}\033[0m] {}".format(n, subloc) #.name, subloc.bodySubtype)
            n += 1
        return oput

    def subAssign(self, childNew, isCore=False):
        try:
            self.orbitals.append(childNew)
            childNew.parent = self
            childNew.bodyRank = self.bodyRank
        except AttributeError:
            return



#print("       Superclasses loaded")
#print("      Initializing primary classes...")
### Primary Classes:
## Body-type

class Planet(Body):
    """Planet: Most ubiquitous celestial body.
A planet is massive enough to be rounded by its own gravity, is not massive enough to cause thermonuclear fusion, and has cleared its neighbouring region of planetesimals. (from Wikipedia)"""
    bodyType = "Planet"
    bodySubtype = "Planet"
    massUnit = M_e
    minSize = 2 # When rendered, objects of this type will always be at least this radius

    def __init__(self, name, parent=None, # Identity information
                 mass=1, rho=1, orbit=365, dayLength=24, radius=100, # Physical information
                 composition="Rock",
                 ruler=None, space=None, isCore=False): # Social information
        super().__init__(name=name, mass=mass, rho=rho, orbit=orbit, radius=radius, ruler=ruler)
        #self.name = name
        self.parent = parent # The object around which this body orbits; If None, planet is Rogue
        self.composition = composition # Type of planet (rock, ice, gas, etc).
        self.orbitals = [] # Natural bodies orbiting this body; Typically another planet
        self.satellites = [] # Synthetic structures orbiting this body; Typically a station

        # Physical characteristics
        self.Gravity = 1 # Strength of surface gravity, relative to Earth

        # Temporal characteristics
        self.lengthOrbit = orbit*24*u.hour # Number of hours in a year
        self.lengthRotation = dayLength*u.hour # Number of hours taken to rotate

        self.bodyRank = 3
        try:
            self.parent.subAssign(self) # If the parent body has a specific method to integrate me, use it
        except AttributeError:
            pass

    def __str__(self):
        return f"{self.name} ({self.bodySubtype.format(c=self.composition)})"

class GiantPlanet(Planet):
    """A planet of such mass that it justifies use of a unique unit."""
    bodySubtype = "{c} Giant"
    massUnit = M_j
    minSize = 4 # When rendered, objects of this type will always be at least this radius

class DwarfPlanet(Planet):
    """A planet which is massive enough to be spherical under its own gravity, but which has not managed to clear its orbital path."""
    bodySubtype = "Dwarf Planet"
    minSize = 1 # When rendered, objects of this type will always be at least this radius


class Star(Body):
    """A standard, normally very bright, celestial body; Found in the core of most Systems."""
    bodyType = "Star"
    bodySubtype = "Star"
    massUnit = M_s
    minSize = 6 # When rendered, objects of this type will always be at least this radius

    def __init__(self, name, parent=None, # Identity information
                 mass=1, radius=100, stellarClass=None, subtype="Main Sequence", # Physical information
                 ruler=None, space=None, isCore=False): # Social information
        self.distUnit = u.lyr
        super().__init__(name=name, mass=mass, radius=radius, ruler=ruler)
        self.name = name # Common designation
        self.parent = parent # Object around which this body orbits OR group in which it belongs
        self.mass = mass * self.massUnit # Mass of the star, given in Solar Masses
        self.stellarClass = stellarClass
        self.stellarSubtype = subtype
        self.ruler = ruler
        self.orbitals = [] # Natural bodies orbiting this body; Typically planets and belts
        self.satellites = [] # Synthetic structures orbiting this body; Typically a station
        self.bodyRank = 2
        try:
            self.parent.subAssign(self, isCore=isCore) # If the parent body has a specific method to integrate me, use it
        except AttributeError:
            pass

    def system(self):
        try:
            return self.parent.system()
        except AttributeError:
            return None

    def describe(self):
        """Return a string of what this thing IS. A single noun with qualifiers as necessary. A Dwarf Planet, or a Gas Giant, or an Ice Giant, etc.
If the object requires a descriptor based on its composition, this can be supported by inserting {c} into its bodySubtype, as in the case of Gas/Ice Giants.
THIS METHOD SHOULD BE OVERWRITTEN for any classes that do not have a composition, such as Stars."""
        return self.bodySubtype

    def getSubs(self, par=True, nat=True, syn=True, incself=True):
        lnat = self.orbitals
        lsyn = self.satellites
        lout = []
        if par:
            lout.append(self.parent)
        if incself:
            lout.append(self)
        if nat:
            lout = lout + lnat
        if syn:
            lout = lout + lsyn
        return lout

    def subAssign(self, childNew, isCore=False):
        print(f"{childNew.name} asks to orbit {self.name}")
        try:
            self.orbitals.append(childNew)
            childNew.parent = self
            childNew.bodyRank = self.bodyRank + 1
            GetRho(childNew)
        except AttributeError:
            return

    def __str__(self):
        return f"{self.name} (Class {self.stellarClass} {self.bodySubtype})"

class BlackHole(Star):
    """A Black Hole is a Star which has exhausted its fuel and cooled to the point that its radius contracts gravitationally to within its Schwarzschild radius.
Escape velocity at its "surface", now called the event horizon, exceeds the speed of information."""
    bodySubtype = "Black Hole"


class Minor(Body):
    """Minor: An object too small to be gravitationally spherical
    Asteroids, meteors, comets, etc."""
    massUnit = u.kg
    bodyType = "Minor"

    def __init__(self, name, parent=None, # Identity information
                 mass=1, rho=1, orbit=365, dayLength=24, radius=100, # Physical information
                 composition="Rock",
                 ruler=None, space=None): # Social information
        super().__init__(name=name, mass=mass, rho=rho, orbit=orbit, radius=radius, ruler=ruler)
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



#print("       Primary classes loaded")
#print("      Initializing organizational classes...")
## Grouping-type

class Galaxy(Grouping):
    """A Galaxy is a grouping of stars, nebulae, dust, and other very massive objects, in orbit of a supermassive object, typically a supermassive black hole or a quasar.
Like a System, a Galaxy is comprised of a core group and a group of orbitals, where the orbitals may be empty but the core cannot be.
However, a Galaxy is so large in scale that while an incomplete System is a clerical error, an incomplete Galaxy more readily indicates the maintenance of sanity.
A Galaxy is typically used simply to encompass multiple Systems in a semblance of an organized manner."""
    bodyType = "Galaxy"

    def __init__(self, name, parent=None, # Identity information
                 posPhi=0, posRho=0, mapCoords="", # Physical information
                 ruler=None, space=None, rank=1, time=0): # Social information
        super().__init__(name=name, ruler=ruler)
        self.parent = parent # OBJ: Object around which this body orbits
        self.core = [] # Massive objects at the core of the galaxy; Typically supermassive black holes
        self.bodySubtype = "Galaxy"
        self.TIME = time

        self.ruler = ruler

        self.bodyRank = rank
        try:
            self.parent.subAssign(self) # If the parent body has a specific method to integrate me, use it
        except AttributeError:
            pass

    @property
    def total(self):
        return self.core + self.orbitals

    def system(self):
        return self

    def getSubs(self, par=True, nat=True, syn=True, incself=True):
        lcor = self.core
        lnat = self.orbitals
        lsyn = [] #self.satellites
        lout = []
        if par and self.parent != None:
            lout.append(self.parent)
        if incself:
            lout.append(self)
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

    def subAssign(self, childNew, isCore=False):
        try:
            childNew.parent = self
            if isCore:
                self.core.append(childNew)
            else:
                self.orbitals.append(childNew)
        except AttributeError:
            pass

    def __str__(self):
        return f"{self.name} ({self.bodySubtype})"

class System(Grouping):
    """System: Standard designation for a grouping of bodies, typically 1-3 stars or 2 planets
Represents a significant gravitational point, and is composed of a core group and a set of orbitals
    While unlikely (for stars), a system may have no orbitals. A system with no core objects, however, is a clerical error."""
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

    @property
    def total(self):
        return self.core #+ self.orbitals

    def system(self):
        return self

    def getSubs(self, par=True, nat=True, syn=True, incself=False):
        lcor = self.core
        lnat = self.orbitals
        lsyn = self.satellites
        lout = []
        if par and self.parent != None:
            lout.append(self.parent)
        if incself:
            lout.append(self)
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
                others += 1

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

    def subAssign(self, childNew, isCore=False):
        try:
            childNew.parent = self
            GetRho(childNew)
            if isCore:
                self.core.append(childNew)
            else:
                self.orbitals.append(childNew)
            self.refreshType()
        except AttributeError:
            pass

    def __str__(self):
        self.refreshType()
        return f"{self.name} ({self.bodySubtype})"

class Belt(Grouping):
    """Belt: A region of debris in orbit around a body, forming a ring
    A belt has a Rho, but no Phi, because it exists at every value of Phi
    Unlike a System, a belt represents a disparate cloud of abstract objects rather than a single point
    As such, "orbitals" of a Belt represent objects found within the Belt, rather than in orbit of it"""
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

    @property
    def total(self):
        return self.orbitals + self.satellites

    def system(self):
        try:
            return self.parent.system()
        except AttributeError:
            return None

    def comp(self): # Calculate what the belt is "made of"
        return findLargestProportion(self.composition,2)

    def subAssign(self, childNew, isCore=False):
        try:
            GetRho(childNew)
            self.orbitals.append(childNew)
            childNew.parent = self
            childNew.bodyRank = self.bodyRank + 1
        except AttributeError:
            pass

    def __str__(self):
        return f"{self.name} ({self.comp().capitalize()} {self.bodySubtype})"










#print("       Organizational classes loaded")


#print("Done")


