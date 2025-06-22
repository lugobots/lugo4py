import random
import signal
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor
import sys

from training_func import my_training_function

sys.path.append("../..")
from src.lugo4py.rl.src.contracts import TrainingController
from src.lugo4py.src.lugo import *
from src.lugo4py.rl import *
from src.lugo4py.src import client
from src.lugo4py.mapper import DIRECTION, Mapper

from example.rl import my_bot

# Training settings
train_iterations = 50
steps_per_iteration = 600

grpc_address = "localhost:5000"
grpc_insecure = True

stop = threading.Event()

if __name__ == "__main__":
    # team_side = TeamSide.HOME
    # print('main: Training bot team side = ', team_side)
    # # The map will help us see the field in quadrants (called regions) instead of working with coordinates
    # # The Mapper will translate the coordinates based on the side the bot is playing on
    # mapper = Mapper(20, 10,  TeamSide.HOME)
    #
    # # Our bot strategy defines our bot initial position based on its number
    # initial_region = mapper.get_region(5, 4)
    #
    # # Now we can create the bot. We will use a shortcut to create the client from the config, but we could use the
    # # client constructor as well
    # lugo_client = client.LugoClient(
    #     grpc_address,
    #     grpc_insecure,
    #     "",
    #     team_side,
    #     my_bot.TRAINING_PLAYER_NUMBER,
    #     initial_region.get_center()
    # )
    # The RemoteControl is a gRPC client that will connect to the Game Server and change the element positions
    # rc = Remote()
    # rc.connect(grpc_address)  # Pass address here
    #


    gym_executor = ThreadPoolExecutor()
    # Now we can create the Gym, which will control all async work and allow us to focus on the learning part
    gym = Gym(gym_executor, grpc_address)

    bot = my_bot.MyBotTrainer(gym.remote)

    # players_executor = ThreadPoolExecutor(22)
    # here we are using zombie players, but you may also use another bot or other helping players.
    # read the main Readme file to find more ways to run other bots.
    # gym.with_zombie_players(grpc_address).start(lugo_client, players_executor)
    gym.start(bot, my_training_function)

    def signal_handler(_, __):
        print("Stop requested\n")
        gym_executor.shutdown(wait=True)
        stop.set()
        print("All stopped\n")


    signal.signal(signal.SIGINT, signal_handler)

    stop.wait()
