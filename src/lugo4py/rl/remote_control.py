import asyncio
from datetime import datetime, timedelta
import grpc
from ..protos.remote_pb2 import PauseResumeRequest, BallProperties, NextTurnRequest, PlayerProperties, GameProperties, ResumeListeningRequest
from ..protos.physics_pb2 import Point, Velocity
from ..protos.server_pb2 import GameSnapshot, Team
from ..protos import remote_pb2_grpc


class RemoteControl(object):

    def __init__(self):
        self.client = None

    async def connect(self, grpcAddress: str):
        loop = asyncio.get_event_loop()
        self.client = remote_pb2_grpc.RemoteClient(
            grpcAddress, grpc.credentials.create_insecure())
        deadline = datetime.now() + timedelta(seconds=5)

        def callback(err):
            if err:
                print(f"ERROR: {err}")
                loop.stop()
            else:
                loop.stop()

        self.client.wait_for_ready(deadline, callback)
        loop.run_forever()

    async def pauseResume(self):
        pauseReq = PauseResumeRequest()
        return asyncio.get_running_loop().run_in_executor(None, lambda: self.client.pauseOrResume(pauseReq))

    async def resumeListening(self):
        req = ResumeListeningRequest()
        return await asyncio.to_thread(self.client.resumeListeningPhase, req)

    async def nextTurn(self):
        nextTurnReq = NextTurnRequest()
        return await asyncio.get_event_loop().run_in_executor(None, lambda: self.client.nextTurn(nextTurnReq))

    async def setBallProps(self, position: Point, velocity: Velocity):
        ball_properties = BallProperties()
        ball_properties.velocity.CopyFrom(velocity)
        ball_properties.position.CopyFrom(position)
        response = await self.client.SetBallProperties(ball_properties)
        return response.GameSnapshot

    async def setPlayerProps(self, teamSide: Team.Side, playerNumber: int, newPosition: Point, newVelocity: Velocity) -> GameSnapshot:
        player_properties = PlayerProperties()
        player_properties.velocity.CopyFrom(newVelocity)
        player_properties.position.CopyFrom(newPosition)
        player_properties.side = teamSide
        player_properties.number = playerNumber
        response = await self.client.SetPlayerProperties(player_properties)
        return response.GameSnapshot

    async def setTurn(self, turnNumber):
        gameProp = GameProperties()
        gameProp.setTurn(turnNumber)
        response = await self.client.setGameProperties(gameProp)
        return response.game_snapshot
