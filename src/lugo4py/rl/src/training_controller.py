import contextlib
import grpc
import time
from typing import Any

from src.lugo4py.protos.remote_pb2_grpc import Remote
from src.lugo4py.protos.rl_assistant_pb2 import RLResetConfig
from src.lugo4py.protos.rl_assistant_pb2_grpc import RLAssistant
from src.lugo4py.rl.src.contracts import BotTrainer


class TrainingCrl:
    def __init__(self, ctx: Any, trainer: BotTrainer, remote: Remote, assistant: RLAssistant):
        self.remote = remote
        self.assistant = assistant
        self.training_context = ctx
        self.trainer = trainer
        self.latest_snapshot = None

    def set_environment(self, data: Any) -> None:
        try:
            self.latest_snapshot = self.trainer.create_new_initial_state(data)
        except Exception as e:
            raise RuntimeError(f"Failed to set environment: {e}")

        with grpc.insecure_channel(self.assistant) as channel:
            ctx = grpc.blocking_channel(channel)
            time.sleep(10)  # Simulating timeout

            print("**** Environment reset ******")
            try:
                self.assistant.ResetEnv(ctx, RLResetConfig())
            except grpc.RpcError as e:
                raise RuntimeError(f"Failed to reset RL assistant: {e}")

    def get_state(self) -> Any:
        return self.trainer.get_training_state(self.latest_snapshot)

    def update(self, action: Any) -> tuple[float, bool]:
        try:
            players_orders = self.trainer.play(self.latest_snapshot, action)
        except Exception as e:
            raise RuntimeError(f"Trainer bot failed to play: {e}")

        try:
            turn_outcome = self.assistant.SendPlayersOrders(self.training_context, players_orders)
        except grpc.RpcError as e:
            raise RuntimeError(f"RL assistant failed to send the orders: {e}")

        previous_snapshot = self.latest_snapshot
        self.latest_snapshot = turn_outcome.game_snapshot
        return self.trainer.evaluate(previous_snapshot, turn_outcome.game_snapshot, turn_outcome)