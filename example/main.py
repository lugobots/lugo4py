import sys
sys.path.append("../src")
sys.path.append("./src")

from lugo4py.loader import EnvVarLoader
from lugo4py.snapshot import GameSnapshotReader
from lugo4py.mapper import Mapper
# from lugo4py.client import NewClientFromConfig

from my_bot import MyBot

import os

from lugo4py.client import LugoClient
from lugo4py.protos import physics_pb2

PLAYER_POSITIONS = {
    1:  {'Col': 0, 'Row': 0},
    2:  {'Col': 1, 'Row': 1},
    3:  {'Col': 2, 'Row': 2},
    4:  {'Col': 2, 'Row': 3},
    5:  {'Col': 1, 'Row': 4},
    6:  {'Col': 3, 'Row': 1},
    7:  {'Col': 3, 'Row': 2},
    8:  {'Col': 3, 'Row': 3},
    9:  {'Col': 3, 'Row': 4},
    10: {'Col': 4, 'Row': 3},
    11: {'Col': 4, 'Row': 2},
}

if __name__ == "__main__":
    # We must load the env vars following the standard defined by the game specs because all bots will receive the
    # arguments in the same format (env vars)
    config = EnvVarLoader()

    # The map will help us to see the field in quadrants (called regions) instead of working with coordinates
    map = Mapper(10, 6, config.getBotTeamSide())

    # Our bot strategy defines our bot initial position based on its number
    initialRegion = map.getRegion(PLAYER_POSITIONS[config.getBotNumber()]['Col'], PLAYER_POSITIONS[config.getBotNumber()]['Row'])

    # Now we can create the bot. We will use a shortcut to create the client from the config, but we could use the
    # client constructor as well
    ##### lugoClient = NewClientFromConfig(config, initialRegion.getCenter())

    ####myBot = MyBot(config.getBotTeamSide(),config.getBotNumber(),initialRegion.getCenter(),map)

    # lugoClient.playAsBot(myBot).then(() => {
    #     console.log(`all done`)
    # }).catch(e => {
    #     console.error(e)
    # })
    print("All good!")