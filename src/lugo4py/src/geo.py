from . import lugo
from ..protos import physics_pb2
from math import hypot


def new_vector(from_point: lugo.Point, to_point: lugo.Point):
    v = physics_pb2.Vector()
    v.x = to_point.x - from_point.x
    v.y = to_point.y - from_point.y
    if is_invalid_vector(v):
        raise RuntimeError("A vector cannot have zero length")
    return v


def normalize(v: lugo.Vector):
    length = get_length(v)
    return get_scaled_vector(v, 100 / length)


def get_length(v: lugo.Vector):
    return hypot(v.x, v.y)


def get_scaled_vector(v: lugo.Vector, scale: float):
    if scale <= 0:
        raise RuntimeError("Vector cannot have zero length")
    v2 = physics_pb2.Vector()
    v2.x = v.x * scale
    v2.y = v.y * scale
    return v2


def sub_vector(original_vector: lugo.Vector, sub_vector: lugo.Vector) -> lugo.Vector:
    new_x = original_vector.x - sub_vector.x
    new_y = original_vector.y - sub_vector.y

    new_vector = physics_pb2.Vector()
    new_vector.x = new_x
    new_vector.y = new_y

    if is_invalid_vector(new_vector):
        raise ValueError("Could not subtract vectors: the result would be a zero-length vector")
    return new_vector


def is_invalid_vector(v: lugo.Vector) -> bool:
    return v.x == 0 and v.y == 0


def distance_between_points(a: lugo.Point, b: lugo.Point):
    return hypot(a.x - b.x, a.y - b.y)
