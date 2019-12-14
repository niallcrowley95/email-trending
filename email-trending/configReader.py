import json


def readFile(location):
    with open(location) as handle:
        dictdump = json.loads(handle.read())
    return dictdump
