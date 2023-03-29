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
        # return new Promise<void>((resolve, reject) => {
        #     const resp = this.client.nextTurn(nextTurnReq, (err) => {
        #         if (err) {
        #             console.log(`ERROR: `, err)
        #             reject(err)
        #             return
        #         }
        #         resolve()
        #     })
        # })

    async def setBallProps(self, position: Point, velocity: Velocity):
        ballPropReq = BallProperties()
        ballPropReq.setVelocity(velocity)
        ballPropReq.setPosition(position)
        # return new Promise<GameSnapshot>((resolve, reject) => {
        #     const resp = this.client.setBallProperties(ballPropReq, (err, commandResponse) => {
        #         if (err) {
        #             console.log(`ERROR: ballPropReq`, ballPropReq, err)
        #             reject(err)
        #             return
        #         }
        #         resolve(commandResponse.getGameSnapshot())
        #     })
        # })

    async def setPlayerProps(teamSide: Team.Side, playerNumber: number, newPosition: Point, newVelocity: Velocity):
        playerProperties = PlayerProperties()
        playerProperties.setVelocity(newVelocity)
        playerProperties.setPosition(newPosition)
        playerProperties.setSide(teamSide)
        playerProperties.setNumber(playerNumber)
        # return new Promise<GameSnapshot>((resolve, reject) => {
        #     const resp = this.client.setPlayerProperties(playerProperties, (err, commandResponse) => {
        #         if (err) {
        #             console.log(`ERROR: (playerProperties)`, err)
        #             reject(err)
        #             return
        #         }
        #         resolve(commandResponse.getGameSnapshot())
        #     })
        # })

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
