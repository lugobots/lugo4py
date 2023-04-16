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
        self.gameServerAddress = None

    async def start(self, lugoClient: LugoClient):
        if self.gameServerAddress:
            await self.helperPlayers(self, self.gameServerAddress)

        hasStarted = False

        async def play_callback(orderSet, snapshot):
            nonlocal hasStarted
            hasStarted = True
            return await self.trainingCrl.gameTurnHandler(orderSet, snapshot)
        await lugoClient.play(play_callback, my_on_join)

        asyncio.get_running_loop().call_later(
            1, lambda: self.remoteControl.resumeListening() if not hasStarted else None
        )

    async def withZombiePlayers(self, gameServerAddress, training_bot_number=None, training_team_side=None):
        print('Entering withZombiePlayers\n')
        self.helperPlayers = await create_helper_players(gameServerAddress, training_bot_number, training_team_side)
        return self

    async def withChasersPlayers(self, gameServerAddress):
        self.gameServerAddress = gameServerAddress

        async def helper_players(gameServerAddress):
            for i in range(1, 12):
                await newChaserHelperPlayer(Team.Side.HOME, i, gameServerAddress)
                await delay(50)
                await newChaserHelperPlayer(Team.Side.AWAY, i, gameServerAddress)
                await delay(50)

        self.helperPlayers = helper_players
        return self


async def create_helper_players(gameServerAddress: str, training_bot_number, training_team_side):
    tasks = []
    for i in range(1, 12):
        if i == training_bot_number and training_team_side is not None:
            if training_team_side == Team.Side.HOME:
                tasks.append(newZombieHelperPlayer(
                    Team.Side.AWAY, i, gameServerAddress))
            elif training_team_side == Team.Side.AWAY:
                tasks.append(newZombieHelperPlayer(
                    Team.Side.HOME, i, gameServerAddress))
            continue

        tasks.append(newZombieHelperPlayer(
            Team.Side.HOME, i, gameServerAddress))
        tasks.append(newZombieHelperPlayer(
            Team.Side.AWAY, i, gameServerAddress))

    return await asyncio.gather(*tasks)


async def my_on_join():
    print("Client connecting to server")
