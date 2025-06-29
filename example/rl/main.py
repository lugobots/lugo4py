import os
import signal
import threading
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', 'src')))

from lugo4py import Team
from training_func import my_training_function
from src.lugo4py.rl import ThreadPoolExecutor, Gym

from example.rl import trainer
from example.simple.my_bot import MyBot

# Training settings
train_iterations = 50
steps_per_iteration = 600

grpc_address = "localhost:5000"
grpc_insecure = True

stop = threading.Event()

if __name__ == "__main__":
    gym_executor = ThreadPoolExecutor()

    # Now we can create the Gym, which will control all async work and allow us to focus on the learning part
    gym = Gym(gym_executor, grpc_address)

    gym.create_team_bots(Team.Side.HOME, lambda conf: MyBot(
        conf.get_bot_team_side(),
        conf.get_bot_number(),
        conf.get_initial_position(),
        conf.get_mapper()
    ))

    gym.create_team_bots(Team.Side.AWAY, lambda conf: MyBot(
        conf.get_bot_team_side(),
        conf.get_bot_number(),
        conf.get_initial_position(),
        conf.get_mapper()
    ))

    trainerBot = trainer.MyBotTrainer(gym.remote)

    gym.start(trainerBot,
              my_training_function)


    def signal_handler(_, __):
        print("Stop requested\n")
        stop.set()
        gym_executor.shutdown(wait=True, cancel_futures=True)
        print("All stopped\n")


    signal.signal(signal.SIGINT, signal_handler)
    stop.wait()
