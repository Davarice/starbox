#print("    Loading SpaceTurtle...", end='')
from astropy import units as u
from tkinter import font as tkFont
import os, tkinter, math, cmath, numpy

_targRes = 2

colors = {"rock":"#373","gas":"#bb4","ice":"#99f"}

colorScreen = "#222"#"#222420" # Grey with very slight green tint
#colorScreen = "#1f241d" # More pronounced gold-green tint

colorDarkGrid = "#303030"
colorTickGrid = "#577"#"#2c3c3c" #"#433343"
colorCentGrid = "#688"#"#3c4c4c"

colorOrbit = "#886"#"#444433"

colorCenterTrace = "#333"
colorParentTrace = "#868"#"#303030"

"""
Rendering module for drawing starmaps
"""

# Common CRT display resolutions
RESOLUTIONS = [[640,480], # 1
               [800,600], # 2
               [1024,768], # 3
               [1200,900], # 4
               [1280,960], # 5
               [1600,1200]] # 6

# Output resolution (The resolution of CRT display to be simulated)
_OUTPUT = RESOLUTIONS[_targRes]

# The density of the grid of viewable locations
navGranularity = 400
setGranularity = 0

CLOCK_ = None

""" # Balance values for RGB->NTSC conversion and vice versa, based on wavelength overlaps
R' = .905R + .286G - .191B
G' = -.16R + 1.177G - .017B
B' = .152R + .298G + .55B

R = .991R' - .326G' + .333B'
G = .129R' + .801G' + .069B'
B = -.344R' - .344G' + 1.689B'
"""

# Convolution matrix to be applied by GIMP. Simulates composite NTSC signal.
# (This block is rotated 90deg because GIMP reads it by columns)
gconv = [0,0,0,0,0,
         0,0,1,0,0,
         0,0,1,0,0,
         0,0,1,0,0,
         0,0,0,0,0]


# The operations which are done to a starmap in GIMP. Note that the format is Python 2.7.
                  # Source block
GimpOperations = ['img = pdb.gimp_file_load("{i}", "{i}")',
                  'drw = img.active_drawable',
                  'pdb.gimp_layer_add_alpha(drw)',

                  # Signal block
                  'pdb.plug_in_antialias(img, drw)',
                  f'pdb.gimp_image_scale(img, {_OUTPUT[0]+4}, {_OUTPUT[1]+4})',
                  f'pdb.gimp_image_crop(img, {_OUTPUT[0]}, {_OUTPUT[1]}, 2, 2)',
                  #'pdb.plug_in_colors_channel_mixer(img,drw,0, 1.1,0,0, 0,1,0, 0,0,1)',
                  # Color balance, to simulate the color channels of an old monitor going out of sync

                  # NTSC composite signal
                  'pdb.plug_in_colors_channel_mixer(img,drw,0, 0.905,0.286,-0.191, -0.16,1.177,-0.017, 0.152,0.298,0.55)',
                  #'a1, _, _, _ = pdb.plug_in_decompose(img, drw, "LCH", 1)',
                  #'[llum, lchr, lhue] = a1.layers', # Split it into Luma, Chroma, and Hue for signal distortion
                  #'pdb.plug_in_recompose(a1, None)', # ~$ git commit -a
                  f'pdb.plug_in_convmatrix(img, drw, 25, {gconv}, 0, 3, 0, 5, [1,1,1,1,1], 0)',

                  # Chromatic block
                  'a2, _, _, _ = pdb.plug_in_decompose(img, drw, "RGB", 1)',
                  '[lred, lgrn, lblu] = a2.layers', # Split it into R/G/B
                  'pdb.plug_in_gauss_rle2(a2, lred, 4, 3)',# Very slightly defocus the red channel (in 4:3 of course)
                  'pdb.plug_in_mblur_inward(a2, lred, 2, 2, 45, {w}, {h})', # Bleed it into the glass
                  'pdb.plug_in_gauss_rle2(a2, lgrn, 2, 1)',# VERY slightly defocus the grn channel
                  'pdb.plug_in_mblur_inward(a2, lgrn, 2, 1, 45, {w}, {h})', # Bleed it into the glass
                  'pdb.plug_in_recompose(a2, None)', # ~$ git commit -a

                  # Screen block
                  'pdb.plug_in_softglow(img, drw, 30, 1, 1)',
                  'pdb.plug_in_video(img, drw, 5, 1, 0)',
                  'pdb.plug_in_lens_distortion(img, drw, 0, 0, 4, 12, 0, -20)',
                  #'pdb.plug_in_lens_distortion(img, drw, 0, 0, 60, 6, 14, -8)', # More dramatic bend

                  # Export "block"
                  'pdb.file_png_save(img, drw, "{o}.png", "{o}.png", 0, 9, 0, 0, 0, 0, 0)']

