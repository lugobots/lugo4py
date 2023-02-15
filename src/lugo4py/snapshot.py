from .loader import EnvVarLoader
from .goal import Goal
from .mapper import *
from . import orientation
from . import specs
from .stub import *
from . import geo

from .protos.physics_pb2 import Point,Vector
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
    def constructor(self, snapshot: server_pb2.GameSnapshot, mySide: server_pb2.Team.Side):
        self.snapshot = snapshot
        self.mySide = mySide
    

    def getMyTeam(self) -> server_pb2.Team:
        return self.getTeam(self.mySide)
    

    def getOpponentTeam(self) -> server_pb2.Team:
        return self.getTeam(self.getOpponentSide())
    

    def getTeam(self, side) -> server_pb2.Team:
        if (side == server_pb2.Side.HOME):
            return self.snapshot.HomeTeam
        
        return self.snapshot.awayTeam
    

    def isBallHolder(self, player: server_pb2.Player) -> bool:
        ball = self.snapshot.Ball

        return ball.Holder != None and ball.Holder.TeamSide == player.TeamSide and ball.Holder.Number == player.Number
    

    def getOpponentSide(self) -> server_pb2.Team.Side:
        if (self.mySide == server_pb2.Team.Side.HOME):
            return server_pb2.Team.Side.AWAY
        
        return server_pb2.Team.Side.HOME
    

    def getMyGoal(self) ->  Goal:
        if (self.mySide == server_pb2.Team.Side.HOME):
            return server_pb2.homeGoal
        
        return server_pb2.awayGoal
    
    def getBall(self) ->  server_pb2.Ball:
        return self.snapshot.Ball
    

    def getOpponentGoal(self) ->  Goal:
        if (self.mySide == server_pb2.Team.Side.HOME):
            return server_pb2.awayGoal
        
        return server_pb2.homeGoal
    

    def getPlayer(self, side: server_pb2.Team.Side, number: int) -> server_pb2.Player:
        team = self.getTeam(side)
        if (team == None):
            return None
        
        for player in team.getPlayersList():
            if (player.getNumber() == number):
                return player
        return None
    

    def makeOrderMoveMaxSpeed(self, origin: Point, target: Point) -> server_pb2.Order:
        return self.makeOrderMove(origin, target, specs.PLAYER_MAX_SPEED)
    

    def makeOrderMove(self, origin: Point, target: Point, speed: int) -> server_pb2.Order:
        if (origin.x == target.x and origin.y == target.y):
            # a vector cannot have zeroed direction. In this case, the player will just be stopped
            return self.makeOrderMoveFromVector(orientation.NORTH, 0)
        

        direction = geo.NewVector(origin, target)
        direction = geo.normalize(direction)
        return self.makeOrderMoveFromVector(direction, speed)
    

    def makeOrderMoveFromVector(self, direction: Vector, speed: int) -> server_pb2.Order:
        velocity = server_pb2.Velocity()
        velocity.setDirection(direction)
        velocity.setSpeed(speed)

        moveOrder = server_pb2.Move()
        moveOrder.setVelocity(velocity)
        return server_pb2.Order().setMove(moveOrder)
    

    def makeOrderMoveByDirection(self, direction) -> server_pb2.Order:
        directionTarget = None
        if direction == DIRECTION.FORWARD:
            directionTarget = orientation.EAST
            if (self.mySide == server_pb2.Team.Side.AWAY):
                directionTarget = orientation.WEST
            
        elif direction == DIRECTION.BACKWARD:
            directionTarget = orientation.WEST
            if (self.mySide == server_pb2.Team.Side.AWAY):
                directionTarget = orientation.EAST
            
        elif direction == DIRECTION.LEFT:
            directionTarget = orientation.NORTH
            if (self.mySide == server_pb2.Team.Side.AWAY):
                directionTarget = orientation.SOUTH
            
        elif direction == DIRECTION.RIGHT:
            directionTarget = orientation.SOUTH
            if (self.mySide == server_pb2.Team.Side.AWAY):
                directionTarget = orientation.NORTH
            
        elif direction == DIRECTION.BACKWARD_LEFT:
            directionTarget = orientation.NORTH_WEST
            if (self.mySide == server_pb2.Team.Side.AWAY):
                directionTarget = orientation.SOUTH_EAST
            
        elif direction == DIRECTION.BACKWARD_RIGHT:
            directionTarget = orientation.SOUTH_WEST
            if (self.mySide == server_pb2.Team.Side.AWAY):
                directionTarget = orientation.NORTH_EAST
            
        elif direction == DIRECTION.FORWARD_LEFT:
            directionTarget = orientation.NORTH_EAST
            if (self.mySide == server_pb2.Team.Side.AWAY):
                directionTarget = orientation.SOUTH_WEST
            
        elif direction == DIRECTION.FORWARD_RIGHT:
            directionTarget = orientation.SOUTH_EAST
            if (self.mySide == server_pb2.Team.Side.AWAY):
                directionTarget = orientation.NORTH_WEST
            
        else:
            raise AttributeError('unknown direction {direction}')

        
        return self.makeOrderMoveFromVector(directionTarget, specs.PLAYER_MAX_SPEED)
    


    def makeOrderJump(origin: Point, target: Point, speed: int) -> server_pb2.Order:
        direction = orientation.EAST
        if (origin.x != target.x or origin.y != target.y):
            # a vector cannot have zeroed direction. In this case, the player will just be stopped
            direction = geo.NewVector(origin, target)
            direction = geo.normalize(direction)
        
        velocity = server_pb2.Velocity()
        velocity.Direction = direction
        velocity.Speed = speed

        jump = server_pb2.Order.Jump()
        jump.setVelocity(velocity)

        order = server_pb2.Order()
        order.Jump = jump 
        return order
    

    def makeOrderKick(ball: server_pb2.Ball, target: Point, speed: int) -> server_pb2.Order:
        ballExpectedDirection = geo.NewVector(ball.getPosition(), target)

        # the ball velocity is summed to the kick velocity, so we have to consider the current ball direction
        diffVector = geo.subVector(ballExpectedDirection, ball.getVelocity().getDirection())

        newVelocity = server_pb2.Velocity()
        newVelocity.setSpeed(speed)
        newVelocity.setDirection(geo.normalize(diffVector))
        
        kick = server_pb2.Order.Kick()
        kick.Velocity = newVelocity 
        return kick
    

    def makeOrderKickMaxSpeed(self, ball: server_pb2.Ball, target: Point) -> server_pb2.Order:
        return self.makeOrderKick(ball, target, specs.BALL_MAX_SPEED)
    

    def makeOrderCatch(self) -> server_pb2.Order:
        return server_pb2.Order.Catch()
    



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
    if (not snapshot or not snapshot.getBall()):
        raise AttributeError('invalid snapshot state - cannot define player state')
    

    reader = GameSnapshotReader(snapshot, side)
    me = reader.getPlayer(side, playerNumber)
    if (not me):
        raise AttributeError('could not find the bot in the snapshot - cannot define player state')
    

    ballHolder = snapshot.getBall().getHolder()
    
    if (not ballHolder):
        return PLAYER_STATE.DISPUTING_THE_BALL

    elif (ballHolder.getTeamSide() == side):
        if (ballHolder.getNumber() == playerNumber):
            return PLAYER_STATE.HOLDING_THE_BALL
        
        return PLAYER_STATE.SUPPORTING
    
    return PLAYER_STATE.DEFENDING