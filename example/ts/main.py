import signal
import threading
from concurrent.futures import ThreadPoolExecutor

import reverb
from tf_agents.agents.dqn import dqn_agent
from tf_agents.drivers import py_driver
from tf_agents.environments import tf_py_environment
from tf_agents.networks import sequential
from tf_agents.policies import py_tf_eager_policy
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import reverb_replay_buffer
from tf_agents.replay_buffers import reverb_utils
from tf_agents.specs import array_spec
from tf_agents.specs import tensor_spec
from tf_agents.trajectories import time_step as ts
from tf_agents.utils import common
from tf_agents.networks import q_network

from example.ts import test1
from example.ts.my_bot import MyBotTrainer, TRAINING_PLAYER_NUMBER
from src.lugo4py import lugo
from src.lugo4py.client import LugoClient
from src.lugo4py.mapper import Mapper
from src.lugo4py.rl.gym import Gym
from src.lugo4py.rl.remote_control import RemoteControl
from src.lugo4py.rl.training_controller import TrainingController
import numpy as np
import tensorflow as tf
from tf_agents.environments.py_environment import PyEnvironment


# region settings

num_iterations = 20000  # @param {type:"integer"}

initial_collect_steps = 100  # @param {type:"integer"}
collect_steps_per_iteration = 1  # @param {type:"integer"}
replay_buffer_max_length = 100000  # @param {type:"integer"}

batch_size = 64  # @param {type:"integer"}
learning_rate = 1e-3  # @param {type:"number"}
log_interval = 200  # @param {type:"integer"}

num_eval_episodes = 1  # @param {type:"integer"}
eval_interval = 1000  # @param {type:"integer"}

# endregion



class GameEnvironment(PyEnvironment):

    def __init__(self, training_ctrl: TrainingController):
        self.num_actions = 8
        self.num_sensors = 6

        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int32, minimum=0, maximum=self.num_actions - 1, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(self.num_sensors,), dtype=np.float32, minimum=0, maximum=1, name='observation')
        self.training_ctrl = training_ctrl

        self._reset()



    def action_spec(self):
        print(f"action spec - called")
        return self._action_spec

    def __setState(self, value):
        print(f"__setState - calledssssss")
        st = self.training_ctrl.get_state()
        self._state = np.array([value, 0.029, 0.9287, 0.029, 0.9287, 0.029], dtype=np.float32)

    def observation_spec(self):
        print(f"observation_spec - called")
        return self._observation_spec

    def _reset(self):
        print(f"_reset - WAS called")
        st = self.training_ctrl.set_environment(None)
        self.__setState(0)
        self._episode_ended = False
        return ts.restart(self._state)

    def _step(self, action):
        print(f"_step - called ")
        evaluation = self.training_ctrl.update(action)
       # print(f"_step - called {evaluation}")
        if self._episode_ended:
            # The last action ended the episode. Ignore the current action and start
            # a new episode.
            return self.reset()
        #print(f"Got an action {action}")
        # Make sure episodes don't go on forever.
        if evaluation["done"]:
            self._episode_ended = True

        if self._episode_ended:
            return ts.termination(self._state, evaluation["reward"])
        else:
            return ts.transition(self._state, reward=evaluation["reward"], discount=1.0)

grpc_address = "localhost:5000"
grpc_insecure = True

stop = threading.Event()


