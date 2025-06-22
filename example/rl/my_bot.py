import random
import time
from typing import Any, List, Optional, Tuple
import sys

from src.lugo4py import PlayersOrders, TurnOutcome, GameSnapshotInspector
from src.lugo4py.mapper.src import mapper
from src.lugo4py.protos import server_pb2
from src.lugo4py.protos.physics_pb2 import Point
from src.lugo4py.protos.remote_pb2 import GameSnapshotRequest, PlayerProperties, CommandResponse
from src.lugo4py.protos.server_pb2 import Team

from src.lugo4py.rl.src.contracts import BotTrainer
from src.lugo4py.src.lugo import GameSnapshot

sys.path.append("../..")
from src.lugo4py.src import client, lugo
from src.lugo4py.rl import *
from src.lugo4py.mapper import *

TRAINING_PLAYER_NUMBER = 5

class MyBotTrainer(BotTrainer):
    def __init__(self, remote_control: Remote):
        remote_control.turn = remote_control
        self.remote_control = remote_control
        self.Mapper = None

    def create_new_initial_state(self, data: Any) -> GameSnapshot:

        player_prop = PlayerProperties()
        player_prop.number = 5
        player_prop.side = Team.HOME
        player_prop.position.x = 5000
        player_prop.position.y = 6000

        response = self.remote_control.SetPlayerProperties(player_prop)
        return response.game_snapshot

    def get_training_state(self, snapshot: GameSnapshot) -> Any:
        # TODO explain this
        return [True, True, False]

    def play(self, game_snapshot: GameSnapshot, action: Any) -> PlayersOrders:
        inspector = GameSnapshotInspector(lugo.TeamSide.HOME, 5, game_snapshot)
        orders = inspector.make_order_move_by_direction(action)

        player_orders = PlayerOrdersOnRLSession(
            team_side=lugo.TeamSide.HOME,
            number=5,
        )

        player_orders.orders.append(orders)

        response = PlayersOrders()
        response.default_behaviour = "statues"
        response.players_orders.append(player_orders)
        return response

    def evaluate(self, previous_game_snapshot: GameSnapshot, new_game_snapshot: GameSnapshot, turn_outcome: TurnOutcome    ) -> Tuple[float, bool]:
        return random.random(), new_game_snapshot.turn >= 600


def _create_velocity(speed: float, direction) -> lugo.Velocity:
    velocity = lugo.new_velocity(direction)
    velocity.speed = speed
    return velocity


def delay(ms: float) -> None:
    time.sleep(ms / 1000)


def random_integer(min_val: int, max_val: int) -> int:
    return random.randint(min_val, max_val)
