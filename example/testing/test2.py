import asyncio
import logging
from src.lugo4py.protos import server_pb2
from src.lugo4py.protos import server_pb2_grpc as server_grpc
from src.lugo4py.protos import physics_pb2
import os
import grpc
from concurrent.futures import ThreadPoolExecutor
from src.lugo4py.stub import Bot


class KeepStoppedBot(Bot):
    async def gettingReady(self, orders, snapshot):
        return orders

    async def asGoalkeeper(self, orders, snapshot, playerState):
        return orders

    async def onDisputing(self, orders, snapshot):
        return orders

    async def onDefending(self, orders, snapshot):
        return orders

    async def onSupporting(self, orders, snapshot):
        return orders

    async def onHolding(self, orders, snapshot):
        return orders


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

grpc_url = 'localhost:5000'
grpc_insecure = True

logger.info(
    f"grpc_url: {grpc_url}, grpc_insecure: {grpc_insecure}")

executor = ThreadPoolExecutor()


# make a gprc call with a timeout
async def call_with_timeout(client, join_request, timeout):
    try:
        # Create a future to run the grpc call in a thread pool executor
        future = executor.submit(
            next, client.JoinATeam(join_request).__iter__())
        # use asyncio.wait to wait for the future to complete or the timeout to occur
        done, pending = await asyncio.wait(
            {asyncio.wrap_future(future)}, timeout=timeout, return_when=asyncio.FIRST_COMPLETED
        )
        if not done:
            # if the timeout occurred, raise an error
            raise asyncio.TimeoutError()
        # Returns the result of the future
        return done.pop().result()
    except asyncio.TimeoutError:
        logger.error("RPC call timed out")
    except Exception as e:
        logger.error(f"RPC call error: {e}")
    # If there was an error, return None
    return None


async def connect_and_play_bot(client, initial_position, team_side, token, bot_number, on_join_callback, turn_processor_callback):
    join_request = server_pb2.JoinRequest(
        token=token,
        team_side=team_side,
        number=bot_number,
        init_position=physics_pb2.Point(
            x=initial_position.x, y=initial_position.y),
    )

    await on_join_callback()

    while True:
        snapshot = await call_with_timeout(client, join_request, timeout=10)
        await asyncio.sleep(0.1)
        if snapshot is None:
            logger.error("Error connecting to the server, retrying...")
            continue  # Retry the connection

        try:
            if snapshot.state == server_pb2.GameSnapshot.State.OVER:
                break
            elif snapshot.state == server_pb2.GameSnapshot.State.LISTENING:
                orders = server_pb2.OrderSet()
                orders.turn = snapshot.turn
                try:
                    orders = await turn_processor_callback(orders, snapshot)
                except Exception as e:
                    logger.error(f"bot error: {e}")

                if orders:
                    client.SendOrders(orders)
                else:
                    logger.error(
                        f"[turn #{snapshot.turn}] bot did not return orders")
        except Exception as e:
            logger.error(f"internal error processing turn: {e}")


async def create_and_play_client(client, initial_position, team_side, token, bot_number, bot):
    logger.info(f"Creating client {bot_number}")

    async def on_join():
        logger.info(f"Bot {bot_number} joined the team.")

    async def turn_processor(orders, snapshot):
        return await bot.process_turn(orders, snapshot)

    logger.info(f"Bot {bot_number} is starting to play")
    await connect_and_play_bot(client, initial_position, team_side, token, bot_number, on_join, turn_processor)
    logger.info(f"Bot {bot_number} started playing")


async def create_players(client, num_players, token):
    team_sides = [server_pb2.Team.Side.HOME, server_pb2.Team.Side.AWAY]
    y_positions = [500 + (i * 1000) for i in range(num_players - 1)]

    tasks = []

    for team_side in team_sides:
        goalkeeper_y = 5000
        goalkeeper_x = 0 if team_side == server_pb2.Team.Side.HOME else 20000
        player_x = 5000 if team_side == server_pb2.Team.Side.HOME else 15000
        initial_positions = [physics_pb2.Point(x=goalkeeper_x, y=goalkeeper_y)] + \
                            [physics_pb2.Point(x=player_x, y=y)
                             for y in y_positions]

        keep_stopped_bot = KeepStoppedBot()

        for i, position in enumerate(initial_positions, start=1):
            task = asyncio.create_task(create_and_play_client(
                client, position, team_side, token, i, keep_stopped_bot))
            tasks.append(task)

    logger.info("Gathering tasks")
    clients = await asyncio.gather(*tasks)
    logger.info("Tasks gathered")

    return clients


async def main():
    num_players = 11
    logger.info(f"Creating {num_players} players")

    if grpc_insecure:
        channel = grpc.insecure_channel(grpc_url)
    else:
        channel = grpc.secure_channel(grpc_url, grpc.ssl_channel_credentials())

    client = server_grpc.GameStub(channel)

    clients = await create_players(client, num_players, "")
    await asyncio.sleep(10)
    # Waits for all clients to complete their tasks
    await asyncio.gather(*(client.wait_for_done() for clients in clients))
    logger.info("All clients completed their tasks")


asyncio.run(main())
