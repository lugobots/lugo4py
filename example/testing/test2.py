import asyncio
import logging
from src.lugo4py.protos import server_pb2
from src.lugo4py.protos import server_pb2_grpc as server_grpc
from src.lugo4py.protos import physics_pb2
import os
import grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

grpc_url = 'localhost:5000'
grpc_insecure = True
team_side = server_pb2.Team.Side.HOME

logger.info(
    f"grpc_url: {grpc_url}, grpc_insecure: {grpc_insecure}, team_side: {team_side}")


async def call_with_timeout(rpc_call, timeout):
    try:
        return await asyncio.wait_for(rpc_call, timeout=timeout)
    except TimeoutError:
        # handle the timeout here
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
        snapshot = await call_with_timeout(client.JoinATeam(join_request).__iter__().__next__(), timeout=5)

        if snapshot is None:
            logger.error("Connection timed out")
            break

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


async def create_and_play_client(client, initial_position, team_side, token, bot_number):
    logger.info(f"Creating client {bot_number}")

    async def on_join():
        logger.info(f"Bot {bot_number} joined the team.")

    async def turn_processor(orders, snapshot):
        pass

    logger.info(f"Bot {bot_number} is starting to play")
    await connect_and_play_bot(client, initial_position, team_side, token, bot_number, on_join, turn_processor)
    logger.info(f"Bot {bot_number} started playing")


async def create_players(client, team_side, num_players, token):
    y_positions = [500 + (i * 1000) for i in range(num_players)]
    initial_positions = [physics_pb2.Point(x=3000, y=y) for y in y_positions]

    tasks = []

    for i, position in enumerate(initial_positions, start=1):
        task = asyncio.create_task(create_and_play_client(
            client, position, team_side, token, i))
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

    clients = await create_players(client, team_side, num_players, "")

    # Waits for all clients to complete their tasks
    await asyncio.gather(*(client.wait_for_done() for clients in clients))
    logger.info("All clients completed their tasks")

asyncio.run(main())
