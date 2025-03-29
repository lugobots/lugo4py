from src.lugo4py.protos.rl_assistant_pb2 import PlayersOrders, PlayerOrdersOnRLSession
from src.lugo4py.protos.server_pb2 import Order


class PlayersOrdersSet:
    def __init__(self, default_bot_behaviour: str):
        self.players_orders = PlayersOrders(default_behaviour=default_bot_behaviour)

    def add_order(self, player_number: int, team_side: Any, orders: List[Order]) -> PlayersOrdersSet:
        self.players_orders.players_orders.append(
            PlayerOrdersOnRLSession(
                team_side=team_side,
                number=player_number,
                orders=orders,
            )
        )
        return self

    def set_player_behaviour(self, player_number: int, team_side: Any, behaviour: str) -> PlayersOrdersSet:
        self.players_orders.players_orders.append(
            PlayerOrdersOnRLSession(
                team_side=team_side,
                number=player_number,
                behaviour=behaviour,
            )
        )
        return self

    def build(self) -> PlayersOrders:
        return self.players_orders