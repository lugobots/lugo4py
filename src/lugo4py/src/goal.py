from . import lugo
from ..protos.physics_pb2 import Point
from ..protos.server_pb2 import Team


class Goal(object):

    def __init__(self, place: lugo.TeamSide, center: lugo.Point, top_pole: lugo.Point, bottom_pole: lugo.Point):
        self._center = center
        self._place = place
        self._topPole = top_pole
        self._bottomPole = bottom_pole

    def get_center(self) -> Point:
        return self._center

    def get_place(self) -> Team.Side:
        return self._place

    def get_top_pole(self) -> Point:
        return self._topPole

    def get_bottom_pole(self) -> Point:
        return self._bottomPole
