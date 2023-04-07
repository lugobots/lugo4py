from src.lugo4py.rl.training_controller import TrainingCrl, delay
from src.lugo4py.rl.helper_bots import newZombiePlayer, newChaserHelperPlayer, newZombieHelperPlayer
from src.lugo4py.rl.remote_control import RemoteControl
from src.lugo4py.rl.interfaces import BotTrainer, TrainingFunction
from src.lugo4py.client import LugoClient
from src.lugo4py.protos.server_pb2 import Team, OrderSet
import asyncio


class Gym(object):

    def __init__(self, lugo_client: LugoClient, trainer: BotTrainer, trainingFunction: TrainingFunction, debugging_log=False):
        self.gameServerAddress = ''
        self.lugo_client = lugo_client
        self.remoteControl = RemoteControl(lugo_client)
        self.trainingCrl = TrainingCrl(
            lugo_client, trainer, trainingFunction)
        self.trainingCrl.debugging_log = debugging_log

    async def playCallable(self, orderSet, snapshot):
        hasStarted = True
        await self.trainingCrl.gameTurnHandler(orderSet, snapshot)
        if self.gameServerAddress:
            await self.completeWithZombies(self.gameServerAddress)
        asyncio.get_running_loop().call_later(
            1, lambda: self.remoteControl.resumeListening() if not hasStarted else None)

    async def start(self, lugoClient: LugoClient):
        # If the game was started in a previous training session, the game server will be stuck on the listening phase.
        # so we check if the game has started, if now, we try to resume the server
        hasStarted = False
        await lugoClient.play(self.playCallable)

    def withZombiePlayers(self, gameServerAddress):
        self.gameServerAddress = gameServerAddress
        return self

    async def completeWithZombies(gameServerAddress):
        for i in range(1, 12):
            await newZombiePlayer(Team.Side.HOME, i, gameServerAddress)
            await delay(50)
            await newZombiePlayer(Team.Side.AWAY, i, gameServerAddress)
            await delay(50)

    def withRandomMotionPlayers(self, gameServerAddress):
        self.gameServerAddress = gameServerAddress

        async def helperPlayers(gameServerAddress):
            for i in range(1, 12):
                await newChaserHelperPlayer(Team.Side.HOME, i, gameServerAddress)
                await delay(50)
                await newChaserHelperPlayer(Team.Side.AWAY, i, gameServerAddress)
                await delay(50)
        self.helperPlayers = helperPlayers
        return self

    def withRandomMotionPlayers(self, gameServerAddress, turnsToChangeDirection=60):
        self.gameServerAddress = gameServerAddress

        async def helperPlayers(gameServerAddress):
            for i in range(1, 12):
                await newZombieHelperPlayer(Team.Side.HOME, i, gameServerAddress, turnsToChangeDirection)
                await delay(50)
                await newZombieHelperPlayer(Team.Side.AWAY, i, gameServerAddress, turnsToChangeDirection)
                await delay(50)
        self.helperPlayers = helperPlayers
        return self
