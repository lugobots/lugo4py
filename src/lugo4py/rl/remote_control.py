from datetime import datetime, timedelta
import grpc
from ..protos import remote_pb2_grpc
from ..protos.remote_pb2 import PauseResumeRequest, BallProperties, NextTurnRequest, PlayerProperties, GameProperties, ResumeListeningRequest
from ..protos.physics_pb2 import Point, Velocity
from ..protos.physics_pb2 import GameSnapshot, Team
import asyncio


class RemoteControl(object):

    def __init__(self):
        self.client = None

    async def connect(self, grpcAddress: str) -> None:
        try:
            self.client = remote.RemoteClient(
                grpcAddress, grpc.credentials.create_insecure())
            deadline = datetime.now() + timedelta(seconds=5)
            await self.client.wait_for_ready(deadline=deadline)
        except grpc.RpcError as e:
            print("ERROR: ", e)
            raise e

    async def pauseResume(self):
        pause_req = remote.PauseResumeRequest()
        try:
            self.client.pause_or_resume(pause_req)
        except grpc.RpcError as e:
            print(f"ERROR: {e}")
            raise

    async def resumeListening(self):
        request = remote.ResumeListeningRequest()
        return await asyncio.create_task(
            self.client.resumeListeningPhase(request)
        )

    async def nextTurn(self):
        nextTurnReq = NextTurnRequest()
        try:
            await self.stub.nextTurn(nextTurnReq)
        except grpc.RpcError as e:
            print(f"Error: {e.code()}: {e.details()}")
        raise e

    async def setBallProps(self, position: Point, velocity: Velocity):
        ball_prop_req = BallProperties()
        ball_prop_req.velocity.CopyFrom(velocity)
        ball_prop_req.position.CopyFrom(position)
        try:
            response = await self.stub.SetBallProperties(ball_prop_req)
            return response.gameSnapshot
        except grpc.RpcError as e:
            print(f"ERROR: ball_prop_req {ball_prop_req} {e}")
        raise e from None

    async def setPlayerProps(teamSide, playerNumber, newPosition, newVelocity):
        playerProperties = PlayerProperties()
        playerProperties.setVelocity(newVelocity)
        playerProperties.setPosition(newPosition)
        playerProperties.setSide(teamSide)
        playerProperties.setNumber(playerNumber)

        loop = asyncio.get_event_loop()
        future = loop.create_future()

        def callback(err, commandResponse):
            if err:
                print(f"ERROR: (playerProperties) {err}")
                future.set_exception(err)
            else:
                future.set_result(commandResponse.getGameSnapshot())

        resp = await loop.run_in_executor(None, client.setPlayerProperties, playerProperties, callback)
        return await future

    async def setTurn(self, turnNumber):
        gameProp = GameProperties()
        # gameProp.setTurn(turnNumber)
        # return new Promise<GameSnapshot>((resolve, reject) => {
        #     const resp = this.client.setGameProperties(gameProp, (err, commandResponse) => {
        #         if (err) {
        #             console.log(`ERROR: `, err)
        #             reject(err)
        #             return
        #         }
        #         resolve(commandResponse.getGameSnapshot())
        #     })
        # })
