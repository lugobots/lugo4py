from .protos.physics_pb2 import Point
from .protos.server_pb2 import Team 

class Goal(object):

    def __init__(self , place: Team.Side, center : Point, topPole : Point, bottomPole : Point):
        self._center = center
        self._place = place
        self._topPole = topPole
        self._bottomPole = bottomPole

    def getCenter(self) -> Point: 
        return self._center

    def getPlace(self) -> Team.Side:
        return self._place

    def getTopPole(self) -> Point:
        return self._topPole

    def getBottomPole(self) -> Point:
        return self._bottomPole