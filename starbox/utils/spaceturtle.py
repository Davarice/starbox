#print("    Loading SpaceTurtle...", end='')
from astropy import units as u
from tkinter import font as tkFont
import os, tkinter, cmath, numpy

# Common CRT display resolutions
RESOLUTIONS = [[640,480],
               [800,600],
               [1024,768],
               [1200,900],
               [1280,960],
               [1600,1200]]

# Output resolution (The resolution of CRT display to be simulated)
_OUTPUT = RESOLUTIONS[4]

# The density of the grid of viewable locations
navGranularity = 400
setGranularity = 0

CLOCK_ = None

"""
Rendering module for drawing starmaps
"""

# The operations which are done to a starmap in GIMP. Note that the format is Python 2.7.
#   >>> a1.layers
#   [<gimp.Layer 'red'>, <gimp.Layer 'green'>, <gimp.Layer 'blue'>]

                  # Source block
#GimpOperations = ['img = pdb.gimp_file_load("tkout.eps", "tkout.eps")',
GimpOperations = ['img = pdb.gimp_file_load("{i}", "{i}")',
                  'drw = img.active_drawable',
                  'pdb.gimp_layer_add_alpha(drw)',

                  # Signal block
                  'pdb.plug_in_antialias(img, drw)',
                  #'pdb.plug_in_pixelize2(img, drw, 2, 2)',
                  f'pdb.gimp_image_scale(img, {_OUTPUT[0]+4}, {_OUTPUT[1]+4})',
                  f'pdb.gimp_image_crop(img, {_OUTPUT[0]}, {_OUTPUT[1]}, 2, 2)',
                  #'pdb.plug_in_softglow(img, drw, 50, 1, 1)',

                  # Chromatic block
                  'a1, _, _, _ = pdb.plug_in_decompose(img, drw, "RGB", 1)',
                  '[lred, lgrn, lblu] = a1.layers', # Split it into R/G/B (I only use R here but dat utility)
                  'pdb.plug_in_gauss_rle2(a1, lred, 4, 3)',# Very slightly defocus the red channel (in 4:3 of course)
                  'pdb.plug_in_mblur_inward(a1, lred, 2, 4, 45, {w}, {h})', # Bleed it into the glass
                  'pdb.plug_in_recompose(a1, None)', # ~$ git commit -a

                  # Screen block
                  'pdb.plug_in_softglow(img, drw, 30, 1, 1)',
                  'pdb.plug_in_video(img, drw, 5, 1, 0)',
                  'pdb.plug_in_lens_distortion(img, drw, 0, 0, 60, 6, 14, -8)',

                  # Export "block"
                  'pdb.file_png_save(img, drw, "{o}.png", "{o}.png", 0, 9, 0, 0, 0, 0, 0)']
                  #'pdb.file_png_save(img, drw, "sysdisplay.png", "sysdisplay.png", 0, 9, 0, 0, 0, 0, 0)']



colors = {"rock":"#373","gas":"#bb4","ice":"#99f"}

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
    if len(loc.orbitals) > 0:
        for p in loc.orbitals:
        #for p in loc.getSubs(par=False,syn=False):
            try:
                if p.posRho > extent:
                    extent = p.posRho
            except:
                pass
    else:
        extent = loc.radius * 3
    scale = limit/extent
    scale = scale/2
    #print(f"\nSCALE: {scale} = ({limit}/{extent})/2 = {scale.si}\n")
    return scale


def getRenderRadius(obj,s):
    r = obj.radius*s # The actual onscreen size of the object
    m = obj.minSize # The minimum size of the object according to its type
    if numpy.greater(m,r): # Return the larger of the two
        return m
    else:
        return r


def drawDot(c, x, y, r, rgb="#888"):
    #print("Drawing dot")
    x0 = x - r
    x1 = x + r

    y0 = y - r
    y1 = y + r
    c.create_oval(x0, y0, x1, y1, outline=rgb, fill=rgb)


def drawCircle(c, x, y, r, rgb="#555"):
    #print("Drawing circle")
    r = r * 0.99999
    x0 = x - r
    y0 = y - r

    x1 = x + r
    y1 = y + r
    c.create_oval(x0, y0, x1, y1, outline=rgb)


def drawSomething(c, loc, w, h, x, y, s, color="#fe4", direct=True, z=1):
    for obj in loc.orbitals:
        if obj.bodyType != "Belt":
            drawCircle(c, x, y, s*obj.posRho)
            cart = cmath.rect(obj.posRho*s, obj.posPhi)
            drawSomething(c, obj, w, h, x+cart.real, y+cart.imag, s, direct=False, z=z)
    try:
        for obj in loc.core:
            drawDot(c, x, y, getRenderRadius(obj,s), rgb=loc.color) # previously (limit/45)*numpy.cbrt(z)
    except AttributeError:
        drawDot(c, x, y, getRenderRadius(loc,s), rgb=loc.color) #colors[loc.composition.lower()])
        if direct:
            c.create_text(x,y+15+getRenderRadius(loc,s), fill="white", text=loc.name, font=tkFont.Font(family="xos4 Terminus",size=18))
        #print(f"Drawing {loc.name} at ({x},{y}) with a radius of {limit/60}")
    except:
        pass




