import sys
import pickle
import json
import collections
from .celestial import *

#__all__ = ["genSol"]

def starbox():
    pass


def genSol():
    solSys = System("Sol")
    sol = Star("the Sun", solSys)

    p = Planet("Mercury", sol)

    p = Planet("Venus", sol)

    p = Planet("Earth", sol)
    m = DwarfPlanet("Luna", p)

    p = Planet("Mars", sol)

    m = Belt("Inner Belt", sol, composition={"dust":50.0,"rock":50.0})
    c = DwarfPlanet("Ceres", m)

    p = GiantPlanet("Jupiter", sol)
    p.composition = "Gas"

    p = GiantPlanet("Saturn", sol)
    p.composition = "Gas"
    m = Belt("Rings of Saturn", p, composition={"ice":95.0,"rock":5.0})

    p = GiantPlanet("Caelus", sol)
    p.composition = "Ice"

    p = GiantPlanet("Neptune", sol)
    p.composition = "Ice"

    p = DwarfPlanet("Pluto", sol)
    p.composition = "Ice"

    m = Belt("Kuiper Belt", sol, composition={"ice":80.0,"rock":20.0})
    return solSys
