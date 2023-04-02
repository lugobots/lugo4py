from lugo4py.loader import EnvVarLoader
from lugo4py.snapshot import GameSnapshotReader
from lugo4py.stub import Bot, PLAYER_STATE
# from lugo4py.client import NewClientFromConfig
from typing import Union

from lugo4py.protos import server_pb2 as Lugo
from lugo4py.protos import physics_pb2 as Physics
import random
import traceback
import time
import random
from typing import Any, Dict, Tuple
from lugo4py.snapshot import GameSnapshotReader, Mapper, Direction
from lugo4py.rl.remote_control import RemoteControl


TRAINING_PLAYER_NUMBER = 5
PLAYER_NUM = 11


class MyBotTrainer:
    def __init__(self, remote_control: RemoteControl):
        self.remote_control = remote_control
        self.Mapper = None

    async def createNewInitialState(self, data: Any) -> Lugo.GameSnapshot:
        self.Mapper = Mapper(20, 10, Lugo.Team.Side.HOME)

        for i in range(1, 12):
            await self._randomPlayerPos(self.Mapper, Lugo.Team.Side.HOME, i)
            await self._randomPlayerPos(self.Mapper, Lugo.Team.Side.AWAY, i)

        randomVelocity = Physics.Velocity()
        randomVelocity.setSpeed(0)
        randomVelocity.setDirection(Direction.NORTH)
        pos = self.Mapper.getRegion(10, random.randint(2, 7)).getCenter()
        await self.remote_control.setPlayerProps(Lugo.Team.Side.HOME, TRAINING_PLAYER_NUMBER, pos, randomVelocity)

        ball_pos = (0, 0)
        ball_velocity = Physics.Velocity()
        ball_velocity.setSpeed(0)
        ball_velocity.setDirection(Direction.NORTH)
        await self.remote_control.setTurn(1)
        return await self.remote_control.setBallProps(ball_pos, ball_velocity)

    def getState(self, snapshot: Lugo.GameSnapshot) -> Any:
        return [True, True, False]

    async def play(self, orderSet: Lugo.OrderSet, snapshot: Lugo.GameSnapshot, action: Any) -> Lugo.OrderSet:
        reader = GameSnapshotReader(snapshot, Lugo.Team.Side.HOME)
        dir = reader.makeOrderMoveByDirection(action)
        return orderSet.setOrdersList([dir])

    async def evaluate(self, previousSnapshot: Lugo.GameSnapshot, newSnapshot: Lugo.GameSnapshot) -> Dict[str, Union[int, bool]]:
        return {"done": newSnapshot.getTurn() >= 20, "reward": random.random()}

    async def _randomPlayerPos(self, Mapper: Mapper, side: Lugo.Team.Side, number: int) -> None:
        min_col = 10
        max_col = 17
        min_row = 1
        max_row = 8

        random_velocity = Physics.Velocity()
        random_velocity.setSpeed(0)
        random_velocity.setDirection(Direction.NORTH)

        random_col = random.randint(min_col, max_col)
        random_row = random.randint(min_row, max_row)
        random_position = Mapper.getRegion(random_col, random_row).getCenter()
        await self.remote_control.setPlayerProps(side, number, random_position, random_velocity)

    def find_opponent(reader):
        get_opponents = reader.get_team(
            reader.get_opponent_side()).get_players_list()
        mapped_opponents = []
        for opponent in get_opponents:
            opponent_region = Mapper.get_region_from_point(
                opponent.get_position())
            if mapped_opponents[opponent_region.get_col()] == None:
                mapped_opponents[opponent_region.get_col()] = []
            mapped_opponents[opponent_region.get_col(
            )][opponent_region.get_row()] = True
        return mapped_opponents

    def has_opponent(mapped_opponents, region):
        return (mapped_opponents[region.get_col()] != None and
                mapped_opponents[region.get_col()][region.get_row()] == True)

    def random_integer(min_val, max_val):
        return random.randint(min_val, max_val)

    def delay(ms):
        time.sleep(ms / 1000)