def my_training_function(training_ctrl: TrainingController, stop_event: threading.Event):

    print("Let's train")

    # region Setup
    lugoEnv = GameEnvironment(training_ctrl)
    # print("Let's train1")
    # validate_py_environment(lugoEnv, episodes=2)
    # print("Let's train2")

    train_env = tf_py_environment.TFPyEnvironment(lugoEnv)

    # test1.train_rl_model(lugoEnv)

    fc_layer_params = (100, 50)
    # action_tensor_spec = tensor_spec.from_spec(env.action_spec())
    num_actions = 8  # action_tensor_spec.maximum - action_tensor_spec.minimum + 1

    # Define a helper function to create Dense layers configured with the right
    # activation and kernel initializer.
    def dense_layer(num_units):
        return tf.keras.layers.Dense(
            num_units,
            activation=tf.keras.activations.relu,
            kernel_initializer=tf.keras.initializers.VarianceScaling(
                scale=2.0, mode='fan_in', distribution='truncated_normal'))

    # QNetwork consists of a sequence of Dense layers followed by a dense layer
    # with `num_actions` units to generate one q_value per available action as
    # its output.
    dense_layers = [dense_layer(num_units) for num_units in fc_layer_params]
    q_values_layer = tf.keras.layers.Dense(
        num_actions,
        activation=None,
        kernel_initializer=tf.keras.initializers.RandomUniform(
            minval=-0.03, maxval=0.03),
        bias_initializer=tf.keras.initializers.Constant(-0.2))
    # q_net = sequential.Sequential(dense_layers + [q_values_layer])

    q_net = q_network.QNetwork(
        train_env.time_step_spec().observation,
        train_env.action_spec(),
        fc_layer_params=(100,))

    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    train_step_counter = tf.Variable(0)

    agent = dqn_agent.DqnAgent(
        train_env.time_step_spec(),
        train_env.action_spec(),
        q_network=q_net,
        optimizer=optimizer,
        td_errors_loss_fn=common.element_wise_squared_loss,
        train_step_counter=train_step_counter)

    agent.initialize()

    eval_policy = agent.policy
    collect_policy = agent.collect_policy

    random_policy = random_tf_policy.RandomTFPolicy(train_env.time_step_spec(),
                                                    train_env.action_spec())

    table_name = 'uniform_table'
    replay_buffer_signature = tensor_spec.from_spec(
        agent.collect_data_spec)
    replay_buffer_signature = tensor_spec.add_outer_dim(
        replay_buffer_signature)

    table = reverb.Table(
        table_name,
        max_size=replay_buffer_max_length,
        sampler=reverb.selectors.Uniform(),
        remover=reverb.selectors.Fifo(),
        rate_limiter=reverb.rate_limiters.MinSize(1),
        signature=replay_buffer_signature)

    reverb_server = reverb.Server([table])

    replay_buffer = reverb_replay_buffer.ReverbReplayBuffer(
        agent.collect_data_spec,
        table_name=table_name,
        sequence_length=2,
        local_server=reverb_server)

    rb_observer = reverb_utils.ReverbAddTrajectoryObserver(
        replay_buffer.py_client,
        table_name,
        sequence_length=2)

    dataset = replay_buffer.as_dataset(
        num_parallel_calls=3,
        sample_batch_size=batch_size,
        num_steps=2).prefetch(3)

    iterator = iter(dataset)

    # (Optional) Optimize by wrapping some of the code in a graph using TF function.
    agent.train = common.function(agent.train)

    # Reset the train step.
    agent.train_step_counter.assign(0)

    # Evaluate the agent's policy once before training.
    avg_return = compute_avg_return(train_env, agent.policy, num_eval_episodes)
    returns = [avg_return]

    # Reset the environment.
    time_step = train_env.reset()

    # Create a driver to collect experience.
    collect_driver = py_driver.PyDriver(
        train_env,
        py_tf_eager_policy.PyTFEagerPolicy(
            agent.collect_policy, use_tf_function=True),
        [rb_observer],
        max_steps=collect_steps_per_iteration)

    # endregion
    print(f"START THE FUN")
    for _ in range(num_iterations):

        print(f"num_iterations #{num_iterations}", time_step)

        # Collect a few steps and save to the replay buffer.
        time_step, _ = collect_driver.run(time_step)

        print(f"RODA MERDA")
        # Sample a batch of data from the buffer and update the agent's network.
        experience, unused_info = next(iterator)

        print(f"olha o train", experience)
        train_loss = agent.train(experience).loss

        step = agent.train_step_counter.numpy()
        print(f"stepstepstepstepstep", step)

        if step % log_interval == 0:
            print('step = {0}: loss = {1}'.format(step, train_loss))

        if step % eval_interval == 0:
            avg_return = compute_avg_return(train_env, agent.policy, num_eval_episodes)
            print('step = {0}: Average Return = {1}'.format(step, avg_return))
            returns.append(avg_return)

    # possible_actions = [
    #     DIRECTION.FORWARD,
    #     DIRECTION.BACKWARD,
    #     DIRECTION.LEFT,
    #     DIRECTION.RIGHT,
    #     DIRECTION.BACKWARD_LEFT,
    #     DIRECTION.BACKWARD_RIGHT,
    #     DIRECTION.FORWARD_RIGHT,
    #     DIRECTION.FORWARD_LEFT,
    # ]
    # scores = []
    # for i in range(train_iterations):
    #     try:
    #         scores.append(0)
    #         training_ctrl.set_environment({"iteration": i})
    #
    #         for j in range(steps_per_iteration):
    #             if stop_event.is_set():
    #                 training_ctrl.stop()
    #                 stop.set()
    #                 print("trainning stopped")
    #                 return
    #
    #             _ = training_ctrl.get_state()
    #
    #             # The sensors would feed our training model, which would return the next action
    #             action = possible_actions[random.randint(
    #                 0, len(possible_actions) - 1)]
    #
    #             # Then we pass the action to our update method
    #             result = training_ctrl.update(action)
    #             # Now we should reward our model with the reward value
    #             scores[i] += result["reward"]
    #             if result["done"]:
    #                 # No more steps
    #                 print(f"End of train_iteration {i}, score:", scores[i])
    #                 break
    #
    #     except Exception as e:
    #         print("error during trainning session:", e)

    training_ctrl.stop()
    # print("Training is over, scores:", scores)
    stop.set()

