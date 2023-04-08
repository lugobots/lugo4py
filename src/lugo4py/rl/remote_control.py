import asyncio
import grpc
from datetime import datetime, timedelta
from src.lugo4py.protos.remote_pb2 import (
    PauseResumeRequest, NextTurnRequest, NextOrderRequest,
    BallProperties, PlayerProperties, GameProperties,
    ResumeListeningRequest, ResumeListeningResponse
)
from src.lugo4py.protos.remote_pb2_grpc import RemoteStub
from src.lugo4py.protos.physics_pb2 import Point, Velocity
from src.lugo4py.protos.server_pb2 import GameSnapshot, Team
from src.lugo4py.client import LugoClient
import time


class RemoteControl:
    def __init__(self):
        self.client = None

    async def connect(self, grpc_address: str) -> None:
        async with grpc.aio.insecure_channel(grpc_address) as channel:
            self.client = RemoteStub(channel)
            deadline = grpc.deadline(time.time() + 5)
            try:
                await channel.wait_for_ready(deadline)
            except grpc.FutureTimeoutError as err:
                print("ERROR:", err)
                raise err

    async def pauseResume(self):
        req = PauseResumeRequest()
        return await self.channel.PauseOrResume(req)

    async def resumeListening(self):
        req = ResumeListeningRequest()
        return await self.channel.ResumeListeningPhase(req)

    async def nextTurn(self):
        req = NextTurnRequest()
        return await self.channel.NextTurn(req)

    async def nextOrder(self):
        req = NextOrderRequest()
        return await self.channel.NextOrder(req)

    async def setBallProps(self, position: Point, velocity: Velocity):
        req = BallProperties(position=position, velocity=velocity)
        response = await self.channel.SetBallProperties(req)
        return response

    async def setPlayerProps(self, teamSide: Team.Side, playerNumber: int, newPosition: Point, newVelocity: Velocity):
        req = PlayerProperties(
            side=teamSide, number=playerNumber,
            position=newPosition, velocity=newVelocity
        )
        response = await self.channel.SetPlayerProperties(req)
        return response

    async def setGameProps(self, turnNumber: int):
        req = GameProperties(turn=turnNumber)
        response = await self.channel.SetGameProperties(req)
        return response
