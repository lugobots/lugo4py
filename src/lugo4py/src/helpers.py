from .lugo import GameSnapshot, Player, TeamSide

def get_ball_holder(snapshot: GameSnapshot):
    holder = snapshot.ball.holder
    return holder if holder is not None else None

def is_ball_holder(snapshot: GameSnapshot, player: Player):
    holder = snapshot.ball.holder
    return holder is not None and holder.team_side == player.team_side and holder.number == player.number

def get_team(snapshot: GameSnapshot, side: TeamSide):
    if side == TeamSide.HOME:
        return snapshot.home_team
    else: return snapshot.away_team


def get_player(snapshot: GameSnapshot, side: TeamSide, number: int):
    team = get_team(snapshot, side)
    if team:
        for current_player in team.players:
            if current_player.number == number:
                return current_player
    return None

def get_opponent_side(side: TeamSide):
    return TeamSide.AWAY if side == TeamSide.HOME else TeamSide.HOME


