from .protos.server_pb2 import GameSnapshot, OrderSet
from abc import ABC, abstractmethod
from typing import Void

PLAYER_STATE  = ["supporting", "holding","defending","disputing"]

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
    def gettingReady (snapshot: GameSnapshot) -> Void :
        pass



