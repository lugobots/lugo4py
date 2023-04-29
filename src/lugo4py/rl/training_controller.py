import asyncio
from .remote_control import RemoteControl
from .interfaces import TrainingController, BotTrainer, TrainingFunction
from ..protos.server_pb2 import GameSnapshot, OrderSet
import threading
from concurrent.futures import ThreadPoolExecutor
import time




class TrainingCrl(TrainingController):

    def __init__(self, executor: ThreadPoolExecutor, remoteControl: RemoteControl, bot: BotTrainer, onReadyCallback: TrainingFunction):
        self._gotNextState = lambda snapshot: print("got first snapshot")
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
        self.trainingExecutor = executor
        self.resumeListeningPhase = lambda action: print(
            'resumeListeningPhase not defined yet - should wait the initialise it on the first "update" call')

    def setEnvironment(self, data):
        self._debug('Reset state')
        try:
            self.lastSnapshot = self.bot.createNewInitialState(data)
        except Exception as e:
            print('bot trainer failed to create initial state: ', e)
            raise e

    def getState(self):
        try:
            self.cycleSeq = self.cycleSeq + 1
            self._debug('get state')
            return self.bot.getState(self.lastSnapshot)
        except Exception as e:
            print('bot trainer failed to return inputs from a particular state', e)
            raise e

    def update(self, action: any):
        self._debug('UPDATE')
        if not self.onListeningMode:
            raise ValueError('faulty synchrony - got a new action when was still processing the last one')

        try:
            previousState = self.lastSnapshot
            self.OrderSet.turn = self.lastSnapshot.turn
            updatedOrderSet = self.bot.play(self.OrderSet, self.lastSnapshot, action)

            self._debug('got order set, passing down')

            self.resumeListeningPhase(updatedOrderSet)
            #time.sleep(2.4)  # before calling next turn, let's wait just a bit to ensure the server got our order
            self.lastSnapshot = self.wait_until_next_listening_state()

            self._debug('got new snapshot after order has been sent')

            if self.stopRequested:
                return True, 0

            # TODO: if I want to skip the net N turns? I should be able too
            self._debug(f"update finished (turn {self.lastSnapshot.turn} waiting for next action)")
        except Exception as e:
            print('failed send new action to the server: ', e)
            raise e

        try:
            done, reward = self.bot.evaluate(previousState, self.lastSnapshot)
            return done, reward
        except Exception as e:
            print('bot trainer failed to evaluate game state', e)
            raise e

    def gameTurnHandler(self, order_set, snapshot):
        self._debug('new turn')
        if self.onListeningMode:
            raise RuntimeError(
                "faulty synchrony - got new turn while waiting for order (check the lugo 'timer-mode')")

        self._gotNextState(snapshot)

        # loop = asyncio.get_running_loop()
        # Create a new Future object.
        # fut = loop.create_future()
        self.OrderSet = order_set

        waiter = threading.Event()
        new_order_set = None

        def resume(updated_order_set):
            nonlocal new_order_set
            new_order_set = updated_order_set
            waiter.set()
            self._debug(f'Sending new action')

        self._debug(f'AAAAAAAAAAAAAAAAAAAAAAAA')

        self.resumeListeningPhase = resume
        self._debug(f'BBBBBBBBBBBBBBBBBBBBBBBBB')
        self.onListeningMode = True
        self._debug(f'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC')
        if self.trainingHasStarted is False:
            self._debug(f'ASHBAHSBAHSBAHSBAHSBASHABSHABSHASBHASBHABSHASBAHBSHASBHASB')
            self.trainingExecutor.submit(self.onReady, self)
            self._debug(f'PASSSED READY!!!')
            self.trainingHasStarted = True
            self._debug(
                f'the training has started')

        self._debug(f'Waiting get new update!')
        waiter.wait(timeout=5)
        self._debug(f'ORDER SENT!')
        return new_order_set

    def wait_until_next_listening_state(self) -> GameSnapshot:
        try:
            self.onListeningMode = False
            waiter = threading.Event()

            new_snapshot = None
            def resume(newGameSnapshot):
                nonlocal new_snapshot
                print(f'BUUUUUUUUU {newGameSnapshot.state}')
                new_snapshot = newGameSnapshot
                waiter.set()

            self._gotNextState = resume


            waiterResumeListening = threading.Event()


            print(f'VAI VIA VAI')
            time.sleep(4)
            self.trainingExecutor.submit(self.remoteControl.resumeListening, waiterResumeListening)
            waiterResumeListening.wait()

            print(f'HOLD YOUR BREATH')
            waiter.wait(timeout=90)

            print(f'AHHHHH {new_snapshot}')

            self._debug(f'resumeListening: {new_snapshot.turn}')

            return new_snapshot
        except Exception as e:
            self._debug(f'failed to send the orders to the server {e}')
            raise

    def stop(self):
        self.stopRequested = True
        # self.remoteControl.stop()

    def _debug(self, message: str):
        if self.debugging_log:
            print(f"[TrainingCrl] {message}")
