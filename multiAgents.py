# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """

        # print "\n\nactions is :", action
        evalScore = 0
        distToGhosts = []
        ghostScared = 0
        ghostThreat = 0
        distanceToClosestFood = 0
        if action == 'Stop':
          return evalScore

        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        foodList = newFood.asList()
        newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # distToGhosts = [abs(ghostPos[0] - newPos[0])

        # finding min ghost distance
        for ghostState in newGhostStates:
          ghostPos = ghostState.getPosition()
          ghostScared == ghostState.scaredTimer
          # print "scared? ", ghostScared
          if (abs(newPos[0] - ghostPos[0]) <= 2 and abs(newPos[1] - ghostPos[1]) <=2):
          # if abs(ghostPos[0] - newPos[0]) <= 2 and abs(ghostPos[1] - newPos[1]) <=2:
            if not ghostScared:
              # print "ghost is threatening!"
              ghostThreat = 1
              distToGhosts.append(manhattanDistance(ghostPos, newPos))
        # finding min food distance
        # print "ghostThreat is ", ghostThreat
        if ghostThreat:
          evalScore = min(distToGhosts)
        elif foodList:
          distanceToClosestFood = min([manhattanDistance(newPos, food) for food in foodList])
          # print "distanceToClosestFood is ", distanceToClosestFood
          if distanceToClosestFood:
            evalScore += 1.0/distanceToClosestFood
          else:
            # print "case 1"
            evalScore += 5
        # print "evalScore is ", evalScore
        return evalScore
        # return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        currDepth = 0
        pacmanActions = gameState.getLegalActions()
        agentIndex = 0
        numberOfTurns = 0

        actionScores = []

        for action in pacmanActions:
          if action != 'Stop':
            successorState = gameState.generateSuccessor(agentIndex, action)
            value, action = (self.getValue(successorState, agentIndex, currDepth), action)
            # print "value, action is", value, action
            actionScores.append((value, action))

        bestValue, bestAction = max(actionScores)
        # print "bestValue, bestAction is\n", bestValue, bestAction
        return bestAction

    def getValue(self, gameState, agentIndex, currDepth):
      """
        Returns the value of the gameState using the minimax algorithm
      """
      print "agentIndex is", agentIndex
      # print "win", gameState.isWin()
      if agentIndex % gameState.getNumAgents() == 0:
        print "resetting agentIndex"
        agentIndex = 0
        if currDepth == self.depth:
          print "exceeding depth", currDepth, "evaluating state"
          return self.evaluationFunction(gameState)
        currDepth += 1
        # print "incrementing currDepth", currDepth
      if agentIndex == 0:
        maxValue = self.maxValue(gameState, agentIndex, currDepth)
        print "maxValue for agent", agentIndex, "is", maxValue, "\n"
        return maxValue
      if agentIndex > 0:
        minValue = self.minValue(gameState, agentIndex, currDepth)
        print "minValue for agent", agentIndex, "is", minValue, "\n"
        return minValue


    def maxValue(self, gameState, agentIndex, currDepth):
      print "maxValue running"
      # print "win in max", gameState.isWin()
      value = -1*float('inf')
      actions = gameState.getLegalActions(agentIndex)
      for step in actions:
        successor = gameState.generateSuccessor(agentIndex, step)
        print "win for successor", successor.isWin()
        value = max(value, self.getValue(successor, agentIndex + 1, currDepth))
        print "step, value", step, value
      return value

    def minValue(self, gameState, agentIndex, currDepth):
      print "minValue running"
      # print "win in min", gameState.isWin()
      value = float('inf')
      actions = gameState.getLegalActions(agentIndex)
      if actions:
        for step in actions:
          successor = gameState.generateSuccessor(agentIndex, step)

          value = min(value, self.getValue(successor, agentIndex + 1, currDepth))
          print "step, value", step, value
      return value




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

