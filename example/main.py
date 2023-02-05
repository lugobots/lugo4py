# const {EnvVarLoader, NewClientFromConfig, GameSnapshotReader, Mapper} = require('@lugobots/lugo4node')
# const MyBot = require('./my_bot')

# const PLAYER_POSITIONS = {
#     1: {Col: 0, Row: 0},
#     2: {Col: 1, Row: 1},
#     3: {Col: 2, Row: 2},
#     4: {Col: 2, Row: 3},
#     5: {Col: 1, Row: 4},
#     6: {Col: 3, Row: 1},
#     7: {Col: 3, Row: 2},
#     8: {Col: 3, Row: 3},
#     9: {Col: 3, Row: 4},
#     10: {Col: 4, Row: 3},
#     11: {Col: 4, Row: 2},
# }

# // we must load the env vars following the standard defined by the game specs because all bots will receive the
# // arguments in the same format (env vars)
# const config = new EnvVarLoader()

# // the map will help us to see the field in quadrants (called regions) instead of working with coordinates
# const map = new Mapper(10, 6, config.getBotTeamSide())

# // our bot strategy defines our bot initial position based on its number
# const initialRegion = map.getRegion(PLAYER_POSITIONS[config.getBotNumber()].Col, PLAYER_POSITIONS[config.getBotNumber()].Row)

# // now we can create the bot. We will use a shortcut to create the client from the config, but we could use the
# // client constructor as well
# const lugoClient = new NewClientFromConfig(config, initialRegion.getCenter())

# const myBot = new MyBot(
#   config.getBotTeamSide(),
#   config.getBotNumber(),
#   initialRegion.getCenter(),
#   map,
# )

# lugoClient.playAsBot(myBot).then(() => {
#     console.log(`all done`)
# }).catch(e => {
#     console.error(e)
# })


import sys
sys.path.append("src")
import os
if "BOT_GRPC_URL" not in os.environ:
    os.environ["BOT_GRPC_URL"] = "localhost:5000"
    os.environ["BOT_NUMBER"] = "1"
    os.environ["BOT_TEAM"] = "home"

import os, threading
from lugo4py.client import LugoClient
from lugo4py.protos import physics_pb2

def test(*args):
   print(args)


def one():
    client = LugoClient.new_client(physics_pb2.Point(x=2200, y=5000))
    client.play(test)


if __name__ == "__main__":
    one()




# const {GameSnapshotReader, Bot, PLAYER_STATE, Mapper, BroadcastClient,  } = require('@lugobots/lugo4node')


# class MyBot {
#   /**
#    * @type {Lugo.Team.Side}
#    */
#   #side;

#   /**
#    * @type {number}
#    */
#   #number;

#   /**
#    * @type {physics.Point}
#    */
#   #initPosition;

#   /**
#    * @type {Mapper}
#    */
#   #mapper;

#   /**
#    *
#    * @param {Lugo.Team.Side} side
#    * @param {number} number
#    * @param {physics.Point} initPosition
#    * @param {Mapper} mapper
#    */
#   constructor(side, number, initPosition, mapper) {
#     this.#side = side
#     this.#number = number
#     this.#mapper = mapper
#     this.#initPosition = initPosition

#   }

#   /**
#    *
#    * @param {GameSnapshot} snapshot
#    * @private
#    * @return {GameSnapshotReader}
#    */
#   _makeReader(snapshot) {
#     const reader = new GameSnapshotReader(snapshot, this.#side)
#     const me = reader.getPlayer(this.#side, this.#number)
#     if (!me) {
#       throw new Error("did not find myself in the game")
#     }
#     return {reader, me}
#   }

#   /**
#    *
#    * @param {} orderSet
#    * @param snapshot
#    * @return {*}
#    */
#   onDisputing(orderSet, snapshot) {
#     try {
#       const {reader, me} = this._makeReader(snapshot)

#       const ballPosition = reader.getBall().getPosition()
#       const ballRegion = this.#mapper.getRegionFromPoint(ballPosition)
#       const myRegion = this.#mapper.getRegionFromPoint(this.#initPosition)

