import colored_traceback.auto

print("Loading StarBox...")

#print("Importing system modules...", end='')
import cmd, sys, re
from multiprocessing import Process as mproc
#print("Done")

#print("Importing core modules...")
import starbox
import timegem

CLOCK_ = timegem.Clock(24568125.75) # Generate a universal clock
starbox.utils.spaceturtle.CLOCK_ = CLOCK_

# Assign the universal clock to any classes that need to access it
starbox.starstuff.world.Site.Clock = CLOCK_
#starbox.starstuff.world.Station.Clock = CLOCK_

#starbox.starstuff.celestial.Body.Clock = CLOCK_
#starbox.starstuff.celestial.Grouping.Clock = CLOCK_

#print(" Core modules imported")

"""
MAIN USER INTERFACE MODULE

ALL actions taken by users are controlled from this file
Core commands, available in all contexts, are defined in the 'sbox' class
Subsequent subclasses are invoked for specific contexts (including the default context)
    sbMain: Default context; Navigate and view the world like a file browser
    sbWep: Weaponry context; Navigate, configure, and test small arms
    sbVeh: Vehicular context; Navigate, configure, and test vehicles
    sbEDIT: EDITOR context; Default context with ultimate power; ### DANGER ###

Utility functions imminently below
"""

space = starbox.starstuff.generate() # TODO: replace these lines with a load function
#space = starbox.utils.stario.load("MilkyWay")
space.Clock = CLOCK_
CLOCK_.update(space)

#print("Finalizing...")

_PromptString = "{c}{u}@{h}\033[0m:\033[94m{p}\033[0m$ "

def StringToTime(sl):
    s = ""
    for w in sl:
        s = s + w.lower()
    t = 0 * timegem.u.minute

    comp = re.findall(r'\d*:\d{2}', s)
    hour = re.findall(r'\d+(?=(?:h|hour|hr))', s)
    mins = re.findall(r'\d+(?=(?:m|minute|min))', s)

    for c in comp:
        c2 = c.split(":")
        if c2[0] == "":
            c0 = 0*timegem.u.hour
        else:
            c0 = int(c2[0])*timegem.u.hour
        c1 = int(c2[1])*timegem.u.minute
        t = t + c0 + c1
    for h in hour:
        t = t+float(h)*timegem.u.hour
    for m in mins:
        t = t+float(m)*timegem.u.minute
    return t

def LocToPath(loc):
    if loc == None:
        return "~/"
    tloc = loc
    npath = ""
    while tloc != None:
        try:
            tname = tloc.name
            npath = "/" + tname + npath
            tloc = tloc.parent
        except AttributeError:
            tloc = None
            pass
    return npath.lower().replace(" ","_")

def PathToLoc(box, path, loc=None):
    if loc == None:
        loc = box.loc
    if path == "":
        return loc
    lpath = path.split("/")
    tpath = lpath.copy()
    if tpath[0] == "":
        loc = box.root
        tpath.remove("")
    for jump in lpath: # For each number included in the path, try to go there
        try:
            if tpath[0] != "":
                dest = int(tpath.pop(0))
                nloc = loc.getSubs()[dest]
            else:
                nloc = loc
        except Exception as e: # Couldnt go there? Output as far as you got
            break
        else:
            loc = nloc
    return loc

def isInt(check, alt=0):
    try: 
        x = int(check)
        return x # If the value being checked can be an integer, return the integer
    except ValueError:
        return alt # If it cannot, return the alternative

# Core functions for ALL StarBox contexts
class sbCORE(cmd.Cmd):
    host = "StarBox.core"
    intro = "StarBox fully initialized. For help: 'help' or '?'"
    farewell = "StarBox powering down...\nRemoving all sapients...\nVirtual universe purged.\nInterface closing."
    root = space
    promptColor = "\033[95m"

    def __init__(self, user="User"):
        super().__init__()
        self.user = user
        self.doShowTime = False
        try:
            self.loc = self.root
        except:
            self.loc = None
        self.refreshPrompt()

    def interject(self, content, resume=""):
        self.stdout.write(f"\n{content}\n{self.prompt}{resume}")

    def default(self, line):
        if "EOF" in line:
            print("")
            return self.do_exit(line)
        print(f"ERROR: Command '{line.split()[0]}' unknown")

    def complete_none(self, text, line, begidx, endidx):
        return []

    def do_exit(self, line):
        """Close current context and return to outer shell, if any"""
        print(f"{self.farewell}")
        return True

    complete_exit = complete_none

    def emptyline(self):
        pass

    def showTime(self):
        print(f"\033[33mCurrent Time [GST]: \033[93m{CLOCK_.toaster()}\033[0m")

    def postcmd(self, stop, line):
        if stop != True:# and self.doShowTime == True:
            self.showTime()
        self.refreshPrompt()
        return stop

    def refreshPrompt(self):
        self.path = LocToPath(self.loc)
        self.prompt = _PromptString.format(c=self.promptColor, u=self.user.lower(), h=self.host, p=self.path)


