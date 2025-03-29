import contextlib
import grpc
import time
from typing import Any

from src.lugo4py.protos.remote_pb2_grpc import Remote
from src.lugo4py.protos.rl_assistant_pb2 import RLSessionConfig
from src.lugo4py.protos.rl_assistant_pb2_grpc import RLAssistant
from src.lugo4py.rl import TrainingCrl


class Gym:
    def __init__(self, grpc_conn: grpc.Channel):
        self.grpc_conn = grpc_conn
        self.logger = lambda msg: print(f'set debugger')
        self.assistant = RLAssistant(grpc_conn)
        self.remote = Remote(grpc_conn)

    @classmethod
    def new_gym(cls, config: "Config", logger: Logger) -> tuple["Gym", Remote]:
        options = [grpc.insecure_channel(config.grpc_address)]

        with contextlib.suppress(Exception):
            ctx = grpc.insecure_channel(config.grpc_address)
            grpc_conn = grpc.blocking_channel(ctx)
            logger.debug("Trying to connect to the server")
            return cls(grpc_conn, logger), Remote(grpc_conn)

        raise ConnectionError("Did not connect to the game server")

    def start(self, ctx: Any, trainer: "BotTrainer", training_function: "TrainingFunction") -> None:
        self.grpc_conn.close()
        training_ctrl = TrainingCrl(ctx, trainer, self.remote, self.assistant)

        self.logger.debug("Starting training session")
        session = self.assistant.StartSession(ctx, RLSessionConfig())

        if session.Context().Err():
            raise RuntimeError("Could not start a training session")

        def keep_alive():
            while True:
                try:
                    session.Recv()
                except grpc.RpcError as err:
                    self.logger.error(f"The RL assistant session ended with error: {err}")
                    return

        self.logger.info("Session started")
        training_function(training_ctrl)
