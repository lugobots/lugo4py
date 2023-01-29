import os, threading
import random
from src.main import LugoClient
from src.protos import physics_pb2


def test(*args: server_pb2.GameSnapshot):
    print(args.turn)
    #     print("cool")


def one():
    x = random.randint(0, 100) + 2000
    y = random.randint(0, 100) + 5000
    if int(os.environ.get("BOT_NUMBER")) == 1:
        x = 0

    print("here we go")
    client = LugoClient.new_client(physics_pb2.Point(x=x, y=y))
    client.play(test)


if __name__ == "__main__":
    one()
