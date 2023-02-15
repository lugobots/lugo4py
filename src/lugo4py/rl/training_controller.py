import asyncio
from remote_control import RemoteControl
from .interfaces import TrainingController, BotTrainer, TrainingFunction
from ..protos.server_pb2 import GameSnapshot, OrderSet

delay = lambda ms : asyncio.sleep(ms)

class TrainingCrl(TrainingController):

    def __init__(self, remoteControl: RemoteControl, bot: BotTrainer, onReadyCallback: TrainingFunction):
        self.remoteControl = remoteControl
        self.trainingHasStarted = False
        self.lastSnapshot = GameSnapshot()

        self.waitingForAction = False

        self.cycleSeq = 0
        
        self.debugging_log = True
        self.stopRequested = False

        #self.gotNewAction = async print('gotNewAction not defined yet - should wait the initialise it on the first "update" call')

        self.onReady = onReadyCallback
        self.bot = bot
        self.remoteControl = remoteControl

    async def setRandomState(self):
        self._debug('Reset state')
        try:
            self.lastSnapshot = await self.bot.createNewInitialState()

        except Exception as e: 
            print('bot trainer failed to create initial state', e)
            raise e

    def getInputs(self):
        try: 
            self.cycleSeq = self.cycleSeq + 1 
            self._debug('get state')
            return self.bot.getInputs(self.lastSnapshot)
        except Exception as e: 
            print('bot trainer failed to return inputs from a particular state', e)
            raise e
        
    

    #  return Promise< reward: number done: boolean > 
    async def update(self, action: any):
        self._debug('UPDATE')
        if not self.waitingForAction:
            raise RuntimeError("faulty synchrony - got a new action when was still processing the last one")
        

        self.previousState = self.lastSnapshot
        self._debug('got action for turn $self.lastSnapshot.getTurn()')
        self.lastSnapshot = await self.gotNewAction(action)
        self._debug('got new snapshot after order has been sent')

        if (self.stopRequested):
            return {'done': True, 'reward': 0}
        

        # TODO: if I want to skip the net N turns? I should be able too
        self._debug('update finished (turn $self.lastSnapshot.getTurn() waiting for next action')
        try: 
            returnDict = await self.bot.evaluate(self.previousState, self.lastSnapshot)
            return returnDict
        except Exception as e: 
            print('bot trainer failed to evaluate game state', e)
            raise e

    def _gotNextState (self, newState: GameSnapshot): 
        self._debug('No one waiting for the next state')
    

    async def gameTurnHandler(self, orderSet, snapshot):
        self._debug('new turn')
        if (self.waitingForAction): 
            raise RuntimeError("faulty synchrony - got new turn while waiting for order (check the lugo 'timer-mode')")
        
        self._gotNextState(snapshot)

        return await new Promise(async (resolve, reject) => 
            const maxWait = setTimeout(() => 
                if (self.stopRequested) 
                    return resolve(orderSet)
                
                console.error('max wait for a new action')
                reject()
            , 5000)
            if (self.stopRequested) 
                self._debug('stop requested - will not defined call back for new actions')
                resolve(orderSet)
                clearTimeout(maxWait)
                return null
            

            self.gotNewAction = async (newAction) => 
                self._debug('sending new action')
                clearTimeout(maxWait)
                return new Promise<GameSnapshot>((resolveTurn, rejectTurn) => 
                    try 
                        self.waitingForAction = false
                        self._gotNextState = (newState) => 
                            self._debug('Returning result for new action (snapshot of turn $newState.getTurn())')
                            resolveTurn(newState)
                        
                        self._debug('sending order for turn $snapshot.getTurn() based on action')
                        orderSet.setTurn(self.lastSnapshot.getTurn())
                        self.bot.play(orderSet, snapshot, newAction).then((orderSet) => 
                            resolve(orderSet)// sending the orders wh
                            self._debug('order sent, calling next turn')
                            return delay(80)// why? ensure the server got the order?
                        ).then(() => 
                            self._debug('RESUME NOW!')
                            return self.remoteControl.resumeListening()
                        ).then(() => 
                            self._debug('listening resumed')
                        )
                     catch (e) 
                        reject()
                        rejectTurn()
                        console.error('failed to send the orders to the server', e)
                    
                )
            
            self.waitingForAction = true
            self._debug('gotNewAction defined, waiting for action (has started: $self.trainingHasStarted)')
            if (!self.trainingHasStarted) 
                self.onReady(this)
                self.trainingHasStarted = true
                self._debug('the training has started')
            

        )
    

    async stop() 
        self.stopRequested = true
    

    _debug(msg) 
        if (self.debugging_log) 
            console.log('[$self.cycleSeq] $msg')
            
async def asyncToSync(asyncOriginalFunc):
    const result = await asyncOriginalFunc()
    return  result