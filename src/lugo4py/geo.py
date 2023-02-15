from .protos import physics_pb2
from typing import Tuple
from math import hypot

def NewVector(fromPoint : physics_pb2.Point, toPoint : physics_pb2.Point) :
    v = physics_pb2.Vector()
    v.x = toPoint.x - fromPoint.x
    v.x = toPoint.y - fromPoint.y
    if isInValidateVector(v):
        raise RuntimeError("A vector cannot have zero length")
    return v

def normalize(v : physics_pb2.Vector):
    length = getLength(v)
    return getScaledVector(v, 100 / length)

def getLength(v: physics_pb2.Vector):
    return hypot(v.x, v.y)

def getScaledVector(v: physics_pb2.Vector, scale : float):
    if (scale <= 0):
        raise RuntimeError("Cector can not have zero length")
    v2 = physics_pb2.Vector()
    v2.x = v.x * scale
    v2.y = v.y * scale
    return v2

def subVector(originalV : physics_pb2.Vector, subV : physics_pb2.Vector):
    newVector = (originalV.x - subV.x, originalV.y - subV.y)

    if (isInValidateVector(newVector)):
        raise RuntimeError("Could not subtract vectors an vector cannot have zero length")
        
    return newVector

def isInValidateVector(v : physics_pb2.Vector):
    return (v.x == 0 and v.y == 0)

def distanceBetweenPoints(a : physics_pb2.Point, b : physics_pb2.Point):
    return hypot(a.x - b.x, a.y - b.y)
