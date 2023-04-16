import asyncio
from ..mapper import Mapper
from ..client import NewClientFromConfig, RawTurnProcessor
from ..protos import server_pb2 as lugo_server_pb2
from ..protos import remote_pb2 as lugo_remote_pb2
from ..snapshot import GameSnapshotReader
import os
from ..loader import EnvVarLoader
from typing import Callable, Awaitable


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


async def create_bot(teamSide, playerNumber, gameServerAddress, turnHandler: RawTurnProcessor, on_join_callback: Callable[[], Awaitable[None]]):
    try:
        map = Mapper(22, 5, teamSide)
        initialRegion = map.getRegion(
            PLAYER_POSITIONS[playerNumber]['Col'], PLAYER_POSITIONS[playerNumber]['Row'])

        os.environ["BOT_GRPC_URL"] = gameServerAddress
        os.environ["BOT_GRPC_INSECURE"] = "true"
        os.environ["BOT_TEAM"] = "HOME" if teamSide == lugo_server_pb2.Team.Side.HOME else "AWAY"
        os.environ["BOT_NUMBER"] = str(playerNumber)
        os.environ["BOT_TOKEN"] = ""

        config = EnvVarLoader()
        lugoClient = NewClientFromConfig(config, initialRegion.getCenter())
        await lugoClient.play(turnHandler, on_join_callback)
    except Exception as e:
        raise e


async def newZombiePlayer(teamSide, playerNumber, gameServerAddress):
    async def turnHandler(orderSet: lugo_remote_pb2.OrderSet, snapshot: lugo_server_pb2.GameSnapshot) -> lugo_remote_pb2.OrderSet:
        orderSet.setDebugMessage(
            f"{ 'HOME' if teamSide == 0 else 'AWAY' }-{playerNumber} #{snapshot.getTurn()}")
        return orderSet

    await create_bot(teamSide, playerNumber, gameServerAddress, turnHandler, my_on_join)


async def newChaserHelperPlayer(teamSide, playerNumber, gameServerAddress):
    async def turnHandler(orderSet: lugo_remote_pb2.OrderSet, snapshot: lugo_server_pb2.GameSnapshot) -> lugo_remote_pb2.OrderSet:
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
    async def turnHandler(orderSet: lugo_server_pb2.OrderSet, snapshot: lugo_server_pb2.GameSnapshot) -> lugo_server_pb2.OrderSet:
        orderSet.setDebugMessage(
            f"{ 'HOME' if teamSide == 0 else 'AWAY' }-{playerNumber} #{snapshot.getTurn()}")
        return orderSet

    await create_bot(teamSide, playerNumber, gameServerAddress, turnHandler, my_on_join)


async def newCustomHelperPlayer(teamSide, playerNumber, gameServerAddress, turnHandler: RawTurnProcessor):
    await create_bot(teamSide, playerNumber, gameServerAddress, turnHandler, my_on_join)


async def my_on_join():
    print("Client connecting to server")
