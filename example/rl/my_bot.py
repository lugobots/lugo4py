from src.lugo4py.loader import EnvVarLoader
from src.lugo4py.snapshot import GameSnapshotReader, Mapper, Direction, Region
from src.lugo4py.stub import Bot
from src.lugo4py.protos import server_pb2 as Lugo
from src.lugo4py.protos.server_pb2 import GameSnapshot
from src.lugo4py.protos import physics_pb2 as Physics
from src.lugo4py.rl.remote_control import RemoteControl
import random
import time
from typing import Any, Dict, Tuple, Union, List, Optional

TRAINING_PLAYER_NUMBER = 5


class MyBotTrainer:
    def __init__(self, remote_control: RemoteControl):
        self.remote_control = remote_control
        self.Mapper = None

    async def createNewInitialState(self, data: Any) -> GameSnapshot:
        self.Mapper = Mapper(20, 10, Lugo.Team.Side.HOME)

        await self._place_players_on_field()

        await self._set_training_player_properties()

        return await self._initialize_ball()

    async def _place_players_on_field(self):
        for i in range(1, 12):
            await self._randomPlayerPos(self.Mapper, Lugo.Team.Side.HOME, i)
            await self._randomPlayerPos(self.Mapper, Lugo.Team.Side.AWAY, i)

    async def _set_training_player_properties(self):
        random_velocity = self._create_velocity(0, Direction.NORTH)
        pos = self.Mapper.getRegion(10, random.randint(2, 7)).getCenter()
        await self.remote_control.setPlayerProps(Lugo.Team.Side.HOME, TRAINING_PLAYER_NUMBER, pos, random_velocity)

    async def _initialize_ball(self):
        ball_pos = (0, 0)
        ball_velocity = self._create_velocity(0, Direction.NORTH)
        await self.remote_control.setTurn(1)
        return await self.remote_control.setBallProps(ball_pos, ball_velocity)

    def getState(self, snapshot: GameSnapshot) -> Any:
        return [True, True, False]

    async def play(self, orderSet: Lugo.OrderSet, snapshot: GameSnapshot, action: Any) -> Lugo.OrderSet:
        reader = GameSnapshotReader(snapshot, Lugo.Team.Side.HOME)
        dir = reader.makeOrderMoveByDirection(action)
        return orderSet.setOrdersList([dir])

    async def evaluate(self, previousSnapshot: GameSnapshot, newSnapshot: GameSnapshot) -> Dict[str, Union[int, bool]]:
        return {"done": newSnapshot.getTurn() >= 20, "reward": random.random()}

    async def _randomPlayerPos(self, Mapper: Mapper, side: Lugo.Team.Side, number: int) -> None:
        min_col = 10
        max_col = 17
        min_row = 1
        max_row = 8

        random_velocity = self._create_velocity(0, Direction.NORTH)

        random_col = random.randint(min_col, max_col)
        random_row = random.randint(min_row, max_row)
        random_position = Mapper.getRegion(random_col, random_row).getCenter()
        await self.remote_control.setPlayerProps(side, number, random_position, random_velocity)

    def _create_velocity(self, speed: float, direction: Direction) -> Physics.Velocity:
        velocity = Physics.Velocity()
        velocity.setSpeed(speed)
        velocity.setDirection(direction)
        return velocity

    def find_opponent(self, reader: GameSnapshotReader) -> List[List[bool]]:
        opponents = reader.get_team(
            reader.get_opponent_side()).get_players_list()
        mapped_opponents = self._create_empty_mapped_opponents()

        for opponent in opponents:
            opponent_region = self.Mapper.get_region_from_point(
                opponent.get_position())
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

    def random_integer(self, min_val: int, max_val: int) -> int:
        return random.randint(min_val, max_val)

    def delay(self, ms: float) -> None:
        time.sleep(ms / 1000)
