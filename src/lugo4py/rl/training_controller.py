import asyncio
from .remote_control import RemoteControl
from .interfaces import TrainingController, BotTrainer, TrainingFunction
from ..protos.server_pb2 import GameSnapshot, OrderSet


def delay(ms): return asyncio.sleep(ms)


class TrainingCrl(TrainingController):

    def __init__(self, remoteControl: RemoteControl, bot: BotTrainer, onReadyCallback: TrainingFunction):
        self._gotNextState = None
        self.previousState = None
        self.remoteControl = remoteControl  # type: RemoteControl
        self.onReady = onReadyCallback
        self.trainingHasStarted = False
        self.lastSnapshot = None  # type: GameSnapshot
        self.onListeningMode = False
        self.OrderSet = None
        self.cycleSeq = 0
        self.bot = bot  # type: BotTrainer
        self.debugging_log = True
        self.stopRequested = False
        self.resumeListeningPhase = lambda action: print(
            'resumeListeningPhase not defined yet - should wait the initialise it on the first "update" call')


    async def setEnvironment(self, data):
        self._debug('Reset state')
        try:
            self.lastSnapshot = await self.bot.createNewInitialState(data)
        except Exception as e:
            print('bot trainer failed to create initial state', e)
            raise e

    def getState(self):
        try:
            self.cycleSeq = self.cycleSeq + 1
            self._debug('get state')
            return self.bot.getState(self.lastSnapshot)
        except Exception as e:
            print('bot trainer failed to return inputs from a particular state', e)
            raise e

    async def update(self, action: any):
        self._debug('UPDATE')
        if not self.onListeningMode:
            raise ValueError('faulty synchrony - got a new action when was still processing the last one')

        previousState = self.lastSnapshot
        self.OrderSet.setTurn(self.lastSnapshot.getTurn())
        updatedOrderSet = await self.bot.play(self.OrderSet, self.lastSnapshot, action)

        self._debug('got order set, passing down')
        self.resumeListeningPhase(updatedOrderSet)
        await delay(20)  # before calling next turn, let's wait just a bit to ensure the server got our order
        self.lastSnapshot = await self.wait_until_next_listening_state()

        self._debug('got new snapshot after order has been sent')

        if self.stopRequested:
            return True, 0

        # TODO: if I want to skip the net N turns? I should be able too
        self._debug(f"update finished (turn {self.lastSnapshot.getTurn()} waiting for next action)")
        try:
            done, reward = await self.bot.evaluate(previousState, self.lastSnapshot)
            return done, reward
        except Exception as e:
            print('bot trainer failed to evaluate game state', e)
            raise e


    async def gameTurnHandler(self, orderSet, snapshot):
        self._debug('new turn')
        if self.onListeningMode:
            raise RuntimeError(
                "faulty synchrony - got new turn while waiting for order (check the lugo 'timer-mode')")

        self._gotNextState(snapshot)

        loop = asyncio.get_running_loop()
        # Create a new Future object.
        fut = loop.create_future()
        self.OrderSet = orderSet

        def resume(updatedOrderSet):
            self._debug(
                f'Sending new action')
            fut.set_result(updatedOrderSet)

        self.resumeListeningPhase = resume
        self.onListeningMode = True

        if self.trainingHasStarted is False:
            self.onReady(self)
            self.trainingHasStarted = True
            self._debug(
                f'the training has started')
        return await fut

    async def wait_until_next_listening_state(self) -> GameSnapshot:
        try:
            self.onListeningMode = False
            loop = asyncio.get_event_loop()
            future_turn = loop.create_future()

            self._gotNextState = lambda newGameSnapshot: future_turn.set_result(newGameSnapshot)

            self._debug(
                f'resumeListening: ${self.lastSnapshot.getTurn()}')
            await self.remoteControl.resumeListening()
            return await future_turn
        except Exception:
            self._debug('failed to send the orders to the server')
            raise

    def stop(self):
        self.stopRequested = True
        # self.remoteControl.stop()

    def _debug(self, message: str):
        if self.debugging_log:
            print(f"[TrainingCrl] {message}")
