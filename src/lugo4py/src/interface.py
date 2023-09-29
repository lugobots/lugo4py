from ..src import lugo, snapshot
from ..mapper import Mapper
from abc import ABC, abstractmethod


class PlayerState(object):
    SUPPORTING = 0
    HOLDING_THE_BALL = 1
    DEFENDING = 2
    DISPUTING_THE_BALL = 3


PLAYER_STATE = PlayerState()


class Bot(ABC):
    def __init__(self, side: lugo.TeamSide, number: int, init_position: lugo.Point, my_mapper: Mapper):
        self.number = number
        self.side = side
        self.mapper = my_mapper
        self.initPosition = init_position

    @abstractmethod
    def on_disputing(self, order_set: lugo.OrderSet, game_snapshot: lugo.GameSnapshot) -> lugo.OrderSet:
        pass

    @abstractmethod
    def on_defending(self, order_set: lugo.OrderSet, game_snapshot: lugo.GameSnapshot) -> lugo.OrderSet:
        pass

    @abstractmethod
    def on_holding(self, order_set: lugo.OrderSet, game_snapshot: lugo.GameSnapshot) -> lugo.OrderSet:
        pass

    @abstractmethod
    def on_supporting(self, order_set: lugo.OrderSet, game_snapshot: lugo.GameSnapshot) -> lugo.OrderSet:
        pass

    @abstractmethod
    def as_goalkeeper(self, order_set: lugo.OrderSet, game_snapshot: lugo.GameSnapshot, state: PLAYER_STATE) -> lugo.OrderSet:
        pass

    @abstractmethod
    def getting_ready(self, game_snapshot: lugo.GameSnapshot):
        pass

    def make_reader(self, game_snapshot: lugo.GameSnapshot):
        reader = snapshot.GameSnapshotReader(game_snapshot, self.side)
        me = reader.get_player(self.side, self.number)
        if me is None:
            raise AttributeError("did not find myself in the game")

        return reader, me
