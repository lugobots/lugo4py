# Lugo4Py - A Lugo Bots Client

Lugo4Py is a Python implementation of a client player for [Lugo](https://lugobots.dev/) game. 

It **is not a bot** that plays the game, it is only the client to connect to the game server. 

This package implements many methods that does not affect the player intelligence/behaviour/decisions. It is meant to
reduce the developer concerns on communication, protocols, attributes, etc.

Using this client, you just need to implement the Artificial Intelligence of your player and some other few methods to support
your strategy (see the project [exampe](./example/simple) folder).
 

### Installation

    pip install lugo4py

### Usage

**Lugo4Py** implements a very basic logic to reduce the code boilerplate. This client will wrap most repetitive
code that handles the raw data got by the bot and will identify the player state.

Implement the [Bot interface](./src/lugo4py/stub.py) to handle each player state based on the ball possession.

```python

class Bot(ABC):
    @abstractmethod
    def on_disputing (self, orderSet: lugo4py.OrderSet, snapshot: GameSnapshot) -> OrderSet:
        # on_disputing is called when no one has the ball possession
        pass

    @abstractmethod
    def on_defending (self, orderSet: OrderSet, snapshot: GameSnapshot) -> OrderSet:
        # OnDefending is called when an opponent player has the ball possession
        pass

    @abstractmethod
    def on_holding (self, orderSet: OrderSet, snapshot: GameSnapshot) -> OrderSet:
        # OnHolding is called when this bot has the ball possession
        pass

    @abstractmethod
    def on_supporting (self, orderSet: OrderSet, snapshot: GameSnapshot) -> OrderSet:
        # OnSupporting is called when a teammate player has the ball possession
        pass

    @abstractmethod
    def as_goalkeeper (self, orderSet: OrderSet, snapshot: GameSnapshot, state: PLAYER_STATE) -> OrderSet:
        # AsGoalkeeper is only called when this bot is the goalkeeper (number 1). This method is called on every turn,
        # and the player state is passed at the last parameter.
        pass

    @abstractmethod
    def getting_ready (self, snapshot: GameSnapshot):
        # getting_ready will be called before the game starts and after a goal event. You will only need to implement
        # this method in very rare cases.
        pass
```

## Kick-start

You may copy the code from [the example directory](./examples) to start you bot, but we encourage you to clone 
[The Dummies Py](https://github.com/lugobots/the-dummies-py) project and start from there. The read me file will have all
details you need.

### Deploying you bots

After developing your bot, you may share it with other developers.

Please find the instructions for uploading your bot on [lugobots.dev](https://lugobots.dev).

There is a Dockerfile template in [the example directory](./examples) to guide you how to create a container.

## Helpers

There are a many things that you will repeatedly need to do on your bot code, e.g. getting your bot position,
creating a move/kick/catch order, finding your teammates positions, etc.

This package brings a collection of functions that will help you get that data from the game snapshot:


```python

config = EnvVarLoader()

reader = GameSnapshotReader(snapshot, self.side)
```

### Mapper and Region

This package also provides a quite useful pair: the Mapper and Region classes.

#### The Mapper

`Mapper` slices the field in columns and rows, so your bot does not have to care about precise coordinates or the team
side. The mapper will automatically translate the map position to the bot side.

And you may define how many columns/rows your field will be divided into.

```python

# let's create a map 10x5 
map = Mapper(10, 5, config.get_bot_team_side())

targetRegion = map.get_region(5, 2)
```

#### The Region

The `Mapper` will slice the field into `Region`s. The Region struct helps your bot to move over the field without caring
about coordinates or team side.

```python

regionInFrontOfMe = targetRegion.front()

moveOrder, err_ := reader.makeOrderMoveMaxSpeed(position, regionInFrontOfMe.center)

```


## The trainable bot

The trainable bot is an interface defined [here](../../src/lugo4py/rl/interfaces.py)


```
docker run -p 8080:8080 -p 5000:5000 lugobots/server:latest play --dev-mode --timer-mode=remote

python3 -m example.rl.main
```
