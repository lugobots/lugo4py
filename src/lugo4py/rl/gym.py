import time

from .training_controller import TrainingCrl
from .helper_bots import newChaserHelperPlayer, newZombieHelperPlayer
from .remote_control import RemoteControl
from .interfaces import BotTrainer, TrainingFunction
from ..client import LugoClient
from ..protos.server_pb2 import Team, OrderSet
import asyncio
from threading import Timer
import threading

from concurrent.futures import ThreadPoolExecutor

class Gym:

    def __init__(
            self,
            executor: ThreadPoolExecutor,
            remote_control: RemoteControl,
            trainer: BotTrainer,
            trainingFunction: TrainingFunction,
            options=None,
    ):
        if options is None:
            options = {"debugging_log": False}

        self.remoteControl = remote_control
        self.trainingCrl = TrainingCrl(executor,
            remote_control, trainer, trainingFunction)
        self.trainingCrl.debugging_log = options["debugging_log"]
        self.gameServerAddress = None
        self.helperPlayers = None

    def start(self, lugoClient: LugoClient, executor: ThreadPoolExecutor):
        hasStarted = False

        def play_callback(orderSet, snapshot):
            # print('22222222222\n')
            nonlocal hasStarted
            hasStarted = True
            return self.trainingCrl.gameTurnHandler(orderSet, snapshot)

        def trigger_listening() -> None:
            nonlocal hasStarted
            if hasStarted is False:
                waiterResumeListening = threading.Event()
                executor.submit(self.remoteControl.resumeListening, waiterResumeListening)
                waiterResumeListening.wait()

        def on_join() -> None:
            print('The main bot is connected!! Starting to connect the zombies\n')
            time.sleep(0.2)
            if self.gameServerAddress:
                self.helperPlayers(self.gameServerAddress, executor)
            # print('helpers are done\n')
            trigger_listening()
            # print('Bhaa\n')
            # exp = Timer(3.0, trigger_listening, ())
            # exp.start()

        lugoClient.play(executor, play_callback, on_join)
        return lugoClient


    def withZombiePlayers(self, game_server_address):
        print('Entering withZombiePlayers\n')
        self.gameServerAddress = game_server_address
        self.helperPlayers = create_helper_players
        return self

    def withChasersPlayers(self, game_server_address):
        self.gameServerAddress = game_server_address

        def helper_players(game_server_address):
            for i in range(1, 12):
                newChaserHelperPlayer(Team.Side.HOME, i, game_server_address)
                delay(50)
                newChaserHelperPlayer(Team.Side.AWAY, i, game_server_address)
                delay(50)

        self.helperPlayers = helper_players(game_server_address)
        return self


def create_helper_players(gameServerAddress: str, executor: ThreadPoolExecutor):
    tasks = []

    # await newZombieHelperPlayer(Team.Side.HOME, 1, gameServerAddress)
    # group = asyncio.gather(newZombieHelperPlayer(Team.Side.AWAY, 1, gameServerAddress))
    # group = asyncio.gather(group, newZombieHelperPlayer(Team.Side.AWAY, 2, gameServerAddress))
    for i in range(0, 11):
        time.sleep(0.1)
        newZombieHelperPlayer(Team.Side.HOME, i + 1, gameServerAddress, executor)
        time.sleep(0.1)
        newZombieHelperPlayer(Team.Side.AWAY, i + 1, gameServerAddress, executor)

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
