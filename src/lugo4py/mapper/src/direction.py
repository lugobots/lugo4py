from ...protos.physics_pb2 import Point

from ...src.specs import *
from ...src.goal import Goal
from ...protos import server_pb2

class Direction(object):
    pass


DIRECTION = Direction()
DIRECTION.FORWARD = 0
DIRECTION.BACKWARD = 1,
DIRECTION.LEFT = 2,
DIRECTION.RIGHT = 3,
DIRECTION.BACKWARD_LEFT = 4,
DIRECTION.BACKWARD_RIGHT = 5,
DIRECTION.FORWARD_LEFT = 6,
DIRECTION.FORWARD_RIGHT = 7

homeGoalCenter = Point()
homeGoalCenter.x = 0
homeGoalCenter.y = int(MAX_Y_COORDINATE / 2)

homeGoalTopPole = Point()
homeGoalTopPole.x = 0
homeGoalTopPole.y = int(GOAL_MAX_Y)

homeGoalBottomPole = Point()
homeGoalBottomPole.x = 0
homeGoalBottomPole.y = int(GOAL_MIN_Y)

awayGoalCenter = Point()
awayGoalCenter.x = int(MAX_X_COORDINATE)
awayGoalCenter.y = int(MAX_Y_COORDINATE / 2)

awayGoalTopPole = Point()
awayGoalTopPole.x = int(MAX_X_COORDINATE)
awayGoalTopPole.y = int(GOAL_MAX_Y)

awayGoalBottomPole = Point()
awayGoalBottomPole.x = int(MAX_X_COORDINATE)
awayGoalBottomPole.y = int(GOAL_MIN_Y)

awayGoal = Goal(
    server_pb2.Team.Side.AWAY,
    awayGoalCenter,
    awayGoalTopPole,
    awayGoalBottomPole
)
homeGoal = Goal(
    server_pb2.Team.Side.HOME,
    homeGoalCenter,
    homeGoalTopPole,
    homeGoalBottomPole
)