def gimpRender(i,o,w=_OUTPUT[0],h=_OUTPUT[1]):
    gstring = "gimp -idf --batch-interpreter=python-fu-eval -b '"
    for line in GimpOperations:
        gstring = gstring + line.format(w=w/2,h=h/2,i=i,o=o) + "; "
    gstring = gstring + "gimp.exit()' >/dev/null 2>/dev/null"
    os.system(gstring)

limit = 100

def getScale(w, h, loc):
    #print("Getting scale")
    # Because the system is a circle, limit to lower measurement
    if w <= h:
        limit = w
    else:
        limit = h
    limit -= 20

    # Find the outer reaches of the system (this is an Astropy quantity)
    extent = 1*u.m
    #print(f"\nExtent BEGINS at {extent.round(3)}.")
    if len(loc.orbitals) > 0:
        #for p in loc.getSubs(par=False,syn=False):
        for p in loc.orbitals:
            #print(f"  Checking whether {p.name} is more than {extent.round(3)} away...")
            try:
                trad = p.posRho + p.radius
            except:
                trad = p.posRho
            try:
                if trad > extent:
                    #print(f"  It is. {trad.round(3)} > {extent.round(3)}.")
                    extent = trad
                #else:
                    #print(f"  It is NOT. {trad.round(3)} < {extent.round(3)}.")
            except:
                pass
    else:
        extent = loc.radius * 3
    scale = limit/extent
    scale = scale/2
    #print(f"\nEXTENT of {loc.name} is {extent.round(3)}.\nLIMIT of screen is {limit}.\nSCALE set to {limit}/(2*{extent.round(3)}).\n(This equals {scale}.)")
    #print(f"\nSCALE: {scale} = ({limit}/{extent})/2 = {scale.si}\n")
    return scale.to(1/u.au)


def getRenderRadius(obj,s):
    r = obj.radius.to(u.au)*s # The actual onscreen size of the object
    m = obj.minSize # The minimum size of the object according to its type
    if numpy.greater(m,r): # Return the larger of the two
        return m
    else:
        return r

#def getPos

def drawObject(c, x, y, r, rgb="#888"):
    #print("Drawing dot")
    x0 = x - r
    x1 = x + r

    y0 = y - r
    y1 = y + r
    c.create_oval(x0, y0, x1, y1, outline=rgb, fill=rgb)

def drawOrbit(c, O, rho, phi, rgb=colorOrbit, width=1):
    [x0,y0] = [O[0]-rho,O[1]-rho]
    [x1,y1] = [O[0]+rho,O[1]+rho]
    c.create_arc(x0, y0, x1, y1, style="arc", outline=rgb, width=width, start=-phi.to(u.degree).value, extent=359.999999)


