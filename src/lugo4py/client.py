import grpc
import json
import os
import random
import threading
import asyncio
import datetime
import traceback
from typing import Tuple, Callable, Awaitable, Any
import time

from .protos.physics_pb2 import Point, Vector
from .protos import server_pb2
from .protos import server_pb2_grpc as server_grpc

from .stub import Bot, PLAYER_STATE
from .loader import EnvVarLoader
from .snapshot import defineState

PROTOCOL_VERSION = "1.0.0"

RawTurnProcessor = Callable[[Any, Any], Awaitable[Any]]

class LugoClient(server_grpc.GameServicer):

    def __init__(self, server_add, grpc_insecure, token, teamSide, number, init_position):
        self.callback = Callable[[server_pb2.GameSnapshot], server_pb2.OrderSet]
        self.serverAdd = server_add
        self.grpc_insecure = grpc_insecure
        self.token = token
        self.teamSide = teamSide
        self.number = number
        self.init_position = init_position

        self._client = _get_client()

    def set_client(self, client: server_grpc.GameStub):
        self._client = client

    def set_initial_position(self, initial_position: Point):
        self.init_position = initial_position

    def getting_ready_handler(self, snapshot : server_pb2.GameSnapshot):
        print(f'Default getting ready handler called for {snapshot}')

    def setReadyHandler(self, newReadyHandler):
        self.getting_ready_handler = newReadyHandler

    async def play(self, callback: Callable[[server_pb2.GameSnapshot], server_pb2.OrderSet]):
        self.callback = callback
        team = os.environ.get("BOT_TEAM").upper()
        number = int(os.environ.get("BOT_NUMBER"))
        token = os.environ.get("BOT_TOKEN")

        join_request = server_pb2.JoinRequest(
            token=token,
            team_side=server_pb2.Team.Side.Value(team),
            number=number,
            init_position=self.initial_position,
        )

        retries = 3
        for i in range(retries):
            try:
                await self._init( join_request)
            except Exception as e:
                print(e)
                time.sleep(1)

    
    async def _init(self, join_request: server_pb2.JoinRequest) -> None:
        for snapshot in self._client.JoinATeam(join_request):
            try:
                if snapshot.state == server_pb2.GameSnapshot.State.OVER:
                    break 

                elif snapshot.state == server_pb2.GameSnapshot.State.LISTENING:
                    
                    orders = self.callback(snapshot)

                    if orders:
                        self._client.SendOrders(orders)
                        pass
                    else:
                        print(f"[turn #{snapshot.turn}] bot did not return orders")

                elif snapshot.state == server_pb2.GameSnapshot.State.GET_READY:
                    await self.getting_ready_handler(snapshot)

            except Exception as e:
                print("internal error processing turn", e)
                traceback.print_exc()


    async def play_as_bot(self, bot: Bot):
        join_request = server_pb2.JoinRequest(token = self.token, team_side = self.teamSide, number = self.number, init_position = self.init_position)
        # join_request = server_pb2.JoinRequest({'token':self.token,  'team_side' : self.teamSide, 'number' : self.number, 'init_position': self.init_position})
        print(join_request)

        retries = 3
        for i in range(retries):
            try:
                await self._bot_start(bot, join_request)
            except Exception as e:
                print(e)
                traceback.print_exc()
                time.sleep(1)



    async def _bot_start(self, bot: Bot, join_request: server_pb2.JoinRequest) -> None:
        print("Bot Starting")
        for snapshot in self._client.JoinATeam(join_request):
            try:
                if snapshot.state == server_pb2.GameSnapshot.State.OVER:
                    break 

                elif snapshot.state == server_pb2.GameSnapshot.State.LISTENING:

                    playerState = defineState(snapshot, self.number, self.teamSide)
                    orders = server_pb2.OrderSet()

                    if (self.number == 1):
                        orders = bot.asGoalkeeper(orders, snapshot, playerState)

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

                    if orders:
                        self._client.SendOrders(orders)

                    else:
                        print(f"[turn #{snapshot.turn}] bot did not return orders")

                elif snapshot.state == server_pb2.GameSnapshot.State.GET_READY:
                    await bot.gettingReady(snapshot)

            except Exception as e:
                print("internal error processing turn", e)
                traceback.print_exc()

    @classmethod
    def new_client(cls, initial_position: Point) -> 'LugoClient':
        instance = cls()
        instance.set_initial_position(initial_position)
        client = _get_client()
        instance.set_client(client)
        return instance

def NewClientFromConfig(config: EnvVarLoader, initialPosition: Point) -> LugoClient:
    return LugoClient(
        config.getGrpcUrl(),
        config.getGrpcInsecure(),
        config.getBotToken(),
        config.getBotTeamSide(),
        config.getBotNumber(),
        initialPosition,
    )

def _get_config() -> Tuple[str, bool]:
    url = os.environ.get("BOT_GRPC_URL")
    if url is None:
        raise Exception("BOT_GRPC_URL is not set")
    insecure = os.environ.get("BOT_GRPC_INSECURE", "false").lower() == "true"
    return url, insecure


def _get_client() -> server_grpc.GameStub:
    url, insecure = _get_config()
    if insecure:
        channel = grpc.insecure_channel(url)
    else:
        channel = grpc.secure_channel(url, grpc.ssl_channel_credentials())
    return server_grpc.GameStub(channel)

