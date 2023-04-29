import asyncio
import grpc
from datetime import datetime, timedelta
from ..protos.remote_pb2 import (
    PauseResumeRequest, NextTurnRequest, NextOrderRequest,
    BallProperties, PlayerProperties, GameProperties,
    ResumeListeningRequest, ResumeListeningResponse
)
from ..protos.remote_pb2_grpc import RemoteStub
from ..protos.physics_pb2 import Point, Velocity
from ..protos.server_pb2 import GameSnapshot, Team
from ..client import LugoClient
import time
import threading

class RemoteControl:
    def __init__(self):
        self.client = None

    def connect(self, grpc_address: str) -> None:
        channel = grpc.insecure_channel(grpc_address)
        try:
            grpc.channel_ready_future(channel).result(timeout=15)
        except grpc.FutureTimeoutError:
            raise Exception("timed out waiting to connect to the game server")
        self.client = RemoteStub(channel)

    def pauseResume(self):
        req = PauseResumeRequest()
        try:
            return self.client.PauseOrResume(req)
        except Exception:
            raise Exception("[Remote Control] Failed to pause/resume the game")

    def resumeListening(self, waiter: threading.Event):
        req = ResumeListeningRequest()
        try:
            result = self.client.ResumeListeningPhase(req)
            print(f"ON LISTENING PHASE: {result}")
            waiter.set()
            return result
        except Exception:
            raise Exception("[Remote Control] Failed to resume listening phase the game")


    def nextTurn(self):
        req = NextTurnRequest()
        try:
            return self.client.NextTurn(req)
        except Exception:
            raise Exception("[Remote Control] Failed to play to next turn")

    def nextOrder(self):
        req = NextOrderRequest()
        try:
            return self.client.NextOrder(req)
        except Exception:
            raise Exception("[Remote Control] Failed to play to next order")

    def setBallProps(self, position: Point, velocity: Velocity):
        req = BallProperties(position=position, velocity=velocity)
        response = self.client.SetBallProperties(req)
        return response

    def setPlayerProps(self, teamSide: Team.Side, playerNumber: int, newPosition: Point, newVelocity: Velocity):
        req = PlayerProperties(
            side=teamSide, number=playerNumber,
            position=newPosition, velocity=newVelocity
        )
        response = self.client.SetPlayerProperties(req)
        return response

    def setGameProps(self, turnNumber: int):
        req = GameProperties(turn=turnNumber)
        response = self.client.SetGameProperties(req)
        return response
