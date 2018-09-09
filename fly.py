print("Loading StarBox...")
#import cmd2 as cmd, sys
import cmd, sys, re

import collections
import astropy
from astropy import constants as c
from astropy import units as u

import starbox

root = starbox.generate()
gst = 24568178.5

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
    #npath = "~" + npath
    return npath.lower().replace(" ","_")

def PathToLoc(box, path, loc=None):
    if loc == None:
        loc = box.loc
    if path == "":
        return loc
    lpath = path.split("/")
    tpath = lpath.copy()
    if tpath[0] == "":
        loc = root
        tpath.remove("")
    for jump in lpath: # For each number included in the path, try to go there
        try:
            if tpath[0] != "":
                dest = int(tpath.pop(0))
                nloc = loc.getSubs()[dest]
            else:
                nloc = loc
        except Exception as e: # Couldnt go there? Output as far as you got
            #print(f"Could not navigate to {loc}[{jump}]")
            break
            #return loc
        else:
            loc = nloc
    return loc


class sbox(cmd.Cmd):
    host = "StarBox"
    intro = "StarBox loaded. For help: '?'"
    farewell = "StarBox powering down...\nRemoving all sapients...\nVirtual universe purged.\nInterface closing."

    def __init__(self, user="Guest"):
        super().__init__()
        self.user = user
        self.loc = root
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

    def do_info(self, line):
        """Info: Print information about the selected location"""
        try:
            loc = PathToLoc(self, line)
            print(loc.printData())
        except:
            print("Selected location ({}) is boring".format(loc))

    complete_info = completePATHING

    def default(self, line):
        if "EOF" in line:
            print("")
            return #self.do_exit(line)
        print(f"ERROR: Command '{line.split()[0]}' unknown")

    def do_exit(self, line):
        """Close StarBox and return to outer shell, if any"""
        print(f"{self.farewell}")
        return True

    complete_exit = complete_none

    def emptyline(self):
        pass

    def refreshPrompt(self):
        self.path = LocToPath(self.loc)
        self.prompt = _PromptString.format(u=self.user.lower(), h=self.host, p=self.path)





class sbMain(sbox):
    """
    "Basic" context, contains navigation and identity tools
    """

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

    def help_science(self, line):
        print("asdfqwert")

    #def do_science(self, line):
        

    def do_su(self, line):
        """Switch User"""
        print("Switching user")
        newu = line.split(" ")[0]
        self.__init__(newu)

try:
    sbMain().cmdloop()
except KeyboardInterrupt:
    print("")
    pass
