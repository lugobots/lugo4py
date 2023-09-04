"""
File: lugo.py
Author: Angelo Katipunan
Date: May 20, 2023
Description: This file mocks the gRPC methods to help IDEs intellisense.

Python gRPC files are not friendly to IDEs, what makes the intellisense experience very poor or, sometimes, impossible.

In order to help the programmer experience while developing bots, this file mocks the gRPC methods in a more friendly way.

In short, this file content is not used at all by the package, but will guide the IDE to help the devs.
If you are looking for the real implementation of these methods, please look at the `protos` directory (good luck on that)

"""

from enum import IntEnum
from typing import List

from ..protos import physics_pb2


class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Velocity:
    def __init__(self, direction=None, speed=0.0):
        self.direction = direction if direction is not None else Vector()
        self.speed = speed


def new_velocity(point: Point) -> Velocity:
    v = physics_pb2.Velocity()
    v.direction.x = point.x
    v.direction.y = point.y
    return v


# Classes from remote.proto

class RemoteServicer(object):

    def PauseOrResume(self, request, context):
        # TODO: Implement the PauseOrResume method.
        response = CommandResponse()
        return response

    def NextTurn(self, request, context):
        # TODO: Implement the NextTurn method.
        response = CommandResponse()
        return response

    def NextOrder(self, request, context):
        # TODO: Implement the NextOrder method.
        response = CommandResponse()
        return response

    def SetBallProperties(self, request, context):
        # TODO: Implement the SetBallProperties method.
        response = CommandResponse()
        return response

    def SetPlayerProperties(self, request, context):
        # TODO: Implement the SetPlayerProperties method.
        response = CommandResponse()
        return response

    def SetGameProperties(self, request, context):
        # TODO: Implement the SetGameProperties method.
        response = CommandResponse()
        return response

    def ResumeListeningPhase(self, request, context):
        # TODO: Implement the ResumeListeningPhase method.
        response = ResumeListeningResponse()
        return response


class PauseResumeRequest(object):
    def __init__(self):
        pass


class NextTurnRequest(object):
    def __init__(self):
        pass


class NextOrderRequest(object):
    def __init__(self):
        pass


class BallProperties:
    def __init__(self, position=None, velocity=None, holder=None):
        self.position = position if position is not None else Point()
        self.velocity = velocity if velocity is not None else Velocity()
        self.holder = holder


class PlayerProperties:
    def __init__(self, side=None, number=0, position=None, velocity=None):
        self.side = side
        self.number = number
        self.position = position if position is not None else Point()
        self.velocity = velocity if velocity is not None else Velocity()


class GameProperties:
    def __init__(self, turn=0, home_score=0, away_score=0, frame_interval=0, shot_clock=None):
        self.turn = turn
        self.home_score = home_score
        self.away_score = away_score
        self.frame_interval = frame_interval
        self.shot_clock = shot_clock


class CommandResponse:
    class StatusCode(IntEnum):
        SUCCESS = 0
        INVALID_VALUE = 1
        DEADLINE_EXCEEDED = 2
        OTHER = 99

    def __init__(self, code=None, game_snapshot=None, details=''):
        self.code = code if code is not None else CommandResponse.StatusCode.SUCCESS
        self.game_snapshot = game_snapshot
        self.details = details


class ResumeListeningRequest(object):
    def __init__(self):
        pass


class ResumeListeningResponse(object):
    def __init__(self):
        pass


# from file src/server.proto


class TeamSide(IntEnum):
    HOME = 0
    AWAY = 1


class State(IntEnum):
    WAITING = 0
    GET_READY = 1
    LISTENING = 2
    PLAYING = 3
    SHIFTING = 4
    OVER = 99


class StatusCode(IntEnum):
    SUCCESS = 0
    UNKNOWN_PLAYER = 1
    NOT_LISTENING = 2
    WRONG_TURN = 3
    OTHER = 99


class Player:
    def __init__(self, number: int, position: Point, velocity: Velocity, team_side: TeamSide, init_position: Point):
        self.number = number

        if position.x is None:
            position.x = 0
        if position.y is None:
            position.y = 0

        self.position = position
        self.velocity = velocity
        self.team_side = team_side
        self.init_position = init_position


class Team:
    def __init__(self, players: List[Player], name: str, score: int, side: TeamSide):
        self.players = players
        self.name = name
        self.score = score
        self.side = side


class Ball:
    def __init__(self, position: Point, velocity: Velocity, holder: Player):
        self.position = position
        self.velocity = velocity
        self.holder = holder


class ShotClock:
    def __init__(self, team_side: TeamSide, remaining_turns: int):
        self.team_side = team_side
        self.remaining_turns = remaining_turns


class JoinRequest:
    def __init__(self, token: str, protocol_version: str, team_side: TeamSide, number: int, init_position: Point):
        self.token = token
        self.protocol_version = protocol_version
        self.team_side = team_side
        self.number = number
        self.init_position = init_position


class GameSnapshot:
    def __init__(self, state: State, turn: int, home_team: Team, away_team: Team, ball: Ball,
                 turns_ball_in_goal_zone: int, shot_clock: ShotClock):
        self.state = state
        self.turn = turn
        self.home_team = home_team
        self.away_team = away_team
        self.ball = ball
        self.turns_ball_in_goal_zone = turns_ball_in_goal_zone
        self.shot_clock = shot_clock


class Order:
    pass


class Move(Order):
    def __init__(self, velocity: Velocity):
        self.velocity = velocity


class Catch(Order):
    pass


class Kick(Order):
    def __init__(self, velocity: Velocity):
        self.velocity = velocity


class Jump(Order):
    def __init__(self, velocity: Velocity):
        self.velocity = velocity


class OrderSet:
    def __init__(self, turn: int, orders: List[Order], debug_message: str):
        self.turn = turn
        self.orders = orders
        self.debug_message = debug_message


class OrderResponse:
    def __init__(self, code: StatusCode, details: str):
        self.code = code
        self.details = details
