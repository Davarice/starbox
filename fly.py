print("Loading StarBox...")
import cmd, sys

import collections
import astropy
from astropy import constants as c
from astropy import units as u

import starbox

#galaxy = [starbox.genSol(), starbox.genSol()]
#galaxy[1].name = "Alternate Sol"

galaxy = starbox.generate()
gst = 24568178.5
#galaxy.name = "Not Sol"

_PromptString = "\033[95m{u}@{h}\033[0m:\033[94m{p}\033[0m$ "

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
    npath = "~" + npath
    return npath.lower().replace(" ","_")

def PathToLoc(box, path):
    loc = box.loc
    if path == "":
        return loc
    lpath = path.split("/")
    tpath = lpath.copy()
    for jump in lpath: # For each number included in the path, try to go there
        try:
            dest = int(tpath.pop(0))
            nloc = loc.getSubs()[dest]
        except Exception as e: # Couldnt go there? Output as far as you got
            print(f"Could not navigate to {loc}[{jump}]")
            return loc
        else:
            loc = nloc
    return loc


class sbox(cmd.Cmd):
    host = "StarBox"
    intro = "StarBox loaded. For help: '?'"
    farewell = "System closing"

    def do_ls(self, line):
        """Print the accessible sublocations of the selected location"""
        try:
            print(PathToLoc(self, line).subList())
        except AttributeError as e:
            print("Error: Selected location ({}) has no sublocations ({})".format(loc, e))

    def do_info(self, line):
        """Info: Print information about the selected location"""
        try:
            print(PathToLoc(self, line).printData())
        except:
            print("Selected location ({}) is boring".format(self.loc))

    def do_exit(self, line):
        """Close system"""
        print(self.farewell)
        return True

    do_EOF = do_exit

class sbMain(sbox):
    """
    "Basic" context, contains navigation and identity tools
    """
    def __init__(self, user="Guest"):
        super().__init__()
        self.user = user
        self.loc = galaxy
        self.refreshPrompt()

    def precmd(self,line):
        print(f"\033[33mCurrent Time: {gst}\033[0m")
        return line

    def do_cd(self, line):
        """Change Directory: Navigate the viewer to a numeric destination
        (Numeric destinations can be found with ls)"""
        try:
            self.loc = PathToLoc(self, line)
        except:
            print("Error: Selected location ({}) has no sublocation [{}]".format(loc, line))
        self.refreshPrompt()

    def refreshPrompt(self):
        self.path = LocToPath(self.loc)
        self.prompt = _PromptString.format(u=self.user.lower(), h=self.host, p=self.path)

    def do_su(self, line):
        print("Switching user")
        newu = line.split(" ")[0]
        self.__init__(newu)


sbMain().cmdloop()




















