from ... import Team, Point, Mapper


class Configurator:
    def __init__(self, team_side: Team.Side, number: int, initial_position: Point, mapper: Mapper):
        self._team_side = team_side
        self._number = number
        self._initial_position = initial_position
        self._mapper = mapper

    def get_bot_team_side(self) -> Team.Side:
        return self._team_side

    def get_bot_number(self) -> int:
        return self._number

    def get_initial_position(self) -> Point:
        return self._initial_position

    def get_mapper(self) -> Mapper:
        return self._mapper
