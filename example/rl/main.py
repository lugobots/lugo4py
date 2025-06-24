import random
import signal
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor
import sys

from training_func import my_training_function

sys.path.append("../..")
from src.lugo4py.rl import *
from example.rl import my_bot

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

    bot = my_bot.MyBotTrainer(gym.remote)

    gym.start(bot, my_training_function)

    def signal_handler(_, __):
        print("Stop requested\n")
        stop.set()
        gym_executor.shutdown(wait=True, cancel_futures=True)
        print("All stopped\n")

    signal.signal(signal.SIGINT, signal_handler)
    stop.wait()
