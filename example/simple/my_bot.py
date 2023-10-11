import traceback
from abc import ABC


import src.lugo4py as lugo4py
import src.lugo4py.mapper as mapper

class MyBot(lugo4py.Bot, ABC):

    def is_near(self, region_origin: mapper.Region, dest_origin: mapper.Region) -> bool:
        max_distance = 2
        return abs(region_origin.get_row() - dest_origin.get_row()) <= max_distance and abs(
            region_origin.get_col() - dest_origin.get_col()) <= max_distance

    def on_disputing(self, order_set: lugo4py.OrderSet, snapshot: lugo4py.GameSnapshot) -> lugo4py.OrderSet:
        try:
            # the Lugo.GameSnapshot helps us to read the game state
            (reader, me) = self.make_reader(snapshot)
            ball_position = reader.get_ball().position

            ball_region = self.mapper.get_region_from_point(ball_position)
            my_region = self.mapper.get_region_from_point(me.position)

            # by default, let's stay on our region  
            move_destination = get_my_expected_position(reader, self.mapper, self.number)
            order_set.debug_message = "Disputing: Returning to my position"

            # but if the ball is near to me, I will try to catch it
            if self.is_near(ball_region, my_region):
                move_destination = ball_position
                order_set.debug_message = "Disputing: Trying to catch the ball"

            move_order = reader.make_order_move_by_direction(lugo4py.DIRECTION_FORWARD)

            # we can ALWAYS try to catch the ball
            catch_order = reader.make_order_catch()

            order_set.turn = snapshot.turn
            order_set.orders.extend([move_order, catch_order])

            return order_set

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_defending(self, order_set: lugo4py.OrderSet, snapshot: lugo4py.GameSnapshot) -> lugo4py.OrderSet:
        try:
            (reader, me) = self.make_reader(snapshot)
            ball_position = snapshot.ball.position
            ball_region = self.mapper.get_region_from_point(ball_position)
            my_region = self.mapper.get_region_from_point(self.initPosition)

            # by default, I will stay at my tactic position
            move_dest = get_my_expected_position(reader, self.mapper, self.number)
            order_set.debug_message = "Defending: returning to my position"

            if self.is_near(ball_region, my_region):
                move_dest = ball_position
                order_set.debug_message = "Defending: trying to catch the ball"

            move_order = reader.make_order_move_max_speed(me.position, move_dest)
            catch_order = reader.make_order_catch()

            order_set.turn = snapshot.turn
            order_set.orders.extend([move_order, catch_order])
            return order_set
        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_holding(self, order_set: lugo4py.OrderSet, snapshot: lugo4py.GameSnapshot) -> lugo4py.OrderSet:
        try:
            (reader, me) = self.make_reader(snapshot)

            my_goal_center = self.mapper.get_region_from_point(reader.get_opponent_goal().get_center())
            current_region = self.mapper.get_region_from_point(me.position)

            if self.is_near(current_region, my_goal_center):
                my_order = reader.make_order_kick_max_speed(snapshot.ball, reader.get_opponent_goal().get_center())
            else:
                my_order = reader.make_order_move_max_speed(me.position, reader.get_opponent_goal().get_center())

            order_set.turn = snapshot.turn
            order_set.debug_message = "attack!"
            order_set.orders.append(my_order)
            return order_set

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_supporting(self, order_set: lugo4py.OrderSet, snapshot: lugo4py.GameSnapshot) -> lugo4py.OrderSet:
        try:
            (reader, me) = self.make_reader(snapshot)
            ball_holder_position = snapshot.ball.position
            ball_holder_region = self.mapper.get_region_from_point(ball_holder_position)
            my_region = self.mapper.get_region_from_point(self.initPosition)

            move_dest = get_my_expected_position(reader, self.mapper, self.number)

            if self.is_near(ball_holder_region, my_region):
                move_dest = ball_holder_position

            move_order = reader.make_order_move_max_speed(me.position, move_dest)

            order_set.turn = snapshot.turn
            order_set.debug_message = "supporting"
            order_set.orders.append(move_order)
            return order_set

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def as_goalkeeper(self, order_set: lugo4py.OrderSet, snapshot: lugo4py.GameSnapshot, state: lugo4py.PLAYER_STATE) -> lugo4py.OrderSet:
        try:
            (reader, me) = self.make_reader(snapshot)
            position = snapshot.ball.position
            if state != lugo4py.PLAYER_STATE.DISPUTING_THE_BALL:
                position = reader.get_my_goal().get_center()

            my_order = reader.make_order_move_max_speed(me.position, position)

            order_set.turn = snapshot.turn
            order_set.debug_message = "defending the goal"
            order_set.orders.extend([my_order, reader.make_order_catch()])
            return order_set

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def getting_ready(self, snapshot: lugo4py.GameSnapshot):
        print('getting ready')

