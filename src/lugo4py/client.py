import grpc
import json
import os
import random
import threading
import asyncio
import datetime
from typing import Tuple, Callable, Awaitable, Any

from .protos import physics_pb2
from .protos import server_pb2
from .protos import server_pb2_grpc as server_grpc

from . import stub
from . import configurator
from . import game_snapshot

RawTurnProcessor = Callable[[Any, Any], Awaitable[Any]]

class LugoClient(server_grpc.GameServicer):
    _client: server_grpc.GameStub
    _initial_position: physics_pb2.Point
    callback: Callable[[server_pb2.GameSnapshot], server_pb2.OrderSet]

    def set_client(self, client: server_grpc.GameStub):
        self._client = client

    def set_initial_position(self, initial_position: physics_pb2.Point):
        self._initial_position = initial_position

    def play(self, callback: Callable[[server_pb2.GameSnapshot], server_pb2.OrderSet]):
        self._callback = callback
        team = os.environ.get("BOT_TEAM").upper()
        number = int(os.environ.get("BOT_NUMBER"))
        token = os.environ.get("BOT_TOKEN")

        join_request = server_pb2.JoinRequest(
            token=token,
            team_side=server_pb2.Team.Side.Value(team),
            number=number,
            init_position=self._initial_position,
        )

        thread = threading.Thread(target=self._init, args=(join_request,))
        thread.start()

    def _init(self, join_request: server_pb2.JoinRequest) -> None:
        for snapshot in self._client.JoinATeam(join_request):
            try:
                if snapshot.state == server_pb2.GameSnapshot.State.OVER:
                    break 

                elif snapshot.state == server_pb2.GameSnapshot.State.LISTENING:
                    
                    orders = self._callback(snapshot)

                    if orders:
                        self._client.SendOrders(orders)
                        pass
                    else:
                        print(f"[turn #{snapshot.turn}] bot did not return orders")

                elif snapshot.state == server_pb2.GameSnapshot.State.GET_READY:
                    # await self.getting_ready_handler(snapshot)
                    pass

            except Exception as e:
                print("internal error processing turn", e)
            

    @classmethod
    def new_client(cls, initial_position: physics_pb2.Point) -> 'LugoClient':
        instance = cls()
        instance.set_initial_position(initial_position)
        client = _get_client()
        instance.set_client(client)
        return instance


def _get_config() -> Tuple[str, bool]:
    url = os.environ.get("BOT_GRPC_URL")
    if url is None:
        raise Exception("BOT_GRPC_URL is not set")
    insecure = os.environ.get("BOT_GRPC_INSECURE", "false").lower() == "true"
    return url, True


def _get_client() -> server_grpc.GameStub:
    url, insecure = _get_config()
    if insecure:
        channel = grpc.insecure_channel(url)
    else:
        channel = grpc.secure_channel(url, grpc.ssl_channel_credentials())
    return server_grpc.GameStub(channel)

