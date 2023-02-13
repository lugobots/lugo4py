from .protos.server_pb2 import GameSnapshot, OrderSet
from abc import ABC, abstractmethod

class PlayerState(object):
    SUPPORTING = 0
    HOLDING_THE_BALL = 1
    DEFENDING = 2
    DISPUTING_THE_BALL = 3 

PLAYER_STATE = PlayerState()

class Bot(ABC):
    @abstractmethod
    def onDisputing (self, orderSet: OrderSet, snapshot: GameSnapshot) -> OrderSet:
        pass

    @abstractmethod
    def onDefending (self, orderSet: OrderSet, snapshot: GameSnapshot) -> OrderSet:
        pass

    @abstractmethod
    def onHolding (self, orderSet: OrderSet, snapshot: GameSnapshot) -> OrderSet:
        pass

    @abstractmethod
    def onSupporting (self, orderSet: OrderSet, snapshot: GameSnapshot) -> OrderSet:
        pass

    @abstractmethod
    def asGoalkeeper (self, orderSet: OrderSet, snapshot: GameSnapshot, state: PLAYER_STATE) -> OrderSet:
        pass

    @abstractmethod
    def gettingReady (self, snapshot: GameSnapshot):
        pass



