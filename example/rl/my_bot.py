import random
import time
from typing import Any, List, Optional

from src.lugo4py import orientation, lugo
from src.lugo4py.mapper import Mapper, Region
from src.lugo4py.rl.interfaces import BotTrainer
from src.lugo4py.rl.remote_control import RemoteControl
from src.lugo4py.snapshot import GameSnapshotReader

TRAINING_PLAYER_NUMBER = 5


class MyBotTrainer(BotTrainer):
    def __init__(self, remote_control: RemoteControl):
        self.remote_control = remote_control
        self.Mapper = None

    def set_environment(self, data: Any):
        self.Mapper = Mapper(20, 10, lugo.TeamSide.HOME)

        for i in range(1, 12):
            self._random_player_pos(self.Mapper, lugo.TeamSide.HOME, i)
            self._random_player_pos(self.Mapper, lugo.TeamSide.AWAY, i)

        random_velocity = _create_velocity(0, orientation.NORTH)
        pos = self.Mapper.get_region(10, random.randint(2, 7)).get_center()
        self.remote_control.set_player_props(lugo.TeamSide.HOME, TRAINING_PLAYER_NUMBER, pos, random_velocity)

        ball_pos = self.Mapper.get_region(0, 0).get_center()
        ball_velocity = _create_velocity(0, orientation.NORTH)
        self.remote_control.set_game_props(1)
        return self.remote_control.set_ball_rops(ball_pos, ball_velocity).game_snapshot

    def get_state(self, snapshot: lugo.GameSnapshot):
        return [True, True, False]

    def play(self, order_set: lugo.OrderSet, snapshot: lugo.GameSnapshot, action: Any) -> lugo.OrderSet:
        reader = GameSnapshotReader(snapshot, lugo.TeamSide.HOME)
        direction = reader.make_order_move_by_direction(action)
        order_set.orders.extend([direction])
        return order_set

    def evaluate(self, previous_snapshot: lugo.GameSnapshot, new_snapshot: lugo.GameSnapshot) -> Any:
        return {"done": new_snapshot.turn >= 600, "reward": random.random()}

    def _random_player_pos(self, mapper: Mapper, side: lugo.TeamSide, number: int) -> None:
        min_col = 10
        max_col = 17
        min_row = 1
        max_row = 8

        random_velocity = _create_velocity(0, orientation.NORTH)

        random_col = random.randint(min_col, max_col)
        random_row = random.randint(min_row, max_row)
        random_position = mapper.get_region(random_col, random_row).get_center()
        self.remote_control.set_player_props(side, number, random_position, random_velocity)

    def find_opponent(self, reader: GameSnapshotReader) -> List[List[bool]]:
        opponents = reader.get_team(
            reader.get_opponent_side()).players
        mapped_opponents = self._create_empty_mapped_opponents()

        for opponent in opponents:
            opponent_region = self.Mapper.get_region_from_point(
                opponent.position)
            col, row = opponent_region.get_col(), opponent_region.get_row()
            mapped_opponents[col][row] = True

        return mapped_opponents

    def _create_empty_mapped_opponents(self) -> List[List[Optional[bool]]]:
        mapped_opponents = []
        for _ in range(self.Mapper.get_num_cols()):
            mapped_opponents.append([None] * self.Mapper.get_num_rows())
        return mapped_opponents

    def has_opponent(self, mapped_opponents: List[List[bool]], region: Region) -> bool:
        col, row = region.get_col(), region.get_row()
        return mapped_opponents[col][row] is True


def _create_velocity(speed: float, direction) -> lugo.Velocity:
    velocity = lugo.new_velocity(direction)
    velocity.speed = speed
    return velocity


def delay(ms: float) -> None:
    time.sleep(ms / 1000)


def random_integer(min_val: int, max_val: int) -> int:
    return random.randint(min_val, max_val)
