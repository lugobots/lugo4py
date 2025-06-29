import contextlib
import traceback
from concurrent.futures import ThreadPoolExecutor

import grpc
import time
from typing import Any, Iterator, Callable

from .configuator import Configurator
from ... import GameSnapshot, Remote, RemoteStub, log_with_time, Bot, Team, Point, Mapper, TeamSide
from ...protos.rl_assistant_pb2 import RLSessionConfig
from ...protos.rl_assistant_pb2_grpc import RLAssistantStub
from ...rl.src.training_controller import TrainingCrl
from ...rl.src.contracts import BotTrainer, TrainingFunction
from ...src.utils.defaults import DEFAULT_PLAYER_POSITIONS, DEFAULT_MAPPER_COLS, DEFAULT_MAPPER_ROWS

Maker = Callable[[Configurator], Bot]

class Gym:

    def __init__(self, executor: ThreadPoolExecutor,  grpc_address):

        channel = grpc.insecure_channel(grpc_address)

        # Block until channel is ready (or timeout)
        grpc.channel_ready_future(channel).result(timeout=5)

        self.remote = RemoteStub(channel)
        self.assistant = RLAssistantStub(channel)
        self.executor = executor
        self.my_bots = {}

    def create_team_bots(self, team: TeamSide, factory: Maker):
        default_mapper = Mapper(DEFAULT_MAPPER_COLS, DEFAULT_MAPPER_ROWS, team)

        for number in range(1, 12):  # Player numbers 1 to 11
            configurator = Configurator(
                team,
                number,
                default_mapper.get_region(DEFAULT_PLAYER_POSITIONS[number]["Col"], DEFAULT_PLAYER_POSITIONS[number]["Row"]).get_center(),
                default_mapper
            )
            self.my_bots[(team, number)] = factory(configurator)


    def start(self, trainer: BotTrainer, training_function: TrainingFunction, normal_speed: bool = False) -> None:

        training_ctrl = TrainingCrl(trainer, self.my_bots, self.remote, self.assistant, normal_speed)

        response_iterator = self.assistant.StartSession(request=RLSessionConfig())


        self._training_routine = self.executor.submit(self._response_watcher, response_iterator)


        time.sleep(2)
        training_function(training_ctrl)

    def _response_watcher(
        self,
        response_iterator: Iterator[GameSnapshot],
        ) -> None:
        try:
            for snapshot in response_iterator:
                log_with_time(f"still alive")

            # self._play_finished.set()
        except grpc.RpcError as e:
            if grpc.StatusCode.INVALID_ARGUMENT == e.code():
                log_with_time(f"did not connect to RL session {e.details()}")
        except Exception as e:
            log_with_time(f"internal error processing RL session: {e}")
            traceback.print_exc()
