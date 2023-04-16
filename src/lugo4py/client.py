import grpc

import traceback
from typing import Callable, Awaitable

from .protos.physics_pb2 import Point, Vector
from .protos import server_pb2
from .protos import server_pb2_grpc as server_grpc

from .stub import Bot, PLAYER_STATE
from .loader import EnvVarLoader
from .snapshot import defineState

PROTOCOL_VERSION = "1.0.0"

RawTurnProcessor = Callable[[
    server_pb2.OrderSet, server_pb2.GameSnapshot], Awaitable[server_pb2.OrderSet]]


class LugoClient(server_grpc.GameServicer):

    def __init__(self, server_add, grpc_insecure, token, teamSide, number, init_position):
        self.callback = Callable[[
            server_pb2.GameSnapshot], server_pb2.OrderSet]
        self.serverAdd = server_add
        self.grpc_insecure = grpc_insecure
        self.token = token
        self.teamSide = teamSide
        self.number = number
        self.init_position = init_position

    def set_client(self, client: server_grpc.GameStub):
        self._client = client

    def set_initial_position(self, initial_position: Point):
        self.init_position = initial_position

    def getting_ready_handler(self, snapshot: server_pb2.GameSnapshot):
        print(f'Default getting ready handler called for {snapshot}')

    def setReadyHandler(self, newReadyHandler):
        self.getting_ready_handler = newReadyHandler

    async def play(self, callback: Callable[[server_pb2.GameSnapshot], server_pb2.OrderSet], on_join: Callable[[], None]):
        self.callback = callback
        await self._bot_start(callback, on_join)

    async def play_as_bot(self, bot: Bot, on_join: Callable[[], None]):
        self.setReadyHandler(bot.gettingReady)

        async def processor(orders: server_pb2.OrderSet, snapshot: server_pb2.GameSnapshot) -> server_pb2.OrderSet:
            playerState = defineState(
                snapshot, self.number, self.teamSide)
            if self.number == 1:
                orders = bot.asGoalkeeper(
                    orders, snapshot, playerState)
            else:
                if playerState == PLAYER_STATE.DISPUTING_THE_BALL:
                    # print(f"[turn #{snapshot.turn}] will call disputing")
                    orders = bot.onDisputing(orders, snapshot)
                elif playerState == PLAYER_STATE.DEFENDING:
                    # print(f"[turn #{snapshot.turn}] will call defending")
                    orders = bot.onDefending(orders, snapshot)
                elif playerState == PLAYER_STATE.SUPPORTING:
                    # print(f"[turn #{snapshot.turn}] will call supporting")
                    orders = bot.onSupporting(orders, snapshot)
                elif playerState == PLAYER_STATE.HOLDING_THE_BALL:
                    # print(f"[turn #{snapshot.turn}] will call holding")
                    orders = bot.onHolding(orders, snapshot)
            return orders
        await self._bot_start(processor, on_join)

    async def _bot_start(self, processor: RawTurnProcessor, on_join: Callable[[], None]) -> None:

        if self.grpc_insecure:
            channel = grpc.insecure_channel(self.serverAdd)
        else:
            channel = grpc.secure_channel(
                self.serverAdd, grpc.ssl_channel_credentials())
        try:
            grpc.channel_ready_future(channel).result(timeout=15)
        except grpc.FutureTimeoutError:
            raise Exception("timed out waiting to connect to the game server")

        self.channel = channel
        self._client = server_grpc.GameStub(channel)

        # joint to the team
        join_request = server_pb2.JoinRequest(
            token=self.token,
            team_side=self.teamSide,
            number=self.number,
            init_position=self.init_position,
        )
        on_join()
        print("joint to the team")
        for snapshot in self._client.JoinATeam(join_request):
            try:
                if snapshot.state == server_pb2.GameSnapshot.State.OVER:
                    print(f" All done! {server_pb2.GameSnapshot.State.OVER}")
                    break

                elif snapshot.state == server_pb2.GameSnapshot.State.LISTENING:
                    orders = server_pb2.OrderSet()
                    orders.turn = snapshot.turn

                    try:
                        orders = await processor(orders, snapshot)
                    except Exception as e:
                        print("bot error", e)

                    if orders:
                        self._client.SendOrders(orders)
                    else:
                        print(
                            f"[turn #{snapshot.turn}] bot did not return orders")
                elif snapshot.state == server_pb2.GameSnapshot.State.GET_READY:
                    await self.getting_ready_handler(snapshot)

            except Exception as e:
                print("internal error processing turn", e)
                traceback.print_exc()


def NewClientFromConfig(config: EnvVarLoader, initialPosition: Point) -> LugoClient:
    return LugoClient(
        config.getGrpcUrl(),
        config.getGrpcInsecure(),
        config.getBotToken(),
        config.getBotTeamSide(),
        config.getBotNumber(),
        initialPosition,
    )
