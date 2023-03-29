import asyncio
from remote_control import RemoteControl
# from ..protos.remote_pb2_grpc import RemoteStub
from .interfaces import TrainingController, BotTrainer, TrainingFunction
from ..protos.server_pb2 import GameSnapshot, OrderSet


def delay(ms): return asyncio.sleep(ms)


class TrainingCrl(TrainingController):

    def __init__(self, remoteControl: RemoteControl, bot: BotTrainer, onReadyCallback: TrainingFunction):
        self.remoteControl = remoteControl
        self.trainingHasStarted = False
        self.lastSnapshot = GameSnapshot()

        self.waitingForAction = False

        self.cycleSeq = 0

        self.debugging_log = True
        self.stopRequested = False

        # self.gotNewAction = async print('gotNewAction not defined yet - should wait the initialise it on the first "update" call')

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
            raise RuntimeError(
                "faulty synchrony - got a new action when was still processing the last one")

        self.previousState = self.lastSnapshot
        self._debug('got action for turn $self.lastSnapshot.getTurn()')
        self.lastSnapshot = await self.gotNewAction(action)
        self._debug('got new snapshot after order has been sent')

        if (self.stopRequested):
            return {'done': True, 'reward': 0}

        # TODO: if I want to skip the net N turns? I should be able too
        self._debug(
            'update finished (turn $self.lastSnapshot.getTurn() waiting for next action')
        try:
            returnDict = await self.bot.evaluate(self.previousState, self.lastSnapshot)
            return returnDict
        except Exception as e:
            print('bot trainer failed to evaluate game state', e)
            raise e

    def _gotNextState(self, newState: GameSnapshot):
        self._debug('No one waiting for the next state')

    # incomplete function remake

    async def gameTurnHandler(self, orderSet, snapshot):
        self._debug('new turn')

        if self.waitingForAction:
            raise RuntimeError(
                "faulty synchrony - got new turn while waiting for order (check the lugo 'timer-mode')")

        self._gotNextState(snapshot)

        async def promiseFunc(resolve, reject):
            maxWait = asyncio.get_event_loop().call_later(5.0, lambda: None)
            if self.stopRequested:
                self._debug(
                    'stop requested - will not define callback for new actions')
                resolve(orderSet)
                maxWait.cancel()
                return

            try:
                self.waitingForAction = True
                self._debug(
                    'gotNewAction defined, waiting for action (has started: %s)' % self.trainingHasStarted)

                if not self.trainingHasStarted:
                    self.onReady(self)
                    self.trainingHasStarted = True
                    self._debug('the training has started')

                await asyncio.sleep(0)

                newAction = await self.gotNewActionPromise
                self._debug('sending new action')
                maxWait.cancel()

                def resolveTurn(newState):
                    self._debug(
                        'Returning result for new action (snapshot of turn %s)' % newState.getTurn())
                    resolve(newState)

                self._gotNextState = resolveTurn

                self._debug('sending order for turn %s based on action' %
                            snapshot.getTurn())
                orderSet.setTurn(self.lastSnapshot.getTurn())
                await self.bot.play(orderSet, snapshot, newAction)

                self._debug('order sent, calling next turn')
                await asyncio.sleep(0.08)

                self._debug('RESUME NOW!')
                await self.remoteControl.resumeListening()

                self._debug('listening resumed')
            except Exception as e:
                reject()
                rejectTurn()
                print('failed to send the orders to the server', e)

        try:
            return await asyncio.wait_for(promiseFunc, timeout=5.0)
        except asyncio.TimeoutError:
            if not self.stopRequested:
                self._debug('max wait for a new action')
            return orderSet