def get_my_expected_position(reader: lugo4py.GameSnapshotReader, my_mapper: mapper.Mapper, number: int):
    mapper_cols = 10

    player_tactic_positions = {
        'DEFENSIVE': {
            2: {'Col': 1, 'Row': 1},
            3: {'Col': 2, 'Row': 2},
            4: {'Col': 2, 'Row': 3},
            5: {'Col': 1, 'Row': 4},
            6: {'Col': 3, 'Row': 1},
            7: {'Col': 3, 'Row': 2},
            8: {'Col': 3, 'Row': 3},
            9: {'Col': 3, 'Row': 4},
            10: {'Col': 4, 'Row': 3},
            11: {'Col': 4, 'Row': 2},
        },
        'NORMAL': {
            2: {'Col': 2, 'Row': 1},
            3: {'Col': 4, 'Row': 2},
            4: {'Col': 4, 'Row': 3},
            5: {'Col': 2, 'Row': 4},
            6: {'Col': 6, 'Row': 1},
            7: {'Col': 8, 'Row': 2},
            8: {'Col': 8, 'Row': 3},
            9: {'Col': 6, 'Row': 4},
            10: {'Col': 7, 'Row': 4},
            11: {'Col': 7, 'Row': 1},
        },
        'OFFENSIVE': {
            2: {'Col': 3, 'Row': 1},
            3: {'Col': 5, 'Row': 2},
            4: {'Col': 5, 'Row': 3},
            5: {'Col': 3, 'Row': 4},
            6: {'Col': 7, 'Row': 1},
            7: {'Col': 8, 'Row': 2},
            8: {'Col': 8, 'Row': 3},
            9: {'Col': 7, 'Row': 4},
            10: {'Col': 9, 'Row': 4},
            11: {'Col': 9, 'Row': 1},
        }
    }

    ball_region = my_mapper.get_region_from_point(reader.get_ball().position)
    field_third = mapper_cols / 3
    ball_cols = ball_region.get_col()

    team_state = "OFFENSIVE"
    if ball_cols < field_third:
        team_state = "DEFENSIVE"
    elif ball_cols < field_third * 2:
        team_state = "NORMAL"

    expected_region = my_mapper.get_region(player_tactic_positions[team_state][number]['Col'],
                                           player_tactic_positions[team_state][number]['Row'])
    return expected_region.get_center()

PLAYER_POSITIONS = {
    1: {'Col': 0, 'Row': 0},
    2: {'Col': 1, 'Row': 1},
    3: {'Col': 2, 'Row': 2},
    4: {'Col': 2, 'Row': 3},
    5: {'Col': 1, 'Row': 4},
    6: {'Col': 3, 'Row': 1},
    7: {'Col': 3, 'Row': 2},
    8: {'Col': 3, 'Row': 3},
    9: {'Col': 3, 'Row': 4},
    10: {'Col': 4, 'Row': 3},
    11: {'Col': 4, 'Row': 2},
}
