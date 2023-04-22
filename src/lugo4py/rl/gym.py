from .training_controller import TrainingCrl, delay
from .helper_bots import newChaserHelperPlayer, newZombieHelperPlayer
from .remote_control import RemoteControl
from .interfaces import BotTrainer, TrainingFunction
from ..client import LugoClient
from ..protos.server_pb2 import Team, OrderSet
import asyncio
from threading import Timer



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
        self.helperPlayers = None

    async def start(self, lugoClient: LugoClient):
        # print('BAAAAAAAA\n')

        hasStarted = False
        print('ZOOOOMBIES\n')
        async def play_callback(orderSet, snapshot):
            nonlocal hasStarted
            hasStarted = True
            return self.trainingCrl.gameTurnHandler(orderSet, snapshot)

        def trigger_listening() -> None:
            nonlocal hasStarted
            if hasStarted is False:
                # loop = asyncio.get_event_loop()
                asyncio.run(self.remoteControl.resumeListening())

        async def on_join() -> None:
            if self.gameServerAddress:
                self.helperPlayers(self.gameServerAddress)
            exp = Timer(1.0, trigger_listening, ())
            exp.start()

        await lugoClient.play(play_callback, on_join)


    async def withZombiePlayers(self, gameServerAddress, training_bot_number=None, training_team_side=None):
        print('Entering withZombiePlayers\n')
        self.gameServerAddress = gameServerAddress
        self.helperPlayers = create_helper_players
        return self

    async def withChasersPlayers(self, gameServerAddress):
        self.gameServerAddress = gameServerAddress

        async def helper_players(gameServerAddress):
            for i in range(1, 12):
                await newChaserHelperPlayer(Team.Side.HOME, i, gameServerAddress)
                await delay(50)
                await newChaserHelperPlayer(Team.Side.AWAY, i, gameServerAddress)
                await delay(50)

        self.helperPlayers = await helper_players(gameServerAddress)
        return self


def create_helper_players(gameServerAddress: str):

    # await newZombieHelperPlayer(Team.Side.HOME, 1, gameServerAddress)
    for i in range(1, 12):
        print(f'PLEAYR {i}\n')
        asyncio.ensure_future(newZombieHelperPlayer(Team.Side.AWAY, i, gameServerAddress))

    return



async def my_on_join():
    print("Client connecting to server")
