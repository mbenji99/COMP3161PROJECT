import itertools
import names
import random

    
def getFirstNames():
    fNames = set()
    while len(fNames) < 317:
        if len(fNames) < 158:
            fNames.add(names.get_first_name(gender="male"))
        else:
            fNames.add(names.get_first_name(gender="female"))

    return list(fNames)

def getLastNames():
    lNames = set()
    while len(lNames) < 316:
        lNames.add(names.get_last_name())

    return list(lNames)


def getFullNames():
    fullNames = []
    fNames = getFirstNames()
    lNames = getLastNames()
    
    fullNames = [f"{fn} {ln}" for fn, ln in itertools.product(fNames, lNames)]
    
    random.shuffle(fullNames)
    return fullNames