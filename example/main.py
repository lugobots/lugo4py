import os, threading
from src.main import LugoClient
from src.protos import physics_pb2

def test(*args):
   print(args)


def one():
    client = LugoClient.new_client(physics_pb2.Point(x=0, y=0))
    client.play(test)


if __name__ == "__main__":
    one()

