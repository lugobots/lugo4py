import random
import sys
import time
import traceback

sys.path.append("../..")
from src.lugo4py import mapper
from src.lugo4py.rl.src.contracts import TrainingController


# Training settings
train_iterations = 50
steps_per_iteration = 600

def my_training_function(training_ctrl: TrainingController) -> None:
    print("Let's train")

    possible_actions = [
        mapper.DIRECTION.FORWARD,
        mapper.DIRECTION.BACKWARD,
        mapper.DIRECTION.LEFT,
        mapper.DIRECTION.RIGHT,
        mapper.DIRECTION.BACKWARD_LEFT,
        mapper.DIRECTION.BACKWARD_RIGHT,
        mapper.DIRECTION.FORWARD_RIGHT,
        mapper.DIRECTION.FORWARD_LEFT,
    ]

    scores = []
    for i in range(train_iterations):
        try:
            scores.append(0)
            training_ctrl.set_environment({"iteration": i})
            for j in range(steps_per_iteration):

                _ = training_ctrl.get_state()

                # The sensors would feed our training model, which would return the next action
                action = possible_actions[random.randint(
                    0, len(possible_actions) - 1)]

                # Then we pass the action to our update method
                reward, done = training_ctrl.update(action)
                # Now we should reward our model with the reward value
                scores[i] += reward
                if done:
                    # No more steps
                    print(f"End of train_iteration {i}, score:", scores[i])
                    break
                time.sleep(1)
        except Exception as e:
            traceback.print_exc()
            print(f"error during training session:", e.__traceback__)