def drawSomething(c, loc, w, h, x, y, s, color="#fe4", direct=2, z=1, NoCore=False):
    for obj in loc.orbitals:
        if obj.bodyType != "Belt":
            rho = obj.posRho.to(u.au)*s
            phi = obj.posPhi
            cart = cmath.rect(rho, phi.value) # Complex number representing the X and Y of OBJ relative to LOC

            if -10 < x+cart.real < w+10 and -10 < y+cart.imag < h+10 and rho > 30:
                c.create_line(x, y, x+cart.real, y+cart.imag, fill=colorParentTrace)
            drawOrbit(c=c, O=[x,y], rho=rho, phi=phi)
            drawSomething(c=c, loc=obj, w=w, h=h, x=x+cart.real, y=y+cart.imag, s=s, direct=direct-1, z=z)
        else:
            rho = obj.posRho.to(u.au)*s
            phi = 0*u.radian
            rad = obj.radius.to(u.au)*s
            #print(f"'{obj.radius.value} TIMES {s.value} IS {rad}'")

            #print(f"Width of {obj.name} is {obj.radius}; It extends from {obj.posRho-obj.radius} to {obj.posRho+obj.radius} away from the center of {obj.parent.name}, with an average distance of {obj.posRho}.\nAt a zoom level of {z} it should have an apparent width of {rad} and an apparent distance of {rho}.")

            drawOrbit(c=c, O=[x,y], rho=rho, phi=phi, width=rad, rgb="#4d4020")
            drawSomething(c=c, loc=obj, w=w, h=h, x=x, y=y, s=s, direct=direct, z=z, NoCore=True)
    if not NoCore:
        try:
            n0 = len(loc.core)
            n1 = n0-1
            rr = 0
            for obj in loc.core:
                rr += getRenderRadius(obj,s)*n1
            i=0
            #print(rr)
            #drawOrbit(c=c, O=[x,y], rho=rr, phi=0)
            for obj in loc.core: # Draw cores of the object at the center
                i += 1
                cart = cmath.rect(rr, (math.tau/n0)*i)
                #cart = cmath.rect(obj.posRho.to(u.au)*s, obj.posPhi)
                drawObject(c, x+cart.real, y+cart.imag, getRenderRadius(obj,s), rgb=obj.color)
                c.create_text(x+cart.real,y+cart.imag+15+getRenderRadius(obj,s), fill="white", text=obj.name, font=tkFont.Font(family="xos4 Terminus",size=18))
        except AttributeError:
            drawObject(c, x, y, getRenderRadius(loc,s), rgb=loc.color) #colors[loc.composition.lower()])
            if direct > 0:
                c.create_text(x,y+15+getRenderRadius(loc,s), fill="white", text=loc.name, font=tkFont.Font(family="xos4 Terminus",size=18))
            #print(f"Drawing {loc.name} at ({x},{y}) with a radius of {limit/60}")
        #except:
        #pass



def drawGRID(img, inp, zoom, xoff, yoff, w, h, s, o1, g):
    x2 = w/3

    # Setup
    if inp == None: # If this is None, a "blank" frame is to be made
        zdisp = f"-"
        dis = "0.00 M"
        ndisp = f"VIEWING NONE"
        tdisp = "-.-.---:--"
        xoff = "-"
        yoff = "-"
        gdisp = "-"
    else:
        zdisp = f"x{zoom}"
        dis = (x2/s/2).to(u.au)
        if dis.round(3).value == 0:
            dis = dis.to(u.km)
            if dis.value < 10:
                dis = dis.to(u.m)
            dis = str(dis.round(2)).upper()
        else:
            dis = str(dis.round(3)).upper()
        ndisp = f"VIEWING {inp.describe().upper()}: {inp.name.upper()}"
        try:
            sep = 7
            tdisp = str(CLOCK_)
            tdisp = tdisp.zfill(sep+1)[0:-sep] + "." + tdisp[-sep:]
        except:
            tdisp = "-.----:--"
        gdisp = g

    ## DARK GRID
    if inp != None:
        # NextTick Grid: Horz
        img.create_line(0, h/2+1-o1, w+2,  h/2+1-o1, fill=colorTickGrid)
        img.create_line(0, h/2+1+o1, w+2,  h/2+1+o1, fill=colorTickGrid)
        # NextTick Grid: Vert
        img.create_line(w/2+1+o1,0, w/2+1+o1, h+2, fill=colorTickGrid)
        img.create_line(w/2+1-o1,0, w/2+1-o1, h+2, fill=colorTickGrid)
    else: # This is an EITHER/OR currently because I felt that having both cluttered the display too much, but its ez2revert
        # Dark Grid: Horz
        img.create_line(0,h/4+1, w+2, h/4+1, fill=colorDarkGrid)
        img.create_line(0,3*h/4+1, w+2, 3*h/4+1, fill=colorDarkGrid)
        # Dark Grid: Vert
        img.create_line(w/4+1,0, w/4+1, h+2, fill=colorDarkGrid)
        img.create_line(3*w/4+1,0, 3*w/4+1, h+2, fill=colorDarkGrid)
    # Dark Grid: Centers
    img.create_line(w/2+1,0, w/2+1, h+2, fill=colorCentGrid)
    img.create_line(0,h/2+1, w+2, h/2+1, fill=colorCentGrid)

    ## CORNERS
    # Scale
    img.create_rectangle(24,20,  24+x2,25,outline="white",fill="white") # Scale bar
    img.create_rectangle(20,20,  24,40,outline="white",fill="white") # Scale end: LEFT
    img.create_rectangle(x2+24,20,  x2+28,40,outline="white",fill="white") # Scale end: RIGHT
    img.create_rectangle(x2/2+19,20,  x2/2+21,35,outline="white",fill="white") # Scale center
    # Scale label
    img.create_text(x2/2+20, 50, fill="white", text=dis, font=tkFont.Font(family="xos4 Terminus",size=24))
    #img.create_text(x2/2+20, 50, fill="white", text="{0.value:0.003f} {0.unit}".format((x2/s/2).to(u.au)), font=tkFont.Font(family="xos4 Terminus",size=24))

    # Adjustment Display
    img.create_text(w-30, 30, fill="white", text=f"=ADJUST=\nMAG: {zdisp}\nX: {xoff}\nY: {yoff}\nG: {gdisp}", font=tkFont.Font(family="xos4 Terminus",size=24), justify=tkinter.RIGHT, anchor=tkinter.NE)

    # Subject Name
    img.create_text(w-30, h-30, fill="white", text=ndisp, font=tkFont.Font(family="xos4 Terminus",size=24), justify=tkinter.RIGHT, anchor=tkinter.SE)

    # Timestamp
    img.create_text(30, h-30, fill="white", text=f"TIME (GST): {tdisp}", font=tkFont.Font(family="xos4 Terminus",size=36), justify=tkinter.LEFT, anchor=tkinter.SW)



