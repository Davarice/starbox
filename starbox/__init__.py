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
    sol = Star("Sol", solSys)
    p = Planet("Mercury", sol)
    p = Planet("Venus", sol)
    p = Planet("Earth", sol)
    m = Planet("Luna", p)
    p = Planet("Mars", sol)
    m = Belt("Inner Belt", sol, composition={"dust":50.0,"rock":50.0})
    p = Planet("Jupiter", sol)
    p.composition = "Gas"
    p = Planet("Saturn", sol)
    p.composition = "Gas"
    m = Belt("Rings of Saturn", p, composition={"ice":95.0,"rock":5.0})
    p = Planet("Caelus", sol)
    p.composition = "Gas"
    p = Planet("Neptune", sol)
    p.composition = "Gas"
    p = Planet("Pluto", sol)
    p.composition = "Ice"
    m = Belt("Kuiper Belt", sol, composition={"ice":80.0,"rock":20.0})
    return solSys
