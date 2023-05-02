from .loader import EnvVarLoader
from .goal import Goal
from .mapper import *
from . import orientation
from . import specs
from .stub import *
from . import geo

from .protos.physics_pb2 import Point, Vector
from .protos import server_pb2


# import * as Lugo from './proto_exported'
# import * as rl from "./rl/index"
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
homeGoalCenter.x = (0)
homeGoalCenter.y = int(specs.MAX_Y_COORDINATE / 2)

homeGoalTopPole = Point()
homeGoalTopPole.x = (0)
homeGoalTopPole.y = int(specs.GOAL_MAX_Y)

homeGoalBottomPole = Point()
homeGoalBottomPole.x = (0)
homeGoalBottomPole.y = int(specs.GOAL_MIN_Y)

awayGoalCenter = Point()
awayGoalCenter.x = int(specs.MAX_X_COORDINATE)
awayGoalCenter.y = int(specs.MAX_Y_COORDINATE / 2)

awayGoalTopPole = Point()
awayGoalTopPole.x = int(specs.MAX_X_COORDINATE)
awayGoalTopPole.y = int(specs.GOAL_MAX_Y)

awayGoalBottomPole = Point()
awayGoalBottomPole.x = int(specs.MAX_X_COORDINATE)
awayGoalBottomPole.y = int(specs.GOAL_MIN_Y)


