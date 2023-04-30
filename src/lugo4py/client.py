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
    server_pb2.OrderSet, server_pb2.GameSnapshot], server_pb2.OrderSet]

# reference https://chromium.googlesource.com/external/github.com/grpc/grpc/+/master/examples/python/async_streaming/client.py
class LugoClient(server_grpc.GameServicer):

    def __init__(self, server_add, grpc_insecure, token, teamSide, number, init_position):
        self.callback = Callable[[
            server_pb2.GameSnapshot], server_pb2.OrderSet]
        self.serverAdd = server_add + "?t=" + str(teamSide) + "-" + str(number)
        self.grpc_insecure = grpc_insecure
        self.token = token
        self.teamSide = teamSide
        self.number = number
        self.init_position = init_position
        self._play_finished = threading.Event()
        self._play_routine = None

    def set_client(self, client: server_grpc.GameStub):
        self._client = client

    def get_name(self):
        return f"{'HOME' if self.teamSide == 0 else 'AWAY'}-{self.number}"

    def set_initial_position(self, initial_position: Point):
        self.init_position = initial_position

    def getting_ready_handler(self, snapshot: server_pb2.GameSnapshot):
        print(f'Default getting ready handler called for ')

    def setReadyHandler(self, newReadyHandler):
        self.getting_ready_handler = newReadyHandler

    def play(self, executor: ThreadPoolExecutor, callback: Callable[[server_pb2.GameSnapshot], server_pb2.OrderSet], on_join: Callable[[], None]) -> threading.Event:
        self.callback = callback
        log_with_time(f"{self.get_name()} Starting to play")
        return self._bot_start(executor, callback, on_join)

    def play_as_bot(self, executor: ThreadPoolExecutor, bot: Bot, on_join: Callable[[], None]) -> threading.Event:
        self.setReadyHandler(bot.gettingReady)
        log_with_time(f"{self.get_name()} Playing as bot")

        def processor(orders: server_pb2.OrderSet, snapshot: server_pb2.GameSnapshot) -> server_pb2.OrderSet:
            playerState = defineState(
                snapshot, self.number, self.teamSide)
            if self.number == 1:
                orders = bot.asGoalkeeper(
                    orders, snapshot, playerState)
            else:
                if playerState == PLAYER_STATE.DISPUTING_THE_BALL:
                    orders = bot.onDisputing(orders, snapshot)
                elif playerState == PLAYER_STATE.DEFENDING:
                    orders = bot.onDefending(orders, snapshot)
                elif playerState == PLAYER_STATE.SUPPORTING:
                    orders = bot.onSupporting(orders, snapshot)
                elif playerState == PLAYER_STATE.HOLDING_THE_BALL:
                    orders = bot.onHolding(orders, snapshot)
            return orders
        return self._bot_start(executor, processor, on_join)

    def _bot_start(self, executor: ThreadPoolExecutor, processor: RawTurnProcessor, on_join: Callable[[], None]) -> threading.Event:
        log_with_time(f"{self.get_name()} Starting bot {self.teamSide}-{self.number}")
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

        response_iterator = self._client.JoinATeam(join_request)

        log_with_time(f"{self.get_name()} Joint to the team")
        on_join()
        self._play_routine = executor.submit(self._response_watcher, response_iterator, processor)
        return self._play_finished

    def stop(self):
        log_with_time(f"{self.get_name()} stopping bot - you may need to kill the process if there is no messages coming from the server")
        self._play_finished.set()

    def wait(self):
        self._play_finished.wait(timeout=None)

    def _response_watcher(
            self,
            response_iterator: Iterator[server_pb2.GameSnapshot],
            # snapshot,
            processor: RawTurnProcessor) -> None:
        try:
            for snapshot in response_iterator:
                if snapshot.state == server_pb2.GameSnapshot.State.OVER:
                    log_with_time(
                        f"{self.get_name()} All done! {server_pb2.GameSnapshot.State.OVER}")
                    break
                elif self._play_finished.is_set():
                    break
                elif snapshot.state == server_pb2.GameSnapshot.State.LISTENING:
                    orders = server_pb2.OrderSet()
                    orders.turn = snapshot.turn
                    try:
                        orders = processor(orders, snapshot)
                    except Exception as e:
                        traceback.print_exc()
                        log_with_time(f"{self.get_name()}bot processor error: {e}")

                    if orders:
                        self._client.SendOrders(orders)
                    else:
                        log_with_time(
                            f"{self.get_name()} [turn #{snapshot.turn}] bot {self.teamSide}-{self.number} did not return orders")
                elif snapshot.state == server_pb2.GameSnapshot.State.GET_READY:
                    self.getting_ready_handler(snapshot)

            self._play_finished.set()
        except Exception as e:
            log_with_time(f"{self.get_name()} internal error processing turn: {e}")
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


def log_with_time(msg):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{current_time}: {msg}")
