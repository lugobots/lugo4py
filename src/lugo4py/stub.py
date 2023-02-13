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
    def onDisputing (orderSet: OrderSet, snapshot: GameSnapshot) -> OrderSet:
        pass

    @abstractmethod
    def onDefending (orderSet: OrderSet, snapshot: GameSnapshot) -> OrderSet:
        pass

    @abstractmethod
    def onHolding (orderSet: OrderSet, snapshot: GameSnapshot) -> OrderSet:
        pass

    @abstractmethod
    def onSupporting (orderSet: OrderSet, snapshot: GameSnapshot) -> OrderSet:
        pass

    @abstractmethod
    def asGoalkeeper (orderSet: OrderSet, snapshot: GameSnapshot, state: PLAYER_STATE) -> OrderSet:
        pass

    @abstractmethod
    def gettingReady (snapshot: GameSnapshot):
        pass



