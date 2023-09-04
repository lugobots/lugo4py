from ..src import lugo
from abc import ABC, abstractmethod


class PlayerState(object):
    SUPPORTING = 0
    HOLDING_THE_BALL = 1
    DEFENDING = 2
    DISPUTING_THE_BALL = 3


PLAYER_STATE = PlayerState()


class Bot(ABC):
    @abstractmethod
    def on_disputing(self, order_set: lugo.OrderSet, snapshot: lugo.GameSnapshot) -> lugo.OrderSet:
        pass

    @abstractmethod
    def on_defending(self, order_set: lugo.OrderSet, snapshot: lugo.GameSnapshot) -> lugo.OrderSet:
        pass

    @abstractmethod
    def on_holding(self, order_set: lugo.OrderSet, snapshot: lugo.GameSnapshot) -> lugo.OrderSet:
        pass

    @abstractmethod
    def on_supporting(self, order_set: lugo.OrderSet, snapshot: lugo.GameSnapshot) -> lugo.OrderSet:
        pass

    @abstractmethod
    def as_goalkeeper(self, order_set: lugo.OrderSet, snapshot: lugo.GameSnapshot, state: PLAYER_STATE) -> lugo.OrderSet:
        pass

    @abstractmethod
    def getting_ready(self, snapshot: lugo.GameSnapshot):
        pass