# Navigational functions for space-oriented contexts
class sbNav(sbCORE):

    ## Autocomplete using available options from the world
    def completePATHING(self, text, line, begidx, endidx):
        full = line.split(" ")
        full.pop(0) # 0 is the command itself; gtfo
        vloc = self.loc
        lret = []
        for sec in full: # Do it on every argument, but only output for the last
            if re.match('^[\d/]*$', sec) != None and re.match('.*\d$', sec) == None:
                if sec.startswith("/"):
                    vloc = root
                sec = sec.strip("/")
                subsec = sec.split("/")
                for rnum in subsec:
                    vloc = PathToLoc(self, rnum, vloc)
                lret = vloc.getSubs() # list return
        nret = list(range(len(lret))) # numbers return
        if nret != []:
            self.interject(str(nret)[1:-1],line)
        return

    complete_cd = completePATHING
    complete_ls = completePATHING
    complete_info = completePATHING

    def do_ls(self, line):
        """Print the accessible sublocations of the selected location"""
        try:
            loc = PathToLoc(self, line)
            print(loc.subList())
        except AttributeError as e:
            print("Error: Selected location ({}) has no sublocations ({})".format(loc, e))


"""
### ### ### ### ### ### ### ###
END OF CORE CONTEXT
From this point on, contextual commands only
### ### ### ### ### ### ### ###
"""


class sbEditorInterface(sbCORE):
    """
    Direct editing mode
    """
    host = "StarBox.wepn.intr"
    intro = None
    promptColor = "\033[91m" # Red prompt for slightly dangerous mode
    farewell = None

    def __init__(self, parent, loc):
        super().__init__()
        self.user = user
        self.loc = None
        self.refreshPrompt()




class sbWep(sbNav):
    """
    Weaponry context, for configuration of small arms
    """
    host = "StarBox.wepn"
    intro = "WEAPONRY subcontext loaded."
    promptColor = "\033[93m" # Yellow prompt for weapons mode
    farewell = "Weaponry mode closing..."





class sbVeh(sbNav):
    """
    Vehicle context, for configuration of surface craft and voidcraft
    """
    host = "StarBox.vhcl"
    intro = "VEHICLULAR subcontext loaded."
    promptColor = "\033[36m" # Cyan prompt for vehicular mode
    farewell = "Vehicular mode closing..."





class sbMain(sbNav):
    """
    "Basic" context, contains navigation and identity tools
    """
    host = "StarBox.main"
    doShowTime=True

    def do_cd(self, line):
        """Change Directory: Navigate the viewer to a numeric destination
        (Numeric destinations can be found with 'ls')"""
        try:
            self.loc = PathToLoc(self, line)
        except:
            print("Error: Selected location ({}) has no sublocation [{}]".format(loc, line))
        self.refreshPrompt()

    def do_gset(self, line):
        """Change the coordinate granularity of the MAP command
        0 to reset to default"""
        try:
            starbox.utils.spaceturtle.setGranularity = int(line)
            print("Successfully adjusted")
        except Exception as e:
            print(f"Could not adjust! {e}")

    def do_mapload(self, line):
        mproc(target=starbox.utils.spaceturtle.DrawNothing).start()

    def do_map(self, line):
        """MAP: Print information about the selected location.
Syntax: 'map [Z] [X] [Y]'
    Z: Zoom coefficient; Increase the scale of objects on the display.
        Default: 1
    X: Horizontal offset; For panning the display East and West.
        Default: 0
    Y: Vertical offset; For panning the display South and North.
        Default: 0"""
        spline = line.split(" ") + ["","",""]
        #loc = PathToLoc(self, spline[0])
        loc = self.loc
        CLOCK_.update(loc)
        zoom = isInt(spline[0],1)
        xoff = isInt(spline[1],0)
        yoff = isInt(spline[2],0)
        mproc(target=starbox.utils.spaceturtle.DrawMap,args=(loc,zoom,xoff,yoff,)).start()

    def do_time(self, line):
        full = line.lower().split(" ")
        subc1 = full.pop(0)
        if subc1 == "":
            print(CLOCK_)
        elif subc1 == "increment":
            t = StringToTime(full)
            if input(f"Move time FORWARDS by {t}? New time will be {CLOCK_.toaster(plus=t)} (y/N): ").lower() == "y":
                CLOCK_.tick(t)
                print("Time has progressed.")
            else:
                print("Time remains unmoved.")
        elif subc1 == "decrement":
            t = StringToTime(full)
            if input(f"Move time BACKWARDS by {t}? New time will be {CLOCK_.toaster(plus=-t)} (y/N): ").lower() == "y":
                CLOCK_.tick(-t)
                print("Time has regressed.")
            else:
                print("Time remains unmoved.")
        elif subc1 == "marker" and input("asdf? ") == "qwert":
            pass
        #elif subc1 == "":
            #pass
        else:
            print(f"Unknown subcommand '{subc1}'")

    def complete_time(self, text, line, begidx, endidx):
        if line.strip().lower() == "time " + text:
            ret = []
            for possible in ["increment","decrement","marker"]:
                if possible.startswith(text):
                    ret.append(possible)
            return ret
        return

    def do_info(self, line):
        """INFO: Print information about the selected location.
Syntax: 'info [L]'
    L: The hierarchy path to examine.
        Default: Current Location"""

        #try:
            #loc = PathToLoc(self, line)
            #print(loc.printData())
        #except Exception as e:
            #print("Selected location ({}) is boring [{}]".format(loc,e))
        loc = PathToLoc(self, line)
        print(loc.printData())

    def do_load(self, line):
        """Load saved state: Initialize a universe that was previously saved to disk"""
        try:
            imp = starbox.utils.stario.load(line)
            CLOCK_=imp.Clock
            space = imp
            self.root = space
            self.loc = space
        except FileNotFoundError:
            print("Failed to load '{}': Saved instance does not exist.".format(line))
        except TypeError:
            print("Failed to load '{}': Saved instance may be corrupted.".format(line))
        except Exception as e:
            print("Failed to load '{}': {}".format(line, e))
        else:
            print("Saved world loaded.")

    #def do_time(self, line):
        #pass

    #def help_navigation(self, line):
        #print("")


    #def do_vehicles(self, line):
        #"""Enter VEHICULAR mode:
