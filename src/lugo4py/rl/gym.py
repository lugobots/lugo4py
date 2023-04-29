from .training_controller import TrainingCrl, delay
from .helper_bots import newChaserHelperPlayer, newZombieHelperPlayer
from .remote_control import RemoteControl
from .interfaces import BotTrainer, TrainingFunction
from ..client import LugoClient
from ..protos.server_pb2 import Team, OrderSet
import asyncio
from threading import Timer

from concurrent.futures import ThreadPoolExecutor

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

    async def start(self, lugoClient: LugoClient, executor: ThreadPoolExecutor):
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
                print('VAI\n')
                asyncio.run(self.remoteControl.resumeListening())
                print('FOI\n')

        async def on_join() -> None:
            print('The main bot is connected\n')
            # await asyncio.sleep(3)
            if self.gameServerAddress:
                await self.helperPlayers(self.gameServerAddress, executor)
            print('helpers are done\n')
            trigger_listening()
            # exp = Timer(3.0, trigger_listening, ())
            # exp.start()

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

async def coro1(i):
    # await asyncio.sleep(1)
    print(f"step 1 - {i}")
    # await asyncio.sleep(1)
    # print(f"step 2 - {i}")

async def create_helper_players(gameServerAddress: str, executor: ThreadPoolExecutor):
    tasks = []
    await asyncio.gather(*(newZombieHelperPlayer(Team.Side.AWAY, i+1, gameServerAddress, executor) for i in range(11)))
    # await newZombieHelperPlayer(Team.Side.HOME, 1, gameServerAddress)
    # group = asyncio.gather(newZombieHelperPlayer(Team.Side.AWAY, 1, gameServerAddress))
    # group = asyncio.gather(group, newZombieHelperPlayer(Team.Side.AWAY, 2, gameServerAddress))
    # for i in range(1, 12):
    print(f'PLEAYR =====================')
    #     if group is None:
    #         group = asyncio.gather(newZombieHelperPlayer(Team.Side.AWAY, i, gameServerAddress))
    #     else:
    #         group = asyncio.gather(group, newZombieHelperPlayer(Team.Side.AWAY, i, gameServerAddress))
    # tasks.append(newZombieHelperPlayer(Team.Side.AWAY, i, gameServerAddress))
    # asyncio.ensure_future()
    # tasks.append(newZombieHelperPlayer(Team.Side.HOME, i, gameServerAddress))
    # async io.ensure_future(newZombieHelperPlayer(Team.Side.HOME, i, gameServerAddress))

    # return await group



async def my_on_join():
    print("Client connecting to server")
