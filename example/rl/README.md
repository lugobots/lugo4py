## Reinforcement learning env - Basic example


In this example you will find a basic example of how the trainable bot can be used in a training session.

## Trainable bot

This example [trainable bot](./my_bot.py) implementation only return dummy data to make the "training" session visible.


## Training function

This example of [training function](./main.py) just pick random actions and print outputs. 



## How to start the training

You must run the Game Server ([https://hub.docker.com/r/lugobots/server](https://hub.docker.com/r/lugobots/server)) on **Dev Mode**
and set the timer mode to **remote**. Those options will allow your RL environment to control the server.

1. **Start the server using this command:**
    ```shell 
    docker run -p 8080:8080 -p 5000:5000 lugobots/server:v1.0.0-beta.6-rc.1 play --dev-mode --timer-mode=remote
    ```
   You may watch your bot training session at http://localhost:8080/
2. **Run the training**
    ```shell
        python3 main.py
    ```