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


class RemoteControl(object):

    def __init__(self):
        self.channel = None
        self.stub = None

    async def connect(self, grpcAddress: str):
        self.channel = grpc.aio.insecure_channel(grpcAddress)
        deadline = datetime.now() + timedelta(seconds=5)
        await self.channel.channel_ready.wait(deadline=deadline)
        self.stub = RemoteStub(self.channel)

    async def pauseResume(self):
        req = PauseResumeRequest()
        return await self.stub.PauseOrResume(req)

    async def resumeListening(self):
        req = ResumeListeningRequest()
        return await self.stub.ResumeListeningPhase(req)

    async def nextTurn(self):
        req = NextTurnRequest()
        return await self.stub.NextTurn(req)

    async def nextOrder(self):
        req = NextOrderRequest()
        return await self.stub.NextOrder(req)

    async def setBallProps(self, position: Point, velocity: Velocity):
        req = BallProperties(position=position, velocity=velocity)
        response = await self.stub.SetBallProperties(req)
        return response

    async def setPlayerProps(self, teamSide: Team.Side, playerNumber: int, newPosition: Point, newVelocity: Velocity):
        req = PlayerProperties(
            side=teamSide, number=playerNumber,
            position=newPosition, velocity=newVelocity
        )
        response = await self.stub.SetPlayerProperties(req)
        return response

    async def setGameProps(self, turnNumber: int):
        req = GameProperties(turn=turnNumber)
        response = await self.stub.SetGameProperties(req)
        return response
