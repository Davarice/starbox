print("Loading StarBox...")
print("Importing core modules...")
import cmd, sys, re
print(" Core modules imported")

#print("Importing secondary modules...")
#import collections
#import astropy
#from astropy import constants as c
#from astropy import units as u
#print(" Secondary modules imported")

print("Importing primary functions...")
import starbox
print(" Primary functions imported")

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

space = starbox.starstuff.generate() # TODO: replace these two lines with a load function
try:
    gst = space.TIME
except:
    gst = 24568125

_PromptString = "{c}{u}@{h}\033[0m:\033[94m{p}\033[0m$ "

def LocToPath(loc):
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


class sbox(cmd.Cmd):
    host = "StarBox.core"
    intro = "StarBox fully initialized. For help: 'help' or '?'"
    farewell = "StarBox powering down...\nRemoving all sapients...\nVirtual universe purged.\nInterface closing."
    root = space
    promptColor = "\033[95m"

    def __init__(self, user="User"):
        super().__init__()
        self.user = user
        self.loc = self.root
        self.refreshPrompt()

    def interject(self, content, resume=""):
        self.stdout.write(f"\n{content}\n{self.prompt}{resume}")

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

    def complete_none(self, text, line, begidx, endidx):
        return []

    def do_ls(self, line):
        """Print the accessible sublocations of the selected location"""
        try:
            loc = PathToLoc(self, line)
            print(loc.subList())
        except AttributeError as e:
            print("Error: Selected location ({}) has no sublocations ({})".format(loc, e))

    complete_ls = completePATHING

    complete_info = completePATHING

    def default(self, line):
        if "EOF" in line:
            print("")
            return self.do_exit(line)
        print(f"ERROR: Command '{line.split()[0]}' unknown")

    def do_exit(self, line):
        """Close current context and return to outer shell, if any"""
        print(f"{self.farewell}")
        return True

    complete_exit = complete_none

    def emptyline(self):
        pass

    def refreshPrompt(self):
        self.path = LocToPath(self.loc)
        self.prompt = _PromptString.format(c=self.promptColor, u=self.user.lower(), h=self.host, p=self.path)


"""
### ### ### ### ### ### ### ###
END OF CORE CONTEXT
From this point on, contextual commands only
### ### ### ### ### ### ### ###
"""


class sbWep(sbox):
    """
    Weaponry context, for configuration of small arms
    """
    host = "StarBox.wepn"
    intro = "WEAPONRY subcontext loaded."
    promptColor = "\033[93m" # Yellow prompt for weapons mode
    farewell = "Weaponry mode closing..."





class sbVeh(sbox):
    """
    Vehicle context, for configuration of surface craft and voidcraft
    """
    host = "StarBox.vhcl"
    intro = "VEHICLULAR subcontext loaded."
    promptColor = "\033[96m" # Cyan prompt for vehicular mode
    farewell = "Vehicular mode closing..."





class sbEDIT(sbox):
    """
    World editing context. Allows MODIFICATION AND SAVING of game world. Dangerous.
    """
    host = "StarBox.EDIT"
    intro = "\033[91mEDITOR\033[0m subcontext loaded."
    promptColor = "\033[91m" # RED prompt for VERY DANGEROUS mode
    farewell = "EDITOR mode closing..."





class sbMain(sbox):
    """
    "Basic" context, contains navigation and identity tools
    """
    host = "StarBox.main"

    #def postcmd(self, stop, line):
        #if stop != True:
            #print(f"\033[33mCurrent Time: {gst}\033[0m")
        #return stop

    def do_cd(self, line):
        """Change Directory: Navigate the viewer to a numeric destination
        (Numeric destinations can be found with 'ls')"""
        try:
            self.loc = PathToLoc(self, line)
        except:
            print("Error: Selected location ({}) has no sublocation [{}]".format(loc, line))
        self.refreshPrompt()

    def do_info(self, line):
        """Info: Print information about the selected location"""
        try:
            loc = PathToLoc(self, line)
            starbox.spaceturtle.DrawMap(loc)
            print(loc.printData())
        except:
            print("Selected location ({}) is boring".format(loc))

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

try:
    sbMain().cmdloop()
except KeyboardInterrupt:
    print("\nStarBox Vaporized")
    pass
