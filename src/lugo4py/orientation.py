from .protos import physics_pb2
from . import geo

EAST = geo.normalize(physics_pb2.Vector().x(1))
WEST = geo.normalize(physics_pb2.Vector().x(-1))
SOUTH = geo.normalize(physics_pb2.Vector().y(1))
NORTH = geo.normalize(physics_pb2.Vector().y(-1))

NORTH_EAST = geo.normalize(physics_pb2.Vector().x(1).y(1))
NORTH_WEST = geo.normalize(physics_pb2.Vector().x(-1).y(1))
SOUTH_EAST = geo.normalize(physics_pb2.Vector().x(1).y(-1))
SOUTH_WEST = geo.normalize(physics_pb2.Vector().x(-1).y(-1))