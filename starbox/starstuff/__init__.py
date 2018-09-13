"""
### STARSTUFF INIT ###

To Galahir950 / Ryan, a creator
# MEMENTO MORI ERGO FABRICATO #

"""
print("  Loading StarStuff...")
from . import celestial, vehicle, weaponry, world

__all__ = ["generate"]

def genSol():
    sol = celestial.System("Sol")
    s = celestial.Star("the Sun", sol)

    p = celestial.Planet("Mercury", sol, orbit=87.969)

    p = celestial.Planet("Venus", sol, orbit=224.701)

    p = celestial.Planet("Earth", sol)
    m = celestial.DwarfPlanet("Luna", p, orbit=28)
    p.color = "#6ad"
    m.color = "#aaa"

    p = celestial.Planet("Mars", sol, orbit=686.971)
    p.color = "red"

    #m = celestial.Belt("Inner Belt", sol, composition={"rock":50.0,"dust":50.0})
    #c = celestial.DwarfPlanet("Ceres", m)
    #c = celestial.Minor("Vesta", m)
    #c = celestial.Minor("Pallas", m)

    p = celestial.GiantPlanet("Jupiter", sol, orbit=4332.59)
    p.composition = "Gas"
    p.color = "#fc8"

    p = celestial.GiantPlanet("Saturn", sol, orbit=10759.22)
    p.composition = "Gas"
    p.color = "#fc8"
    #m = celestial.Belt("Rings of Saturn", p, composition={"ice":95.0,"rock":5.0})

    p = celestial.GiantPlanet("Caelus", sol, orbit=30688.5)
    p.composition = "Ice"
    p.color = "#99f"

    p = celestial.GiantPlanet("Neptune", sol, orbit=60182)
    p.composition = "Ice"
    p.color = "#55a"

    #m = celestial.Belt("Kuiper Belt", sol, composition={"ice":80.0,"rock":20.0})
    #p = celestial.DwarfPlanet("Pluto", m)
    #p.composition = "Ice"

    return sol

def genBC():
    bc = celestial.System("Beta Cygni")
    s1 = celestial.Star("Albireo A")
    s2 = celestial.Star("Albireo B")

    g = celestial.GiantPlanet("Beta Cygni I", bc)
    g.composition = "Ice"

    g = celestial.GiantPlanet("Beta Cygni II", bc)
    g.composition = "Gas"
    p = celestial.Planet("Beta Cygni IIa", g)
    p = celestial.DwarfPlanet("Beta Cygni IIb", g)
    p.composition = "Ice"

    return bc

def generate():
    mw = celestial.Galaxy("Milky Way")
    mw.subAssign(genSol())
    #mw.subAssign(genBC())
    return mw

#class Generator:



print("   StarStuff Initialized")
