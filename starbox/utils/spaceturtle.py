print("    Loading SpaceTurtle...", end='')
from astropy import units as u
import os, tkinter, cmath, numpy
from tkinter import font as tkFont

_OUTPUT = [ 1280, 960 ] # Output resolution

"""
Rendering module for drawing starmaps
"""

# The operations which are done to a starmap in GIMP. Note that the format is Python 2.7.

                  # Init block
GimpOperations = ['img = pdb.gimp_file_load("tkout.eps", "tkout.eps")',
                  'drw = img.active_drawable',
                  'pdb.gimp_layer_add_alpha(drw)',

                  # Effect block
                  'pdb.plug_in_antialias(img, drw)',
                  'pdb.plug_in_pixelize2(img, drw, 2, 2)',
                  f'pdb.gimp_image_scale(img, {_OUTPUT[0]+2}, {_OUTPUT[1]+2})',
                  f'pdb.gimp_image_crop(img, {_OUTPUT[0]}, {_OUTPUT[1]}, 1, 1)',
                  #'pdb.plug_in_rgb_noise(img, drw, 1, 1, 0.2, 0.2, 0.2, 0)',
                  #'pdb.plug_in_hsv_noise(img, drw, 4, 3, 5, 20)',
                  'pdb.plug_in_softglow(img, drw, 50, 1, 1)',
                  'pdb.plug_in_video(img, drw, 1, 1, 0)',
                  'pdb.plug_in_lens_distortion(img, drw, 0, 0, 60, 6, 14, -22)',

                  # Export "block"
                  'pdb.file_png_save(img, drw, "sysdisplay.png", "sysdisplay.png", 0, 0, 0, 0, 0, 0, 0)']



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
    for p in loc.orbitals:
    #for p in loc.getSubs(par=False,syn=False):
        try:
            if p.posRho > extent:
                extent = p.posRho
        except:
            pass
    scale = limit/extent
    scale = scale/2
    #print(f"\nSCALE: {scale} = ({limit}/{extent})/2 = {scale.si}\n")
    return scale





def drawDot(c, x, y, r, rgb="#555"):
    #print("Drawing dot")
    x0 = x - r
    x1 = x + r
    y0 = y - r
    y1 = y + r
    c.create_oval(x0, y0, x1, y1, outline=rgb, fill=rgb)


def drawCircle(c, x, y, r, rgb="#444"):
    #print("Drawing circle")
    x0 = x - r
    y0 = y - r

    x1 = x + r
    y1 = y + r
    c.create_oval(x0, y0, x1, y1, outline=rgb)


def drawSystem(c, loc, w, h, x, y, s, color="#fc8", norb=True, z=1):
    for obj in loc.orbitals:
        if obj.bodyType != "Belt":
            drawCircle(c, x, y, s*obj.posRho)
            cart = cmath.rect(obj.posRho*s, obj.posPhi)
            if loc.bodyType == "System":
                drawSystem(c, obj, w, h, x+cart.real, y+cart.imag, s, norb=True, z=z)#*10)
            else:
                drawSystem(c, obj, w, h, x+cart.real, y+cart.imag, s, norb=False, z=z)#*10)
    try:
        for obj in loc.core:
            drawDot(c, x, y, (limit/45)*numpy.cbrt(z), rgb=color)
    except AttributeError:
        drawDot(c, x, y, (limit/60)*numpy.cbrt(z), rgb=loc.color) #colors[loc.composition.lower()])
        if norb:
            c.create_text(x+10,y+10*numpy.cbrt(z), fill="white", text=loc.name, font=tkFont.Font(family="xos4 Terminus",size=18))
        #print(f"Drawing {loc.name} at ({x},{y}) with a radius of {limit/60}")
    except:
        pass


def DrawMap(inp, zoom=1, xoff=0, yoff=0, w=_OUTPUT[0], h=_OUTPUT[1], doInit=True):
    #os.system("cp -f loadscreen.png sysdisplay.png")

    tki = tkinter.Tk()
    img = tkinter.Canvas(tki, bg="#222", width=w+2, height=h+2)
    img.create_rectangle(-w, -h, 2*w, 2*h, outline="#222", fill="#242420")

    s = getScale(w, h, inp)
    s = s*zoom

    #xoff = (xoff/w)*zoom

    x2 = w/3

    img.create_rectangle(20,20,  x2+20,25,outline="white",fill="white") # Scale bar
    img.create_rectangle(20,20,  24,40,outline="white",fill="white") # Scale end: LEFT
    img.create_rectangle(x2+15,20,  x2+20,40,outline="white",fill="white") # Scale end: RIGHT
    img.create_rectangle(x2/2+19,20,  x2/2+21,35,outline="white",fill="white") # Scale center

    img.create_text(x2/2+20, 50, fill="white", text="{0.value:0.003f} {0.unit}".format((x2/s/2).to(u.au)), font=tkFont.Font(family="xos4 Terminus",size=24,weight="bold"))

    drawSystem(img, inp, w+2, h+2, w/2-xoff, h/2+yoff, s, z=zoom)
    img.postscript(file="tkout.eps",colormode="color",width=w+2,height=h+2)
    #tki.destroy()

    # Now that we have a Starmap exported, apply a faux-CRT filter.
    gstring = "gimp -idf --batch-interpreter=python-fu-eval -b '"
    for line in GimpOperations:
        gstring = gstring + line + "; "
    gstring = gstring + "gimp.exit()' >/dev/null 2>/dev/null"
    os.system(gstring)

print("Done")

