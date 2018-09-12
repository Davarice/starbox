print("    Loading sites...")
import collections
from .celestial import u,c

"""
### TODO ###
Stub module for LOCATION classes
"""

class Site:
    """A location on the surface of a massive celestial body.
    A natural feature, a settlement, a point of interest, etc."""
    bodyType = "Site"

    def __init__(self, name, host, phi=None, theta=None, *, parent=None, ruler=None, nat=False):
        self.name = name # Common designation
        self.host = host # The celestial body upon which this site is located
        self.parent = parent # If this is a sublocation, the parent location is what contains it
        self.tethers = [] # Synthetic structures in space with a physical connection to this site
        self.isNatural = nat

        # Positional characteristics
        self.posPhi = None # Longitude of the site, if applicable
        self.posTheta = None # Latitude of the site, if applicable

        self.ruler = ruler # Who controls it?
        self.pretenders = [] # List of entities who want control (and have a presence)

    def timeline(self):
        """Return a line detailing the following:
    Colored to match whether it is day or night:
        Local time
        A representation of the progress through the day or night
    Colored to match the season:
        YYYY/MM/DD date
    In no specific color:
        Site Name
        Site Time Zone
        Site Type
        Critical Features (Capital, space elevator, etc.)
This MAY be outsourced to the Time module and externally assigned here on init."""
        pass

    def describe(self):
        return "Generic Site"



class Station:
    """A synthetic construct in space, usually in orbit around a body.
    Distinct from voidcraft in that mobility is not a significant factor beyond initial positioning."""
    bodyType = "Station"

    def __init__(self, name, parent=None, utility="Generic"):
        self.name = name
        self.parent = parent
        self.utility = utility # A simple descriptor selected such that a "{utility} Station" could be described as a "Station designed for {utility.lower()} purposes"
        # For example, a "Research Station" is a "Station designed for research purposes"
        self.bodySubtype = "Station"

        self.posPhi = None
        self.posTheta = None
        self.posRho = None # Distance from the station to the center of the parent. If this is less than the radius of the parent, there is a problem.

        self.ruler = ruler

    def describe(self):
        return f"{self.utility} {self.bodySubtype}"


print("     Sites Loaded")
