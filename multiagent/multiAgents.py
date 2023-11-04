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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def closestGhostDistance(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newGhostStates = successorGameState.getGhostStates()
        ghosts = successorGameState.getGhostPosition()
        if ghosts.isEmpty():
            return 0
        ghostPos = newGhostStates[0]
        pacmanPos = newPos
        return util.manhattanDistance(pacmanPos, ghostPos)
    def closestFoodDistance(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newFood = successorGameState.getFood()
        pacPos = successorGameState.getPacmanPosition()
        minDistance = float('inf')
        foodDistance = 1
        for x in range(newFood.width):
            #currentRow = newFood[x]
            int_x = int(x)
            for y in range(newFood.height):
                int_y = int(y)
                #currentPosition = currentRow[y]
                if newFood[x][y] is True:
                    positionTuple = (int_x, int_y)
                   # foodDistance = float(util.manhattanDistance(pacPos, positionTuple))

                    foodDistance = abs(pacPos[0] - int_x) + abs(pacPos[1] - int_y)
                    if float(foodDistance) < minDistance:
                        minDistance = foodDistance

        return minDistance
    # should be similar logic for closest ghost and capsules once food works

    '''def closestCapsules(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newCap = successorGameState.getCapsules()
        pacPos = successorGameState.getPacmanPosition()
        minDistance = float('inf')
        capDistance = 1
        for x in range(newCap.width):
            # currentRow = newFood[x]
            int_x = int(x)
            for y in range(newCap.height):
                int_y = int(y)
                # currentPosition = currentRow[y]
                if newCap[x][y] is True:
                    positionTuple = (int_x, int_y)
                    # capDistance = float(util.manhattanDistance(pacPos, positionTuple))

                    capDistance = abs(pacPos[0] - int_x) + abs(pacPos[1] - int_y)
                    if float(capDistance) < minDistance:
                        minDistance = capDistance

        return minDistance'''

    def numGhosts(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        number = successorGameState.getGhostPositions()
        return len(number)



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
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        print(newScaredTimes)
        "*** YOUR CODE HERE ***"
        numFood = successorGameState.getNumFood()
        ghosts = successorGameState.getGhostPositions()
        numGhosts = self.numGhosts(currentGameState, action)
        closestFood = self.closestFoodDistance(currentGameState, action)
        #numCapsules = self.closestCapsules(currentGameState, action)
        score = 0
        score = (numFood / numGhosts) / (newScaredTimes[0] + 1)
        return score


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
    def calculateMax(self, gameState, turn, current_depth):
        if gameState.isWin() or gameState.isLose()  or current_depth == self.depth:
            return (self.evaluationFunction(gameState), None)

        value = float("-inf")
        result_action = None
        for current_action in gameState.getLegalActions(turn):
            nextState = gameState.generateSuccessor(turn, current_action)
            # change here for alpha beta
            nextValueAction = self.calculateMin(nextState, turn + 1, current_depth)
            nextValue = nextValueAction[0]
            if nextValue > value:
                # making next value our new MAX, updating our action to go along with new MAX
                value = nextValue
                result_action = current_action
        # returning max value and its corresponding action
        return (value, result_action)

    def calculateMin(self, gameState, turn, current_depth):
        if gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), None)

        value = float("inf")
        result_action = None
        for current_action in gameState.getLegalActions(turn):
            nextState = gameState.generateSuccessor(turn , current_action)

            # Pacman's turn is next
            if turn == gameState.getNumAgents() - 1:
                nextValueAction = self.calculateMax(nextState, 0, current_depth + 1)
            else:
                # A ghost is up next
                nextValueAction = self.calculateMin(nextState, turn + 1, current_depth)

            nextValue = nextValueAction[0]
            if nextValue < value:
                value = nextValue
                result_action = current_action
        return (value, result_action)
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # turn is 0 (pacman) or turn is greater than 0 (opponent/ghosts)
        pacman_turn = 0
        starting_depth = 0
        return self.calculateMax(gameState, pacman_turn, starting_depth)[1]



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    # add parameters (alpha, beta)
    def calculateMax(self, gameState, turn, current_depth, alpha, beta):

        if gameState.isWin() or gameState.isLose() or current_depth == self.depth:
            return (self.evaluationFunction(gameState), None)

        value = float("-inf")
        result_action = None
        for current_action in gameState.getLegalActions(turn):
            nextState = gameState.generateSuccessor(turn, current_action)
            # change here for alpha beta, add params alpha beta
            # NextValue = v
            nextValueAction = self.calculateMin(nextState, turn + 1, current_depth, alpha, beta)
            nextValue = nextValueAction[0]
            if nextValue > value:
                # making next value our new MAX, updating our action to go along with new MAX
                value = nextValue
                result_action = current_action
            # if value > = beta, return value, current action IE PRUNE the other children
            # reassign alpha = max(alpha,value)
            if value > beta:
                return (value, result_action)
            alpha = max(alpha, value)
        # returning max value and its corresponding action
        return (value, result_action)

    def calculateMin(self, gameState, turn, current_depth, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), None)

        value = float("inf")
        result_action = None
        for current_action in gameState.getLegalActions(turn):
            nextState = gameState.generateSuccessor(turn, current_action)

            # Pacman's turn is next
            if turn == gameState.getNumAgents() - 1:
                nextValueAction = self.calculateMax(nextState, 0, current_depth + 1, alpha, beta)
            else:
                # A ghost is up next
                nextValueAction = self.calculateMin(nextState, turn + 1, current_depth, alpha, beta)

            nextValue = nextValueAction[0]
            if nextValue < value:
                value = nextValue
                result_action = current_action
            if value < alpha:
                return (value, result_action)
            beta = min(beta, value)

        return (value, result_action)

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # turn is 0 (pacman) or turn is greater than 0 (opponent/ghosts)
        pacman_turn = 0
        starting_depth = 0
        alpha = float("-inf")
        beta = float("inf")
        return self.calculateMax(gameState, pacman_turn, starting_depth, alpha, beta)[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    # keep max the same as minimax, modify min function to calculate expected value instead
    # think you take probability as uniformly at random so like length of successor list = 4, divide all expected values
    # by four to get weighted avg. keep get action the same as minimax too
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        pacman_turn = 0
        starting_depth = 0
        return self.calculateMax(gameState, pacman_turn, starting_depth)[1]

    def calculateMax(self, gameState, turn, current_depth):
        if gameState.isWin() or gameState.isLose() or current_depth == self.depth:
            return (self.evaluationFunction(gameState), None)

        value = float("-inf")
        result_action = None
        for current_action in gameState.getLegalActions(turn):
            nextState = gameState.generateSuccessor(turn, current_action)
            # change here for alpha beta
            nextValueAction = self.calculateExp(nextState, turn + 1, current_depth)
            nextValue = nextValueAction[0]
            if nextValue > value:
                # making next value our new MAX, updating our action to go along with new MAX
                value = nextValue
                result_action = current_action
        # returning max value and its corresponding action
        return (value, result_action)

    def calculateExp(self, gameState, turn, current_depth):
        if gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), None)

        result_action = None
        # finding number to divide by for probability average
        num_options = len(gameState.getLegalActions(turn))
        value = 0
        for current_action in gameState.getLegalActions(turn):
            nextState = gameState.generateSuccessor(turn, current_action)

            # Pacman's turn is next
            if turn == gameState.getNumAgents() - 1:
                nextValueAction = self.calculateMax(nextState, 0, current_depth + 1)
            else:
                # A ghost is up next
                nextValueAction = self.calculateExp(nextState, turn + 1, current_depth)

            nextValue = nextValueAction[0]
            probability = 1 / num_options
            value += probability * nextValue
            result_action = current_action
        return (value, result_action)

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