def compute_avg_return(environment, policy, num_episodes=10):

    total_return = 0.0
    for _ in range(num_episodes):

        time_step = environment.reset()
        episode_return = 0.0

        while not time_step.is_last():
            action_step = policy.action(time_step)
            time_step = environment.step(action_step.action)
            episode_return += time_step.reward
        total_return += episode_return

    avg_return = total_return / num_episodes
    print("zzzzzzzz zzzzz zzzz ", avg_return)
    return avg_return.numpy()[0]

if __name__ == "__main__":
    team_side = lugo.TeamSide.HOME
    print('main: Training bot team side = ', team_side)
    # The map will help us see the field in quadrants (called regions) instead of working with coordinates
    # The Mapper will translate the coordinates based on the side the bot is playing on
    mapper = Mapper(20, 10, lugo.TeamSide.HOME)

    # Our bot strategy defines our bot initial position based on its number
    initial_region = mapper.get_region(5, 4)

    # Now we can create the bot. We will use a shortcut to create the client from the config, but we could use the
    # client constructor as well
    lugo_client = LugoClient(
        grpc_address,
        grpc_insecure,
        "",
        team_side,
        TRAINING_PLAYER_NUMBER,
        initial_region.get_center()
    )
    # The RemoteControl is a gRPC client that will connect to the Game Server and change the element positions
    rc = RemoteControl()
    rc.connect(grpc_address)  # Pass address here

    bot = MyBotTrainer(rc)

    gym_executor = ThreadPoolExecutor()
    # Now we can create the Gym, which will control all async work and allow us to focus on the learning part
    gym = Gym(gym_executor, rc, bot, my_training_function, {"debugging_log": False})

    players_executor = ThreadPoolExecutor(22)
    gym.with_zombie_players(grpc_address).start(lugo_client, players_executor)


    def signal_handler(_, __):
        print("Stop requested\n")
        lugo_client.stop()
        gym.stop()
        players_executor.shutdown(wait=True)
        gym_executor.shutdown(wait=True)


    signal.signal(signal.SIGINT, signal_handler)

    stop.wait()
