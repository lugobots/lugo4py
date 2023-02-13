import sys
import os
import asyncio

# both src are necessary to account for execution on docker and on project folder
sys.path.append("../../src")
sys.path.append("./src")

from lugo4py.mapper import Mapper
from lugo4py.client import LugoClient
from lugo4py import rl
from lugo4py.protos import server_pb2
from my_bot import MyBotTrainer, PLAYER_NUM

# training settings
trainIterations = 500
gamesPerIteration = 10
maxStepsPerGame = 60
hiddenLayerSizes = [4, 4]
learningRate = 0.95
discountRate = 0.05
testingGames = 20

grpcAddress = "localhost:5000"
grpcInsecure = True
model_path = 'file: ./model_output'

async def myTrainingFunction(trainingCtrl: rl.TrainingController) :
    print("Let's start training")
    policyNet = None
    
    await trainingCtrl.stop()

async def async_main():
    teamSide = server_pb2.Team.Side.HOME
    playerNumber = PLAYER_NUM

    # the map will help us to see the field in quadrants (called regions) instead of working with coordinates
    map = Mapper(10, 6, server_pb2.Team.Side.HOME)

    # our bot strategy defines our bot initial position based on its number
    initialRegion = map.getRegion(1, 1)

    # now we can create the bot. We will use a shortcut to create the client from the config, but we could use the
    # client constructor as well
    lugoClient = LugoClient(
        grpcAddress,
        grpcInsecure,
        "",
        teamSide,
        playerNumber,
        initialRegion.getCenter())

    rc = rl.RemoteControl()
    await rc.connect(grpcAddress)

    bot = MyBotTrainer(rc)
    gym = rl.Gym(rc, bot, myTrainingFunction, debugging_log = False)

    await gym.withZombiePlayers(grpcAddress).start(lugoClient)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())
    loop.close()