#       let moveDest = this.#initPosition
#       if (Math.abs(myRegion.getRow() - ballRegion.getRow()) <= 2 &&
#         Math.abs(myRegion.getCol() - ballRegion.getCol()) <= 2) {
#         moveDest = ballPosition
#       }
#       const moveOrder = reader.makeOrderMoveMaxSpeed(me.getPosition(), moveDest)
#       // const catchOrder = reader.
#       orderSet.setTurn(snapshot.getTurn())
#       orderSet.setDebugMessage("mi mi mi")
#       orderSet.setOrdersList([moveOrder])
#       return orderSet
#     } catch (e) {
#       console.log(`did not play this turn`, e)
#     }
#   }

#   onDefending(orderSet, snapshot) {
#     try {
#       const {reader, me} = this._makeReader(snapshot)
#       const ballPosition = snapshot.getBall().getPosition()
#       const ballRegion = this.#mapper.getRegionFromPoint(ballPosition)
#       const myRegion = this.#mapper.getRegionFromPoint(this.#initPosition)

#       let moveDest = this.#initPosition
#       if (Math.abs(myRegion.getRow() - ballRegion.getRow()) <= 2 &&
#         Math.abs(myRegion.getCol() - ballRegion.getCol()) <= 2) {
#         moveDest = ballPosition
#       }
#       const moveOrder = reader.makeOrderMoveMaxSpeed(me.getPosition(), moveDest)
#       const catchOrder =  reader.makeOrderCatch()

#       orderSet.setTurn(snapshot.getTurn())
#       orderSet.setDebugMessage("trying to catch the ball")
#       orderSet.setOrdersList([moveOrder, catchOrder])
#       return orderSet
#     } catch (e) {
#       console.log(`did not play this turn`, e)
#     }
#   }

#   onHolding(orderSet, snapshot) {
#     try {
#       const {reader, me} = this._makeReader(snapshot)

#       const myGoalCenter = this.#mapper.getRegionFromPoint(reader.getOpponentGoal().center)
#       const currentRegion = this.#mapper.getRegionFromPoint(me.getPosition())

#       let myOrder;
#       if (Math.abs(currentRegion.getRow() - myGoalCenter.getRow()) <= 1 &&
#         Math.abs(currentRegion.getCol() - myGoalCenter.getCol()) <= 1) {
#         myOrder = reader.makeOrderKickMaxSpeed(snapshot.getBall(), reader.getOpponentGoal().center)
#       } else {
#         myOrder = reader.makeOrderMoveMaxSpeed(me.getPosition(), reader.getOpponentGoal().center)
#       }

#       orderSet.setTurn(snapshot.getTurn())
#       orderSet.setDebugMessage("attack!")
#       orderSet.setOrdersList([myOrder])
#       return orderSet
#     } catch (e) {
#       console.log(`did not play this turn`, e)
#     }
#   }

#   onSupporting(orderSet, snapshot) {
#     try {
#       const {reader, me} = this._makeReader(snapshot)
#       const ballHolderPosition = snapshot.getBall().getPosition()
#       const myOrder = reader.makeOrderMoveMaxSpeed(me.getPosition(), ballHolderPosition)

#       orderSet.setTurn(snapshot.getTurn())
#       orderSet.setDebugMessage("supporting")
#       orderSet.setOrdersList([myOrder])
#       return orderSet
#     } catch (e) {
#       console.log(`did not play this turn`, e)
#     }
#   }

#   /**
#    *
#    * @param orderSet
#    * @param snapshot
#    * @param state
#    * @return {OrderSet}
#    */
#   asGoalkeeper(orderSet, snapshot, state) {
#     try {
#       const {reader, me} = this._makeReader(snapshot)
#       let position = snapshot.getBall().getPosition()
#       if (state !== PLAYER_STATE.DISPUTING_THE_BALL) {
#         position = reader.getMyGoal().center
#       }

#       const myOrder = reader.makeOrderMoveMaxSpeed(me.getPosition(), position)

#       const orderSet = new Lugo.OrderSet()
#       orderSet.setTurn(snapshot.getTurn())
#       orderSet.setDebugMessage("supporting")
#       orderSet.setOrdersList([myOrder, reader.makeOrderCatch()])
#       return orderSet
#     } catch (e) {
#       console.log(`did not play this turn`, e)
#     }
#   }
# }