#View, configure, and test transportation vessels"""
        #print("Entering subcontext...")
        #sbWep(self.user).cmdloop()
        #print("Returning to standard context")
    #do_vh = do_vehicles # Alias


    def do_weaponry(self, line):
        """Enter WEAPONS mode:
View, configure, and test small arms"""
        print("Entering subcontext...")
        sbWep(self.user).cmdloop()
        print("Returning to standard context")
    do_wp = do_weaponry # Alias


    def do_edit(self, line):
        """Enter EDITOR mode:
Full control over game world"""
        if self.user != "root":
            print("\033[91mAccess Denied\033[0m")
            return
        print("Entering subcontext...")
        sbEDIT(self.user).cmdloop()
        print("Returning to standard context")

    def do_su(self, line):
        """Switch User
For now this simply changes the username..."""
        print("Switching user")
        newu = line.split(" ")[0]
        self.__init__(newu)

    def default(self, line):
        if "EOF" in line:
            print("")
            return #self.do_exit(line) # In MAIN context, do not allow Ctrl-D exiting
        print(f"ERROR: Command '{line.split()[0]}' unknown")





class sbEDIT(sbMain):
    """ # DANGER #
    World editing context. Allows MODIFICATION AND SAVING of game world. Dangerous.
    """ # DANGER #
    host = "StarBox.EDIT"
    intro = "\033[91mEDITOR\033[0m subcontext loaded."
    promptColor = "\033[31m" # RED prompt for VERY DANGEROUS mode
    farewell = "EDITOR mode closing..."

    def __init__(self, user="ROOT"):
        super().__init__(user=user)
        self.doShowTime = True
        self.showTime()
        #del self.do_vehicles
        #del self.do_vh
        #del self.do_weaponry
        #del self.do_wp

    def do_save(self, line):
        """Save to disk: Serialize the current universe and save it as a file."""
        if input(f"Save '{self.root.name} ({self.root.bodyType})' to disk? It would be saved as 'data/{starbox.utils.stario.getfile(self.root.name)}'.\n(y/N) ").lower() != "y":
            print("Cancelled.")
            return
        try:
            starbox.utils.stario.save(self.root)
        except Exception as e:
            print("Failed to save '{}': {}".format(line, e))
        else:
            print("Saved world to disk.")

    def do_new(self, name):
        pass

    # This power-class builds atop all the cool stuff in the sbMain, but should still exit on ctrl-D.
    default = sbCORE.default # So we grab it from the sbCORE.

    # END DANGER #



sbterm = sbMain()

def sbrun():
    try:
        sbMain().cmdloop()
    except KeyboardInterrupt:
        print("\nStarBox Vaporized")
        pass

if __name__ == "__main__":
    sbrun()
