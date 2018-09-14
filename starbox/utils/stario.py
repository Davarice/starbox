#print("    Loading StarIO...", end='')
import pickle,sys

"""
### TODO ###
Stub module for loading and saving worlds as objects
"""

def getfile(inp):
    """Return a string representing what WOULD be the saved filename if the input string were the name of an object being pickled.
*This does NOT include the 'data/' segment of the path."""
    return f"{inp.lower().replace(' ','')}.pkl"


def load(name):
    return pickle.load(open(f"data/{getfile(name)}","rb"))


def save(obj):
    pickle.dump(obj, open(f"data/{getfile(obj.name)}","wb"))



#print("Done")