class GameSnapshotReader:
    def __init__(self, snapshot: server_pb2.GameSnapshot, mySide: server_pb2.Team.Side):
        self.snapshot = snapshot
        self.mySide = mySide

    def get_my_team(self) -> server_pb2.Team:
        return self.getTeam(self.mySide)

    def get_opponent_team(self) -> server_pb2.Team:
        return self.getTeam(self.getOpponentSide())

    def get_team(self, side) -> server_pb2.Team:
        if side == server_pb2.Team.Side.HOME:
            return self.snapshot.home_team

        return self.snapshot.away_team

    def is_ball_holder(self, player: server_pb2.Player) -> bool:
        ball = self.snapshot.ball

        return ball.holder != None and ball.holder.team_side == player.team_side and ball.holder.number == player.number

    def get_opponent_side(self) -> server_pb2.Team.Side:
        if self.mySide == server_pb2.Team.Side.HOME:
            return server_pb2.Team.Side.AWAY

        return server_pb2.Team.Side.HOME

    def get_my_goal(self) -> Goal:
        if self.mySide == server_pb2.Team.Side.HOME:
            return homeGoal

        return awayGoal

    def get_ball(self) -> server_pb2.Ball:
        return self.snapshot.ball

    def get_opponent_goal(self) -> Goal:
        if self.mySide == server_pb2.Team.Side.HOME:
            return awayGoal

        return homeGoal

    def get_player(self, side: server_pb2.Team.Side, number: int) -> server_pb2.Player:
        team = self.get_team(side)
        if team is None:
            return None

        for player in team.players:
            if player.number == number:
                return player
        return None

    def make_order_move_max_speed(self, origin: Point, target: Point) -> server_pb2.Order:
        return self.make_order_move(origin, target, specs.PLAYER_MAX_SPEED)

    def make_order_move(self, origin: Point, target: Point, speed: int) -> server_pb2.Order:
        if origin.x == target.x and origin.y == target.y:
            # a vector cannot have zeroed direction. In this case, the player will just be stopped
            return self.make_order_move_from_vector(orientation.NORTH, 0)

        direction = geo.NewVector(origin, target)
        direction = geo.normalize(direction)
        return self.make_order_move_from_vector(direction, speed)

    def make_order_move_from_vector(self, direction: Vector, speed: int) -> server_pb2.Order:
        order = server_pb2.Order()

        order.move.velocity.direction.x = direction.x
        order.move.velocity.direction.y = direction.y
        order.move.velocity.speed = speed
        return order

    def make_order_move_by_direction(self, direction) -> server_pb2.Order:
        if direction == DIRECTION.FORWARD:
            direction_target = orientation.EAST
            if self.mySide == server_pb2.Team.Side.AWAY:
                direction_target = orientation.WEST

        elif direction == DIRECTION.BACKWARD:
            direction_target = orientation.WEST
            if self.mySide == server_pb2.Team.Side.AWAY:
                direction_target = orientation.EAST

        elif direction == DIRECTION.LEFT:
            direction_target = orientation.NORTH
            if self.mySide == server_pb2.Team.Side.AWAY:
                direction_target = orientation.SOUTH

        elif direction == DIRECTION.RIGHT:
            direction_target = orientation.SOUTH
            if self.mySide == server_pb2.Team.Side.AWAY:
                direction_target = orientation.NORTH

        elif direction == DIRECTION.BACKWARD_LEFT:
            direction_target = orientation.NORTH_WEST
            if self.mySide == server_pb2.Team.Side.AWAY:
                direction_target = orientation.SOUTH_EAST

        elif direction == DIRECTION.BACKWARD_RIGHT:
            direction_target = orientation.SOUTH_WEST
            if self.mySide == server_pb2.Team.Side.AWAY:
                direction_target = orientation.NORTH_EAST

        elif direction == DIRECTION.FORWARD_LEFT:
            direction_target = orientation.NORTH_EAST
            if self.mySide == server_pb2.Team.Side.AWAY:
                direction_target = orientation.SOUTH_WEST

        elif direction == DIRECTION.FORWARD_RIGHT:
            direction_target = orientation.SOUTH_EAST
            if self.mySide == server_pb2.Team.Side.AWAY:
                direction_target = orientation.NORTH_WEST

        else:
            raise AttributeError('unknown direction {direction}')

        return self.make_order_move_from_vector(direction_target, specs.PLAYER_MAX_SPEED)

    def makeOrderJump(origin: Point, target: Point, speed: int) -> server_pb2.Order:
        direction = orientation.EAST
        if (origin.x != target.x or origin.y != target.y):
            # a vector cannot have zeroed direction. In this case, the player will just be stopped
            direction = geo.NewVector(origin, target)
            direction = geo.normalize(direction)

        velocity = server_pb2.Velocity()
        velocity.direction = direction
        velocity.speed = speed

        jump = server_pb2.Order.Jump()
        jump.velocity = velocity

        order = server_pb2.Order()
        order.Jump = jump
        return order

    def makeOrderKick(ball: server_pb2.Ball, target: Point, speed: int) -> server_pb2.Order:
        ballExpectedDirection = geo.NewVector(ball.getPosition(), target)

        # the ball velocity is summed to the kick velocity, so we have to consider the current ball direction
        diffVector = geo.subVector(ballExpectedDirection, ball.getVelocity().getDirection())

        newVelocity = server_pb2.Velocity()
        newVelocity.speed = speed
        newVelocity.direction = geo.normalize(diffVector)

        kick = server_pb2.Order.Kick()
        kick.Velocity = newVelocity
        return kick

    def makeOrderKickMaxSpeed(self, ball: server_pb2.Ball, target: Point) -> server_pb2.Order:
        return self.makeOrderKick(ball, target, specs.BALL_MAX_SPEED)

    def makeOrderCatch(self) -> server_pb2.Order:
        order = server_pb2.Order()
        order.catch.SetInParent()
        return order


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


def defineState(snapshot: server_pb2.GameSnapshot, playerNumber: int, side: server_pb2.Team.Side) -> PLAYER_STATE:
    if (not snapshot or not snapshot.ball):
        raise AttributeError('invalid snapshot state - cannot define player state')

    reader = GameSnapshotReader(snapshot, side)
    me = reader.getPlayer(side, playerNumber)
    if (me is None):
        raise AttributeError('could not find the bot in the snapshot - cannot define player state')

    ballHolder = snapshot.ball.holder

    if ballHolder.number == 0:
        return PLAYER_STATE.DISPUTING_THE_BALL

    if (ballHolder.team_side == side):
        if (ballHolder.number == playerNumber):
            return PLAYER_STATE.HOLDING_THE_BALL

        return PLAYER_STATE.SUPPORTING

    return PLAYER_STATE.DEFENDING
