import contextlib
import grpc
import time
from typing import Any, Dict, Tuple, List

from ... import Bot, Team, GameSnapshotInspector, Order
from ...protos.remote_pb2_grpc import RemoteStub
from ...protos.rl_assistant_pb2 import RLResetConfig, PlayerOrdersOnRLSession, PlayersOrders
from ...protos.rl_assistant_pb2_grpc import RLAssistant
from ...rl.src.contracts import BotTrainer
from ...src.define_state import define_state, PLAYER_STATE


class TrainingCrl:
    def __init__(self, trainer: BotTrainer, bots: Dict[Tuple[Team.Side.ValueType, int], Bot], remote: RemoteStub,
                 assistant: RLAssistant,
                 normal_speed: bool = False
                 ):
        self.remote = remote
        self.assistant = assistant
        self.trainer = trainer
        self.latest_snapshot = None
        self.bots = bots
        self.normal_speed = normal_speed

    def set_environment(self, data: Any) -> None:
        try:
            self.latest_snapshot = self.trainer.create_new_initial_state(data)
        except Exception as e:
            raise RuntimeError(f"Failed to set environment: {e}")

        try:
            self.assistant.ResetEnv(request=RLResetConfig())
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
            complete_list = self.ensure_all_players_have_orders(players_orders.players_orders,
                                                                players_orders.default_behaviour)

            complete_play_orders = PlayersOrders()
            complete_play_orders.default_behaviour = players_orders.default_behaviour
            complete_play_orders.players_orders.extend(complete_list)

            turn_outcome = self.assistant.SendPlayersOrders(complete_play_orders)
        except grpc.RpcError as e:
            raise RuntimeError(f"RL assistant failed to send the orders: {e}")

        if self.normal_speed:
            time.sleep(.05)
        previous_snapshot = self.latest_snapshot
        self.latest_snapshot = turn_outcome.game_snapshot
        return self.trainer.evaluate(previous_snapshot, turn_outcome.game_snapshot, turn_outcome)

    def ensure_all_players_have_orders(self, player_orders_list, default_behaviour):
        result = {(order.team_side, order.number): order for order in player_orders_list}

        for number in range(1, 12):  # Player numbers 1 to 11
            # Home team
            key = (Team.Side.HOME, number)
            if key not in result:
                if (Team.Side.HOME, number) in self.bots:
                    result[key] = self.create_new_order_from_bot(self.bots[Team.Side.HOME, number], Team.Side.HOME, number,
                                                             default_behaviour)

            # Away team
            key = (Team.Side.AWAY, number)
            if key not in result:
                if (Team.Side.AWAY, number) in self.bots:
                    result[key] = self.create_new_order_from_bot(self.bots[Team.Side.AWAY, number], Team.Side.AWAY, number,
                                                             default_behaviour)

        return list(result.values())

    def create_new_order_from_bot(self, bot: Bot, team_side: Team.Side, number: int,
                                  default_behaviour) -> PlayerOrdersOnRLSession:
        inspector = GameSnapshotInspector(team_side, number, self.latest_snapshot)

        player_state = define_state(inspector, number, team_side)
        orders: List[Order] = []
        if number == 1:
            orders = bot.as_goalkeeper(inspector, player_state)
        else:
            if player_state == PLAYER_STATE.DISPUTING_THE_BALL:
                orders = bot.on_disputing(inspector)
            elif player_state == PLAYER_STATE.DEFENDING:
                orders = bot.on_defending(inspector)
            elif player_state == PLAYER_STATE.SUPPORTING:
                orders = bot.on_supporting(inspector)
            elif player_state == PLAYER_STATE.HOLDING_THE_BALL:
                orders = bot.on_holding(inspector)

        new_order = PlayerOrdersOnRLSession()
        new_order.team_side = team_side
        new_order.number = number
        new_order.behaviour = default_behaviour
        new_order.orders.extend(orders)
        return new_order
