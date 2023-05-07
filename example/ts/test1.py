import tensorflow as tf
from tf_agents.agents.dqn.dqn_agent import DqnAgent
from tf_agents.drivers import dynamic_episode_driver
from tf_agents.networks.q_network import QNetwork
from tf_agents.policies.policy_saver import PolicySaver
from tf_agents.replay_buffers.tf_uniform_replay_buffer import TFUniformReplayBuffer
from tf_agents.trajectories import trajectory
from tf_agents.utils import common
from tf_agents.drivers.dynamic_step_driver import DynamicStepDriver


def train_rl_model(environment, num_iterations=200, batch_size=12, learning_rate=1e-3, replay_buffer_capacity=12000000,
                   collect_steps_per_iteration=1, num_eval_episodes=10, eval_interval=1000):
    # Set up the agent's network
    q_net = QNetwork(
        environment.observation_spec(),
        environment.action_spec(),
        fc_layer_params=(100,)
    )
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    train_step_counter = tf.Variable(0)

    # Set up the agent
    agent = DqnAgent(
        environment.time_step_spec(),
        environment.action_spec(),
        q_network=q_net,
        optimizer=optimizer,
        td_errors_loss_fn=common.element_wise_squared_loss,
        train_step_counter=train_step_counter
    )
    agent.initialize()

    # Set up the replay buffer
    replay_buffer = TFUniformReplayBuffer(
        data_spec=agent.collect_data_spec,
        batch_size=batch_size,
        # max_length=replay_buffer_capacity
    )

    # Set up the policy saver
    policy_saver = PolicySaver(agent.policy)

    # Set up the data collector
    def collect_step(environment, policy):
        print(f"COLLECT!")
        time_step = environment.current_time_step()
        action_step = policy.action(time_step)
        next_time_step = environment.step(action_step.action)
        traj = trajectory.from_transition(time_step, action_step, next_time_step)

        # Add the trajectory to the replay buffer
        replay_buffer.add_batch(traj)

    collect_policy = agent.collect_policy
    collect_driver = DynamicStepDriver(
        environment,
        collect_policy,
        observers=[collect_step],
        num_steps=collect_steps_per_iteration
    )

    # Set up the evaluation driver
    eval_policy = agent.policy
    num_eval_episodes = num_eval_episodes
    eval_interval = eval_interval
    eval_driver = dynamic_episode_driver.DynamicEpisodeDriver(
        environment,
        eval_policy,
        observers=[],
        num_episodes=num_eval_episodes
    )

    # Train the agent
    for i in range(num_iterations):
        # Collect some data
        print(f"FUUUUU!")
        collect_driver.run()
        print(f"DDDEU!")
        # Sample a batch of data from the replay buffer
        experience = replay_buffer.gather_all()
        train_loss = agent.train(experience)

        print(f"Iteration {i}, train_loss: {train_loss}")
        # Evaluate the agent periodically
        if i % eval_interval == 0:
            avg_return = compute_avg_return(environment, eval_policy, num_eval_episodes)
            print(f"Iteration {i}, average return: {avg_return}")

    # Save the final policy
    policy_saver.save("final_policy")


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
