import asyncio
from ..mapper import Mapper
from ..client import NewClientFromConfig, RawTurnProcessor
from ..protos.server_pb2 import GameSnapshot, OrderSet
from lugo4py.snapshot import GameSnapshotReader

PLAYER_POSITIONS = {
    1: {'Col': 0, 'Row': 1},
    2: {'Col': 1, 'Row': 1},
    3: {'Col': 2, 'Row': 1},
    4: {'Col': 3, 'Row': 1},
    5: {'Col': 4, 'Row': 1},
    6: {'Col': 5, 'Row': 1},
    7: {'Col': 6, 'Row': 1},
    8: {'Col': 7, 'Row': 1},
    9: {'Col': 8, 'Row': 1},
    10: {'Col': 9, 'Row': 1},
    11: {'Col': 10, 'Row': 1},
}


async def newZombiePlayer(teamSide, playerNumber, gameServerAddress):
    loop = asyncio.get_event_loop()
    promise = loop.create_future()
    try:
        map = Mapper(22, 5, teamSide)
        initialRegion = map.getRegion(
            PLAYER_POSITIONS[playerNumber]['Col'], PLAYER_POSITIONS[playerNumber]['Row'])
        lugoClient = NewClientFromConfig(
            gameServerAddress, True, "", teamSide, playerNumber, initialRegion.getCenter())

        async def turnHandler(orderSet: OrderSet, snapshot: GameSnapshot) -> OrderSet:
            orderSet.setDebugMessage(
                f"{ 'HOME' if teamSide == 0 else 'AWAY' }-{playerNumber} #{snapshot.getTurn()}")
            return orderSet
        await lugoClient.play(turnHandler, promise.set_result)
    except Exception as e:
        promise.set_exception(e)
    return promise


async def newChaserHelperPlayer(teamSide, playerNumber, gameServerAddress):
    async def turnHandler(orderSet: OrderSet, snapshot: GameSnapshot) -> OrderSet:
        reader = GameSnapshotReader(snapshot, teamSide)
        orderSet.addOrders(reader.makeOrderCatch())
        me = reader.getPlayer(teamSide, playerNumber)
        if not me:
            raise ValueError("did not find myself in the game")

        orderSet.addOrders(reader.makeOrderMoveMaxSpeed(
            me.getPosition(), snapshot.getBall().getPosition()))
        orderSet.setDebugMessage(
            f"{ 'HOME' if teamSide == 0 else 'AWAY' }-{playerNumber} #{snapshot.getTurn()} - chasing ball")
        return orderSet

    return newCustomHelperPlayer(teamSide, playerNumber, gameServerAddress, turnHandler)


async def newZombieHelperPlayer(teamSide, playerNumber, gameServerAddress):
    async def turnHandler(orderSet: OrderSet, snapshot: GameSnapshot) -> OrderSet:
        orderSet.setDebugMessage(
            f"{ 'HOME' if teamSide == 0 else 'AWAY' }-{playerNumber} #{snapshot.getTurn()}")
        return orderSet

    return await newCustomHelperPlayer(teamSide, playerNumber, gameServerAddress, turnHandler)


async def newCustomHelperPlayer(teamSide, playerNumber, gameServerAddress, turnHandler: RawTurnProcessor):
    try:
        map = Mapper(22, 5, teamSide)
        initialRegion = map.getRegion(
            PLAYER_POSITIONS[playerNumber]['Col'], PLAYER_POSITIONS[playerNumber]['Row'])
        lugoClient = NewClientFromConfig(
            gameServerAddress, True, "", teamSide, playerNumber, initialRegion.getCenter())
        await lugoClient.play(turnHandler)
    except Exception as e:
        raise e
