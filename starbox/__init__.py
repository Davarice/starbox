import sys
import pickle
import json

import collections
import astropy
from astropy import constants as c
from astropy import units as u

from .celestial import *

#__all__ = ["genSol"]

def starbox():
    pass


def genSol():
    sol = System("Sol")
    s = Star("the Sun", sol)

    p = Planet("Mercury", sol)

    p = Planet("Venus", sol)

    p = Planet("Earth", sol)
    m = DwarfPlanet("Luna", p)

    p = Planet("Mars", sol)

    m = Belt("Inner Belt", sol, composition={"rock":50.0,"dust":50.0})
    c = DwarfPlanet("Ceres", m)
    c = Minor("Vesta", m)
    c = Minor("Pallas", m)

    p = GiantPlanet("Jupiter", sol)
    p.composition = "Gas"

    p = GiantPlanet("Saturn", sol)
    p.composition = "Gas"
    m = Belt("Rings of Saturn", p, composition={"ice":95.0,"rock":5.0})

    p = GiantPlanet("Caelus", sol)
    p.composition = "Ice"

    p = GiantPlanet("Neptune", sol)
    p.composition = "Ice"

    m = Belt("Kuiper Belt", sol, composition={"ice":80.0,"rock":20.0})
    p = DwarfPlanet("Pluto", m)
    p.composition = "Ice"

    return sol

def generate():
    return genSol()





