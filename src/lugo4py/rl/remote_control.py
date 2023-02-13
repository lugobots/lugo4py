import grpc
from ..protos import remote_pb2_grpc
from ..protos.remote_pb2 import  PauseResumeRequest, BallProperties, NextTurnRequest, PlayerProperties, GameProperties, ResumeListeningRequest
from ..protos.physics_pb2 import Point, Velocity
from ..protos.physics_pb2 import GameSnapshot, Team


class RemoteControl(object):
    
    def __init__(self):
        self.client = None

    async def connect(grpcAddress: str):
        pass
        # await new Promise<void>((resolve, reject) => {
        #     this.client = new remote.RemoteClient(grpcAddress, grpc.credentials.createInsecure())
        #     const deadline = new Date();
        #     deadline.setSeconds(deadline.getSeconds() + 5);
        #     this.client.waitForReady(deadline, (err) => {
        #         if (err) {
        #             console.log(`ERROR: `, err)
        #             reject(err)
        #             return
        #         }
        #         resolve()
        #     })
        # })

    async def pauseResume(self):
        pauseReq = PauseResumeRequest()
        # return new Promise<void>((resolve, reject) => {
        #     const resp = this.client.pauseOrResume(pauseReq, (err) => {
        #         if (err) {
        #             console.log(`ERROR: `, err)
        #             reject(err)
        #             return
        #         }
        #         resolve()
        #     })
        # })

    async def resumeListening(self):
        req = ResumeListeningRequest()
        # return new Promise<void>((resolve, reject) => {
        #     const resp = this.client.resumeListeningPhase(req, (err) => {
        #         if (err) {
        #             console.log(`ERROR: `, err)
        #             reject(err)
        #             return
        #         }
        #         resolve()
        #     })
        # })

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