from .protos import server_pb2_grpc
from .protos import server_pb2

from . import specs

import os

class EnvVarLoader:

    def __init__(self):
        self._grpcUrl = ""
        self._grpcInsecure = True
        self._botTeamSide = None
        self._botNumber = None
        self._botToken = ""

        if "BOT_TEAM" not in os.environ:
            raise SystemError("missing BOT_TEAM env value")
        

        if "BOT_NUMBER" not in os.environ:
            raise SystemError("missing BOT_NUMBER env value")

        # the Lugo address
        self._grpcUrl = os.environ["BOT_GRPC_URL"] if "BOT_GRPC_URL" in os.environ else 'localhost:5000'
        if "BOT_GRPC_INSECURE" in os.environ:
            self._grpcUrl = bool(os.environ["BOT_GRPC_INSECURE"])
        
        # defining bot side
        self._botTeamSide = server_pb2.Team.Side.HOME if os.environ["BOT_TEAM"].upper() == 'HOME' else server_pb2.Team.Side.AWAY
        self._botNumber = int(os.environ["BOT_NUMBER"])
        if (self._botNumber < 1 or self._botNumber > specs.MAX_PLAYERS):
            raise  SystemError('invalid bot number {self._botNumber}, must be between 1 and {specs.MAX_PLAYERS}')

        # // the token is mandatory in official matches, but you may ignore in local games
        self._botToken = os.environ["BOT_TOKEN"] if "BOT_TOKEN" in os.environ else ''
    

    def getGrpcUrl(self):
        return self._grpcUrl

    def getGrpcInsecure(self):
        return self._grpcInsecure
    
    def getBotTeamSide(self):
        return self._botTeamSide

    def getBotNumber(self):
        return self._botNumber

    def getBotToken(self):
        return self._botToken

