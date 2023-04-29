import asyncio

import grpc
import time
from concurrent.futures import ThreadPoolExecutor
import traceback
from typing import Callable, Awaitable, Iterator

from .protos.physics_pb2 import Point, Vector
from .protos import server_pb2
from .protos import server_pb2_grpc as server_grpc

from .stub import Bot, PLAYER_STATE
from .loader import EnvVarLoader
from .snapshot import defineState
import threading

PROTOCOL_VERSION = "1.0.0"

RawTurnProcessor = Callable[[
    server_pb2.OrderSet, server_pb2.GameSnapshot], Awaitable[server_pb2.OrderSet]]


class LugoClient(server_grpc.GameServicer):

    def __init__(self, server_add, grpc_insecure, token, teamSide, number, init_position, executor: ThreadPoolExecutor):
        self.callback = Callable[[
            server_pb2.GameSnapshot], server_pb2.OrderSet]
        self.serverAdd = server_add + "?t=" + str(teamSide) + "-" + str(number)
        self.grpc_insecure = grpc_insecure
        self.token = token
        self.teamSide = teamSide
        self.number = number
        self.init_position = init_position
        self._call_finished = threading.Event()
        self.executor = executor

    def set_client(self, client: server_grpc.GameStub):
        self._client = client

    def set_initial_position(self, initial_position: Point):
        self.init_position = initial_position

    def getting_ready_handler(self, snapshot: server_pb2.GameSnapshot):
        print(f'Default getting ready handler called for ')

    def setReadyHandler(self, newReadyHandler):
        self.getting_ready_handler = newReadyHandler

    async def play(self, callback: Callable[[server_pb2.GameSnapshot], server_pb2.OrderSet], on_join: Callable[[], Awaitable[None]]):
        self.callback = callback
        log_with_time("Starting to play")
        await self._bot_start(callback, on_join)

    async def play_as_bot(self, bot: Bot, on_join: Callable[[], Awaitable[None]]):
        self.setReadyHandler(bot.gettingReady)
        log_with_time("Playing as bot")

        async def processor(orders: server_pb2.OrderSet, snapshot: server_pb2.GameSnapshot) -> server_pb2.OrderSet:
            playerState = defineState(
                snapshot, self.number, self.teamSide)
            log_with_time(
                f"Processing orders for player {self.number} with state {playerState}")
            if self.number == 1:
                orders = bot.asGoalkeeper(
                    orders, snapshot, playerState)
            else:
                if playerState == PLAYER_STATE.DISPUTING_THE_BALL:
                    log_with_time(
                        f"[turn #{snapshot.turn}] will call disputing")
                    orders = bot.onDisputing(orders, snapshot)
                elif playerState == PLAYER_STATE.DEFENDING:
                    log_with_time(
                        f"[turn #{snapshot.turn}] will call defending")
                    orders = bot.onDefending(orders, snapshot)
                elif playerState == PLAYER_STATE.SUPPORTING:
                    log_with_time(
                        f"[turn #{snapshot.turn}] will call supporting")
                    orders = bot.onSupporting(orders, snapshot)
                elif playerState == PLAYER_STATE.HOLDING_THE_BALL:
                    log_with_time(f"[turn #{snapshot.turn}] will call holding")
                    orders = bot.onHolding(orders, snapshot)
            return orders
        await self._bot_start(processor, on_join)

    async def _bot_start(self, processor: RawTurnProcessor, on_join: Callable[[], Awaitable[None]]) -> None:
        log_with_time("Starting bot")
        if self.grpc_insecure:
            channel = grpc.insecure_channel(self.serverAdd)
        else:
            channel = grpc.secure_channel(
                self.serverAdd, grpc.ssl_channel_credentials())
        try:
            grpc.channel_ready_future(channel).result(timeout=30)
        except grpc.FutureTimeoutError:
            raise Exception("timed out waiting to connect to the game server")

        self.channel = channel
        self._client = server_grpc.GameStub(channel)

        join_request = server_pb2.JoinRequest(
            token=self.token,
            team_side=self.teamSide,
            number=self.number,
            init_position=self.init_position,
        )
        await on_join()

        response_iterator = self._client.JoinATeam(join_request)

        log_with_time("Joint to the team")

        # def wrapper(coro):
        #     log_with_time("BBB")
        #     return asyncio.run(coro)
        # await asyncio.gather(self._response_watcher(response_iterator, processor))
        # executor = ThreadPoolExecutor()
        # await self._response_watcher(response_iterator, processor)
        log_with_time("AAAAA")

        # self.executor.map(wrapper, response_iterator)
        asyncio.ensure_future(self._response_watcher(response_iterator, processor))
        # coros = [ for snapshot in response_iterator]
        # for r in self.executor.map(wrapper, coros):
        #     print(r, time.ctime())
        # self._consumer_future = self.executor.submit(self._response_watcher, response_iterator, processor)
        # log_with_time("BBB")
        # self._consumer_future.result()
        await asyncio.sleep(100)
        # log_with_time("CCCCCC")
        # self._call_finished.wait(timeout=None)
        # log_with_time("DDDD")
        # for snapshot in self._client.JoinATeam(join_request):
        #     log_with_time(f"Snapshot state: {snapshot.state}")
        #     try:
        #         if snapshot.state == server_pb2.GameSnapshot.State.OVER:
        #             log_with_time(
        #                 f" All done! {server_pb2.GameSnapshot.State.OVER}")
        #             break
        #         elif snapshot.state == server_pb2.GameSnapshot.State.LISTENING:
        #             orders = server_pb2.OrderSet()
        #             orders.turn = snapshot.turn
        #             try:
        #                 orders = await processor(orders, snapshot)
        #             except Exception as e:
        #                 log_with_time(f"bot error: {e}")
        #
        #             if orders:
        #                 self._client.SendOrders(orders)
        #             else:
        #                 log_with_time(
        #                     f"[turn #{snapshot.turn}] bot did not return orders")
        #         elif snapshot.state == server_pb2.GameSnapshot.State.GET_READY:
        #             log_with_time(f"[turn #{snapshot.turn}] getting ready")
        #             await self.getting_ready_handler(snapshot)
        #
        #     except Exception as e:
        #         log_with_time(f"internal error processing turn: {e}")
        #         traceback.print_exc()

    async def _response_watcher(
            self,
            response_iterator: Iterator[server_pb2.GameSnapshot],
            # snapshot,
            processor: RawTurnProcessor) -> None:
        try:
            log_with_time("ME CHAMOU??")
            await asyncio.sleep(3)
            # Essa porra desser FOR ta fudendo TUDO!!
            log_with_time("listening")
            # Talvez essa merda aqui ajude https://chromium.googlesource.com/external/github.com/grpc/grpc/+/master/examples/python/async_streaming/client.py

            for snapshot in response_iterator:
                log_with_time("Got snapshot")
                if snapshot.state == server_pb2.GameSnapshot.State.OVER:
                    log_with_time(
                        f" All done! {server_pb2.GameSnapshot.State.OVER}")
                    break
                elif snapshot.state == server_pb2.GameSnapshot.State.LISTENING:
                    orders = server_pb2.OrderSet()
                    orders.turn = snapshot.turn
                    try:
                        orders = await processor(orders, snapshot)
                    except Exception as e:
                        log_with_time(f"bot error: {e}")

                    if orders:
                        self._client.SendOrders(orders)
                    else:
                        log_with_time(
                            f"[turn #{snapshot.turn}] bot did not return orders")
                elif snapshot.state == server_pb2.GameSnapshot.State.GET_READY:
                    log_with_time(f"[turn #{snapshot.turn}] getting ready")
                    self.getting_ready_handler(snapshot)
            # self._call_finished.set()
        except Exception as e:
            log_with_time(f"internal error processing turn: {e}")
            traceback.print_exc()

def NewClientFromConfig(config: EnvVarLoader, initialPosition: Point) -> LugoClient:
    log_with_time("Creating a new client from config")
    return LugoClient(
        config.getGrpcUrl(),
        config.getGrpcInsecure(),
        config.getBotToken(),
        config.getBotTeamSide(),
        config.getBotNumber(),
        initialPosition,
    )


def log_with_time(msg: str):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{current_time}: {msg}")