def DrawNothing(w=_OUTPUT[0]/0.79, h=_OUTPUT[1]/0.79):
    """Create a "loading screen" that is empty"""
    s = None
    offsetOne = 10
    gran = navGranularity

    tki = tkinter.Tk()
    img = tkinter.Canvas(tki, bg=colorScreen, width=w+2, height=h+2)
    img.create_rectangle(-w, -h, 2*w, 2*h, outline=colorScreen, fill=colorScreen)

    drawGRID(img, None, zoom=1, xoff=0, yoff=0, w=w, h=h, s=None, o1=10, g=navGranularity)

    # Screen Center Mark
    #drawDot(img, x=w/2+1, y=h/2+1, r=1, rgb="#ffffff")
    img.create_line(w/2+1,h/2-4, w/2+1, h/2+7, fill="#FFFFFF")
    img.create_line(w/2-4,h/2+1, w/2+7, h/2+1, fill="#FFFFFF")

    img.postscript(file="loadout.eps",colormode="color",width=w+2,height=h+2)
    tki.destroy()
    del tki

    # Now that we have a Starmap exported, apply a faux-CRT filter.
    gimpRender("loadout.eps","loadscreen")


def DrawMap(inp, zoom=1, xoff=0, yoff=0, w=_OUTPUT[0]/0.79, h=_OUTPUT[1]/0.79, doInit=True):
    #os.system("cp -f loadscreen.png sysdisplay.png")

    tki = tkinter.Tk()
    img = tkinter.Canvas(tki, bg=colorScreen, width=w+2, height=h+2)
    img.create_rectangle(-w, -h, 2*w, 2*h, outline=colorScreen, fill=colorScreen)

    if zoom < 1:
        zoom = 1
    s = getScale(w, h, inp)
    s = s*zoom

    if setGranularity > 0:
        gran = setGranularity
    else:
        try:
            gran = inp.localGranularity
        except:
            gran = navGranularity

    offsetOne = (350*zoom)/gran

    xoffZ = xoff*offsetOne
    yoffZ = yoff*offsetOne

    #img.create_line(w/2+1,h/2+1, w/2+1-xoffZ, h/2+1-yoffZ, fill=colorCenterTrace)

    drawGRID(img, inp, zoom, xoff, yoff, w, h, s, offsetOne, gran)
    drawSomething(img, inp, w+2, h+2, w/2+1-xoffZ, h/2+1-yoffZ, s, z=zoom)

    # Screen Center Mark
    #drawDot(img, x=w/2+1, y=h/2+1, r=1, rgb="#ffffff")
    img.create_line(w/2+1,h/2-4, w/2+1, h/2+7, fill="#FFFFFF")
    img.create_line(w/2-4,h/2+1, w/2+7, h/2+1, fill="#FFFFFF")

    img.postscript(file="tkout.eps",colormode="color",width=w+2,height=h+2)
    tki.destroy()
    del tki

    # Now that we have a Starmap exported, apply a faux-CRT filter.
    gimpRender("tkout.eps","sysdisplay")

#print("Done")