def drawGRID(img, inp, zoom, xoff, yoff, w, h, s, o1, g):
    x2 = w/3

    ## DARK GRID
    ## Dark Grid: Horz
    #img.create_line(w/4+1,0, w/4+1, h+2, fill="#282828")
    #img.create_line(3*w/4+1,0, 3*w/4+1, h+2, fill="#282828")
    ## Dark Grid: Vert
    #img.create_line(0,h/4+1, w+2, h/4+1, fill="#282828")
    #img.create_line(0,3*h/4+1, w+2, 3*h/4+1, fill="#282828")

    # Dark Grid: Centers
    img.create_line(w/2+1,0, w/2+1, h+2, fill="#333333")
    img.create_line(0,h/2+1, w+2, h/2+1, fill="#333333")

    # NextTick Grid: Horz
    img.create_line(w/2+1+o1,0, w/2+1+o1, h+2, fill="#4c4c4c")
    img.create_line(w/2+1-o1,0, w/2+1-o1, h+2, fill="#4c4c4c")
    # NextTick Grid: Vert
    img.create_line(0, h/2+1+o1, w+2,  h/2+1+o1, fill="#4c4c4c")
    img.create_line(0, h/2+1-o1, w+2,  h/2+1-o1, fill="#4c4c4c")


    ## CORNERS
    # Scale
    img.create_rectangle(24,20,  24+x2,25,outline="white",fill="white") # Scale bar
    img.create_rectangle(20,20,  24,40,outline="white",fill="white") # Scale end: LEFT
    img.create_rectangle(x2+24,20,  x2+28,40,outline="white",fill="white") # Scale end: RIGHT
    img.create_rectangle(x2/2+19,20,  x2/2+21,35,outline="white",fill="white") # Scale center

    # Scale label
    dis = (x2/s/2).to(u.au)
    if dis.round(3).value == 0:
        dis = dis.to(u.km)
        if dis.value < 10:
            dis = dis.to(u.m)
        dis = str(dis.round(2)).upper()
    else:
        dis = str(dis.round(3)).upper()
    img.create_text(x2/2+20, 50, fill="white", text=dis, font=tkFont.Font(family="xos4 Terminus",size=24))
    #img.create_text(x2/2+20, 50, fill="white", text="{0.value:0.003f} {0.unit}".format((x2/s/2).to(u.au)), font=tkFont.Font(family="xos4 Terminus",size=24))

    # Adjustment Display
    img.create_text(w-30, 30, fill="white", text=f"=ADJUST=\nMAG: x{zoom}\nX: {xoff}\nY: {yoff}\nG: {g}", font=tkFont.Font(family="xos4 Terminus",size=24), justify=tkinter.RIGHT, anchor=tkinter.NE)

    # Subject Name
    img.create_text(w-30, h-30, fill="white", text=f"VIEWING {inp.describe().upper()}: {inp.name.upper()}", font=tkFont.Font(family="xos4 Terminus",size=24), justify=tkinter.RIGHT, anchor=tkinter.SE)

    # Timestamp
    try:
        tdisp = str(CLOCK_)#.TIME#.timeString
    except:
        tdisp = "00:00"
    img.create_text(30, h-30, fill="white", text=f"TIME (GST): {tdisp}", font=tkFont.Font(family="xos4 Terminus",size=36), justify=tkinter.LEFT, anchor=tkinter.SW)



def gimpRender(i,o,w=_OUTPUT[0],h=_OUTPUT[1]):
    gstring = "gimp -idf --batch-interpreter=python-fu-eval -b '"
    for line in GimpOperations:
        gstring = gstring + line.format(w=w/2,h=h/2,i=i,o=o) + "; "
    gstring = gstring + "gimp.exit()' >/dev/null 2>/dev/null"
    os.system(gstring)



def DrawMap(inp, zoom=1, xoff=0, yoff=0, w=_OUTPUT[0], h=_OUTPUT[1], doInit=True):
    #os.system("cp -f loadscreen.png sysdisplay.png")

    tki = tkinter.Tk()
    img = tkinter.Canvas(tki, bg="#222", width=w+2, height=h+2)
    img.create_rectangle(-w, -h, 2*w, 2*h, outline="#222", fill="#222420")

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

    img.create_line(w/2+1,h/2+1, w/2+1-xoffZ, h/2+1-yoffZ, fill="#333333")
    drawGRID(img, inp, zoom, xoff, yoff, w, h, s, offsetOne, gran)
    drawSomething(img, inp, w+2, h+2, w/2+1-xoffZ, h/2+1-yoffZ, s, z=zoom)

    # Screen Center Mark
    #drawDot(img, x=w/2+1, y=h/2+1, r=1, rgb="#ffffff")
    img.create_line(w/2+1,h/2-4, w/2+1, h/2+6, fill="#FFFFFF")
    img.create_line(w/2-4,h/2+1, w/2+6, h/2+1, fill="#FFFFFF")

    img.postscript(file="tkout.eps",colormode="color",width=w+2,height=h+2)
    #tki.destroy()

    # Now that we have a Starmap exported, apply a faux-CRT filter.
    gimpRender("tkout.eps","sysdisplay")

#print("Done")

