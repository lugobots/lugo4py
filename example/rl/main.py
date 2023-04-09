import random
from my_bot import MyBotTrainer, TRAINING_PLAYER_NUMBER
from lugo4py.protos import server_pb2
from lugo4py.rl.training_controller import TrainingController
from lugo4py.rl.gym import Gym
from lugo4py.client import LugoClient
from lugo4py.rl.remote_control import RemoteControl
from lugo4py.mapper import Mapper
from lugo4py.snapshot import DIRECTION
from typing import Tuple, Callable, Awaitable, Any
import grpc
import asyncio
import os
from lugo4py.loader import EnvVarLoader


def set_environment_variables():
    os.environ["BOT_GRPC_URL"] = "localhost:5000"
    os.environ["BOT_GRPC_INSECURE"] = "true"
    os.environ["BOT_NUMBER"] = str(TRAINING_PLAYER_NUMBER)
    os.environ["BOT_TEAM"] = "home"


set_environment_variables()

env_loader = EnvVarLoader()

# Training settings
train_iterations = 50
steps_per_iteration = 240

grpc_address = "localhost:5000"
grpc_insecure = True


async def main():
    team_side = server_pb2.Team.Side.HOME

    # The map will help us see the field in quadrants (called regions) instead of working with coordinates
    # The Mapper will translate the coordinates based on the side the bot is playing on
    map = Mapper(20, 10, server_pb2.Team.Side.HOME)

    # Our bot strategy defines our bot initial position based on its number
    initial_region = map.getRegion(5, 4)

    # Now we can create the bot. We will use a shortcut to create the client from the config, but we could use the
    # client constructor as well
    lugo_client = LugoClient(
        grpc_address,
        grpc_insecure,
        "",
        team_side,
        TRAINING_PLAYER_NUMBER,
        initial_region.getCenter())

    # The RemoteControl is a gRPC client that will connect to the Game Server and change the element positions
    rc = RemoteControl()
    await rc.connect(grpc_address)  # Pass address here

    bot = MyBotTrainer(rc)

    # Now we can create the Gym, which will control all async work and allow us to focus on the learning part
    gym = Gym(rc, bot, my_training_function, {"debugging_log": False})

    # First, starting the game server
    # If you want to train playing against another bot, then you should start the other team first.
    # If you want to train using two teams, you should start the away team, then start the training bot, and finally start the home team
    # await gym.start(lugo_client)

    # If you want to train controlling all players, use the with_zombie_players players to create zombie players.
    await gym.withZombiePlayers(grpc_address).start(lugo_client)

    # If you want to train against bots running randomly, you can use this helper
    # await gym.with_random_motion_players(grpc_address, 10).start(lugo_client)

    # If you want to train against bots chasing the ball, you can use this helper
    # await gym.with_chasers_players(grpc_address).start(lugo_client)


async def my_training_function(training_ctrl: TrainingController):
    print("Let's train")

    possible_actions = [
        DIRECTION.FORWARD,
        DIRECTION.BACKWARD,
        DIRECTION.LEFT,
        DIRECTION.RIGHT,
        DIRECTION.BACKWARD_LEFT,
        DIRECTION.BACKWARD_RIGHT,
        DIRECTION.FORWARD_RIGHT,
        DIRECTION.FORWARD_LEFT,
    ]
    scores = []
    for i in range(train_iterations):
        try:
            scores.append(0)
            await training_ctrl.set_environment({"iteration": i})

            for j in range(steps_per_iteration):
                sensors = await training_ctrl.get_state()

                # The sensors would feed our training model, which would return the next action
                action = possible_actions[random.randint(
                    0, len(possible_actions) - 1)]

                # Then we pass the action to our update method
                reward, done = await training_ctrl.update(action)
                # Now we should reward our model with the reward value
                scores[i] += reward
                if done:
                    # No more steps
                    print(f"End of train_iteration {i}, score:", scores[i])
                    break

        except Exception as e:
            print("Error:", e)

    await training_ctrl.stop()
    print("Training is over, scores:", scores)

if __name__ == "__main__":
    asyncio.run(main())
