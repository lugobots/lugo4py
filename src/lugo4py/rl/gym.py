from .training_controller import TrainingCrl, delay
from .helper_bots import newZombiePlayer, newChaserHelperPlayer, newZombieHelperPlayer
from .remote_control import RemoteControl
from .interfaces import BotTrainer, TrainingFunction
from ..client import LugoClient
from ..protos.server_pb2 import Team, OrderSet
import asyncio


class Gym:

    def __init__(
        self,
        remote_control: RemoteControl,
        trainer: BotTrainer,
        trainingFunction: TrainingFunction,
        options=None,
    ):
        if options is None:
            options = {"debugging_log": False}

        self.remoteControl = remote_control
        self.trainingCrl = TrainingCrl(
            remote_control, trainer, trainingFunction)
        self.trainingCrl.debugging_log = options["debugging_log"]

    async def start(self, lugoClient: LugoClient):
        if self.gameServerAddress:
            await self.helperPlayers(self, self.gameServerAddress)

        hasStarted = False

        async def play_callback(orderSet, snapshot):
            nonlocal hasStarted
            hasStarted = True
            return await self.trainingCrl.gameTurnHandler(orderSet, snapshot)
        await lugoClient.play(play_callback)

        asyncio.get_running_loop().call_later(
            1, lambda: self.remoteControl.resumeListening() if not hasStarted else None
        )

    def withZombiePlayers(self, gameServerAddress):
        self.gameServerAddress = gameServerAddress

        async def helper_players(self, gameServerAddress: str):
            for i in range(1, 12):
                await newZombieHelperPlayer(
                    Team.Side.HOME, i, gameServerAddress)
                await newZombieHelperPlayer(
                    Team.Side.AWAY, i, gameServerAddress)

        self.helperPlayers = helper_players
        return self

    def withChasersPlayers(self, gameServerAddress):
        self.gameServerAddress = gameServerAddress

        async def helper_players(gameServerAddress):
            for i in range(1, 12):
                await newChaserHelperPlayer(Team.Side.HOME, i, gameServerAddress)
                await delay(50)
                await newChaserHelperPlayer(Team.Side.AWAY, i, gameServerAddress)
                await delay(50)

        self.helperPlayers = helper_players
        return self
