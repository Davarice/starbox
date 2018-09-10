from . import celestial

__all__ = ["generate"]

def genSol():
    sol = celestial.System("Sol")
    s = celestial.Star("the Sun", sol)

    p = celestial.Planet("Mercury", sol)

    p = celestial.Planet("Venus", sol)

    p = celestial.Planet("Earth", sol)
    m = celestial.DwarfPlanet("Luna", p)

    p = celestial.Planet("Mars", sol)

    m = celestial.Belt("Inner Belt", sol, composition={"rock":50.0,"dust":50.0})
    c = celestial.DwarfPlanet("Ceres", m)
    c = celestial.Minor("Vesta", m)
    c = celestial.Minor("Pallas", m)

    p = celestial.GiantPlanet("Jupiter", sol)
    p.composition = "Gas"

    p = celestial.GiantPlanet("Saturn", sol)
    p.composition = "Gas"
    m = celestial.Belt("Rings of Saturn", p, composition={"ice":95.0,"rock":5.0})

    p = celestial.GiantPlanet("Caelus", sol)
    p.composition = "Ice"

    p = celestial.GiantPlanet("Neptune", sol)
    p.composition = "Ice"

    m = celestial.Belt("Kuiper Belt", sol, composition={"ice":80.0,"rock":20.0})
    p = celestial.DwarfPlanet("Pluto", m)
    p.composition = "Ice"

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
    mw.subAssign(genBC())
    return mw





