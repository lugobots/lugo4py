from .protos import physics_pb2
from typing import Tuple
from math import hypot

def NewVector(fromPoint , toPoint) :
    v = ()
    v[0] = toPoint[0] - fromPoint[0]
    v[1] = toPoint[1] - fromPoint[1]
    if isInValidateVector(v):
        raise RuntimeError("A vector cannot have zero length")
    return v

def normalize(v):
    length = len(v)
    return getScaledVector(v, 100 / length)

def getLength(v):
    return hypot(v)

def getScaledVector(v, scale):
    if (scale <= 0):
        raise RuntimeError("Cector can not have zero length")
    v2 = ()
    v2[0] = v[0] * scale
    v2[1] = v[1] * scale
    return v2

def subVector(originalV, subV):
    newVector = (originalV[0] - subV[0], originalV[1] - subV[1])

    if (isInValidateVector(newVector)):
        raise RuntimeError("Could not subtract vectors an vector cannot have zero length")
        
    return newVector

def isInValidateVector(v):
    return (v[0] == 0 and v[1] == 0)

def distanceBetweenPoints(a, b):
    return hypot(a[0] - b[0], a[1] - b[1])
