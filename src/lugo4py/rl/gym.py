from training_controller import TrainingCrl, delay
from .zombie import newZombiePlayer
from .remote_control import RemoteControl
from .interfaces import BotTrainer, TrainingFunction
from ..client import LugoClient
from ..protos.server_pb2 import Team, OrderSet

class Gym(object):

    def __init__(self, remoteControl: RemoteControl, trainer : BotTrainer, trainingFunction : TrainingFunction,  debugging_log = False):
        self.gameServerAddress = ''
        self.remoteControl = remoteControl
        self.trainingCrl = TrainingCrl(remoteControl, trainer, trainingFunction)
        self.trainingCrl.debugging_log = debugging_log
    

    async def start(self, lugoClient: LugoClient):
        # If the game was started in a previous training session, the game server will be stuck on the listening phase.
        # so we check if the game has started, if now, we try to resume the server
        hasStarted = False
        # await lugoClient.play((orderSet, snapshot) :Promise<OrderSet> => {
        #     hasStarted = true;
        #     return this.trainingCrl.gameTurnHandler(orderSet, snapshot)
        # }, async () => {
        #     if(this.gameServerAddress) {
        #         await completeWithZombies(this.gameServerAddress)
        #     }
        #     setTimeout(() => {
        #         if(!hasStarted) {
        #             this.remoteControl.resumeListening()
        #         }
        #     }, 1000);
        # })
    

    def withZombiePlayers(self, gameServerAddress):
        self.gameServerAddress = gameServerAddress
        return self
    


async def completeWithZombies(gameServerAddress):
    for i in range (1,11):
        await newZombiePlayer(Team.Side.HOME, i, gameServerAddress)
        await delay(50)
        await newZombiePlayer(Team.Side.AWAY, i, gameServerAddress)
        await delay(50)
    
