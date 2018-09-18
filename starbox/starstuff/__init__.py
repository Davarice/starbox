"""
### STARSTUFF INIT ###

To Galahir950 / Ryan, a creator
# MEMENTO MORI ERGO FABRICATO #

"""
#print("  Loading StarStuff...")
from . import celestial, vehicle, weaponry, world

__all__ = ["generate"]

def genSol():
    sol = celestial.System("Sol")
    s = celestial.Star("the Sun", sol, radius=695700, isCore=True)
    s.color = "#fc8"
    #s = celestial.BlackHole("Gargantua", sol, mass=1, radius=695700)
    #s.color = "#111111"

    p = celestial.Planet("Mercury", sol, orbit=87.969, radius=2439.7)
    p.color = "#aaaaaa"

    p = celestial.Planet("Venus", sol, orbit=224.701, radius=6051.8)
    p.color = "#efefe8"

    p = celestial.Planet("Earth", sol, orbit=365, radius=6371)
    p.color = "#6ad"
    m = celestial.DwarfPlanet("Luna", p, orbit=28, dayLength=28*24, radius=1737.1)
    m.color = "#aaa"

    p = celestial.Planet("Mars", sol, orbit=686.971, radius=3389.5)
    p.color = "#cc734c"

    m = celestial.Belt("Inner Belt", sol, radius=0.5, posRho=2.7, composition={"rock":50.0,"dust":50.0})
    c = celestial.DwarfPlanet("Ceres", m, orbit=1681.63)
    c = celestial.Minor("4 Vesta", m, orbit=1325.75)
    c = celestial.Minor("2 Pallas", m, orbit=1686)

    p = celestial.GiantPlanet("Jupiter", sol, orbit=4332.59, radius=69911)
    p.composition = "Gas"
    p.color = "#b89776"

    p = celestial.GiantPlanet("Saturn", sol, orbit=10759.22, radius=58232)
    p.composition = "Gas"
    p.color = "#f2dea9"
    m = celestial.Belt("Rings of Saturn", p, radius=36500, posRho=67300+36500, composition={"ice":95.0,"rock":5.0})

    p = celestial.GiantPlanet("Caelus", sol, orbit=30688.5, radius=25362)
    p.composition = "Ice"
    p.color = "#9fb0c6"

    #>>> (67,-2)@50; (13422,-405)@10k
    p = celestial.GiantPlanet("Neptune", sol, orbit=60182, radius=24622)
    p.composition = "Ice"
    p.color = "#5279cc"

    m = celestial.Belt("Kuiper Belt", sol, radius=4, posRho=44, composition={"ice":80.0,"rock":20.0})
    p = celestial.DwarfPlanet("Pluto", m, orbit=90560, radius=1188.3)
    p.composition = "Ice"

    return sol

def genBC():
    bc = celestial.System("Beta Cygni")
    s1 = celestial.Star("Albireo A", bc, radius=695700, isCore=True)
    s2 = celestial.Star("Albireo B", bc, radius=995700, isCore=True)
    s3 = celestial.Star("Albireo C", bc, radius=395700, isCore=True)

    g = celestial.GiantPlanet("Beta Cygni I", bc, orbit=4332.59, radius=69911)
    g.composition = "Ice"

    g = celestial.GiantPlanet("Beta Cygni II", bc, orbit=60182, radius=24622)
    g.composition = "Gas"
    p = celestial.Planet("Beta Cygni IIa", g, orbit=87.969, radius=2439.7)
    p = celestial.DwarfPlanet("Beta Cygni IIb", g, orbit=107.969, radius=2439.7)
    p.composition = "Ice"

    return bc

def generate():
    mw = celestial.Galaxy("Milky Way")
    mw.subAssign(genSol())
    mw.subAssign(genBC())
    return mw

#class Generator:



#print("   StarStuff Initialized")
