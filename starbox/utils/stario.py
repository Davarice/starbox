print("    Loading StarIO...")
import pickle,sys

"""
### TODO ###
Stub module for loading and saving worlds as objects
"""

def load(name):
    return pickle.load(open(f"data/{name.lower().replace(' ','')}.pkl","rb"))


def save(obj):
    pickle.dump(obj, open(f"data/{obj.name.lower().replace(' ','')}.pkl","wb"))



print("     StarIO Loaded")
