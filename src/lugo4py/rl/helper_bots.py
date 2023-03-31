from ..mapper import Mapper
from ..client import NewClientFromConfig
from ..protos.server_pb2 import GameSnapshot, OrderSet

import asyncio


PLAYER_POSITIONS = {
    1:  {'Col': 0, 'Row': 1},
    2:  {'Col': 1, 'Row': 1},
    3:  {'Col': 2, 'Row': 1},
    4:  {'Col': 3, 'Row': 1},
    5:  {'Col': 4, 'Row': 1},
    6:  {'Col': 5, 'Row': 1},
    7:  {'Col': 6, 'Row': 1},
    8:  {'Col': 7, 'Row': 1},
    9:  {'Col': 8, 'Row': 1},
    10: {'Col': 9, 'Row': 1},
    11: {'Col': 10, 'Row': 1},
}


def newZombiePlayer(teamSide, playerNumber, gameServerAddress):
    promise = asyncio.Future()
    # https://stackoverflow.com/questions/66940979/what-is-the-python-equivalent-of-a-promise-from-javascript
    pass
    
    # return new Promise<void>((resolve, reject) => {
    #     const map = new Mapper(22, 5, teamSide)
    #     const initialRegion = map.getRegion(PLAYER_POSITIONS[playerNumber].Col, PLAYER_POSITIONS[playerNumber].Row)
    #     const lugoClient = new Client(
    #         gameServerAddress,
    #         true,
    #         "",
    #         teamSide,
    #         playerNumber
    #         , initialRegion.getCenter())

    #     const turnHandler = (orderSet: OrderSet, snapshot: GameSnapshot) : Promise<OrderSet> => {
    #         return new Promise((r, j ) => {
    #             orderSet.setDebugMessage(`${teamSide === 0 ? 'HOME' : 'AWAY'}-${playerNumber} #${snapshot.getTurn()}`)
    #             r(orderSet);
    #         });
    #     }
    #     lugoClient.play(turnHandler, resolve).catch(e => {
    #       //  console.log(`[PLay] Zombie player ${teamSide === 0 ? 'HOME' : 'AWAY'}-${playerNumber} said: ${e.toString()}`)
    #         reject();
    #     })
    # })

