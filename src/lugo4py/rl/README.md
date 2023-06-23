# Lugo Reinforcement Learning 

See example at the [RL example](../../example/rl)

## How to use the RL lib?

The RL lib has a class called `Gym` that will require 3 params:

### The Remote control

The RC allow you to control the game server flow by pausing, changing the elements' position, etc. (see
the [Remote Service in the Game protocol definition](https://github.com/lugobots/protos/blob/master/doc/docs.md#remote))

The remote control is already implemented in **Lugo4Node** package.:
```typescript
    const rc = new rl.RemoteControl();
    await rc.connect(grpcAddress)
```

### The Bot Trainer

You should create a class that implements the interface `rl.BotTrainer`.

The BotTrainer is used by the Gym class to play the game as a bot and to control the game state when needed.
It is NOT your learning agent! You should create your agent inside the training function.

Please read the [interface documentation](interfaces.ts#L38) to learn what each method is expected to do.

**Important**: You can train only one player at once. So, your bot trainer must play as a single play (defined by the
player number). See in the next steps how add more players to the game.

### The training function

You should to implement a training function:

```typescript
    type TrainingFunction = (trainingCtr: TrainingController) => Promise<void>;
```
The training function will receive a `rl.TrainingController` interface that will allow you to control the training flow.

You should train your model inside the training function.

## How to start the training

You must run the Game Server ([https://hub.docker.com/r/lugobots/server](https://hub.docker.com/r/lugobots/server)) on **Dev Mode**
and set the timer mode to **remote**. Those options will allow your RL environment to control the server.

1. **Start the server using this command:**
    ```shell 
    docker run -p 8080:8080 -p 5000:5000 lugobots/server:v1.0.0-beta.6-rc.1 play --dev-mode --timer-mode=remote
    ```
    You may watch your bot training session at http://localhost:8080/
2. **Compile the Typescript files**: This project is developer in Typescript. You must compile the files everytime you
    change the `.ts` files. The easier way to do that is keeping `npm run watch` running, what will constantly update
    the compiled files.
3. **Run the training**
    ```shell
    npm run start
    ```

### Improving performance

You may start the server without the frontend part (headless), it will save some resources and speed up the training.

```bash 
docker run -p 8080:8080 -p 5000:5000 lugobots/server:v1.0.0-beta.6-rc.1 play --dev-mode --timer-mode=remote --headless
```

## 5. Adding more players to the game

The Game Server requires exactly 11 players in each team to start the game. Since your bot trainer can only play as one player in
the game, you will need complete your game with more players.

You may start another bot team (see [The Dummies bot](https://github.com/lugobots/the-dummies-go) ) or you may use _Zombie PLayers_.

The  _Zombie PLayers_ are bots the only connects to the game, but they do nothing else during the entire game. The Gym
class comes with a method that will start these zombies right after the trainable bot be ready to play.

```javascript
    // instead of starting the training session with 
await gym.start(lugoClient)

// start with
await gym.withZombiePlayers(grpcAddress).start(lugoClient)
```

**Note** that the Gym will try to connect 11 players in each side, so at least one of the connections will fail because
one position is already occupied by your trainable bot. Just ignore it.
