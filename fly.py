import cmd, sys

import collections
import astropy
from astropy import constants as c
from astropy import units as u

import starbox

#galaxy = [starbox.genSol(), starbox.genSol()]
#galaxy[1].name = "Alternate Sol"

galaxy = starbox.genSol()
galaxy.name = "Not Sol"

_PromptString = "\033[95m{u}@{h}\033[0m:\033[94m{p}\033[0m$ "

def LocToPath(loc):
    return "~"

class sbox(cmd.Cmd):
    host = "StarBox"
    intro = "StarBox loaded. For help: '?'"
    farewell = "System closing"

    def do_ls(self, line):
        """Print the accessible sublocations of your current location"""
        try:
            print(self.loc.subList())
        except AttributeError:
            print("Error: Current location {} has no sublocations".format(self.loc))

    def do_cd(self, line):
        """Change Directory: Navigate the viewer to a numeric destination
        (Numeric destinations can be found with ls)"""
        try:
            dest = int(line)
            self.loc = self.loc.getSubs()[dest]
        except:
            print("Error: Current location {} has no sublocation [{}]".format(self.loc, line))

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
        self.loc = galaxy.heads[0]
        self.refreshPrompt()

    def refreshPrompt(self):
        self.path = LocToPath(self.loc)
        self.prompt = _PromptString.format(u=self.user.lower(), h=self.host, p=self.path)

    def do_su(self, line):
        print("Switching user")
        newu = line.split(" ")[0]
        self.__init__(newu)


sbMain().cmdloop()
















