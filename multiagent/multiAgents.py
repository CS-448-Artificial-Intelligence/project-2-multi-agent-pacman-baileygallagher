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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def closestGhostDistance(self, currentGameState):
        newPos = currentGameState.getPacmanPosition()
        newGhostStates = currentGameState.getGhostStates()
        ghosts = currentGameState.getGhostPositions()
        if len(ghosts) == 0:
            return 0
        ghostState = newGhostStates[0]
        ghostPos = ghostState.configuration.pos
        pacmanPos = newPos
        return util.manhattanDistance(pacmanPos, ghostPos)

    def closestFoodDistance(self, currentGameState):
        newFood = currentGameState.getFood()  # .asList()
        pacPos = currentGameState.getPacmanPosition()
        minDistance = float('inf')
        foodDistance = 1
        for col in range(newFood.width):
            # current_column = newFood[col]
            int_col = int(col)
            for row in range(newFood.height):
                int_row = int(row)

                # (col, row)
                # currentPosition = currentRow[y]
                if newFood[int_col][int_row]:
                    # positionTuple = (int_col, int_row)
                    # foodDistance = float(util.manhattanDistance(pacPos, positionTuple))
                    pac_x = int(pacPos[0])
                    pac_y = int(pacPos[1])
                    foodDistance = abs(pac_x - int_col) + abs(pac_y - int_row)
                    if float(foodDistance) < minDistance:
                        minDistance = foodDistance

        return minDistance

    def numGhosts(self, currentGameState):
        number = currentGameState.getGhostPositions()
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
        capsules = len(currentGameState.getCapsules())
        "*** YOUR CODE HERE ***"
        numFood = successorGameState.getNumFood()
        ghosts = successorGameState.getGhostPositions()

        closetGhost = self.closestGhostDistance(successorGameState)
        successorClosestFood = self.closestFoodDistance(successorGameState)
        currentClosestFood = self.closestFoodDistance(currentGameState)
        score = scoreEvaluationFunction(successorGameState)

        food_score = 0
        if successorClosestFood < currentClosestFood:
            # make food value worth more if pacman is getting closer to food
            food_score = 100 * 1 / successorClosestFood
        else:
            food_score = 10 * 1 / successorClosestFood

        if numFood == 0:
            numFood = 1
        total_food_left = 100 * 1 / numFood

        ghost_score = 0
        if 4 > closetGhost > 0:
            ghost_score = -1 * (100 * 1 / closetGhost)
        # print("FoodScore: %f, GhostScore: %f" % (food_score, ghost_score))
        score = score + ghost_score + food_score + total_food_left
        return score
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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def calculateMax(self, gameState, turn, current_depth):
        if gameState.isWin() or gameState.isLose() or current_depth == self.depth:
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
            nextState = gameState.generateSuccessor(turn, current_action)

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
    # need to add capsules in, otherwise pacman gets stuck
    if currentGameState.isWin():
        score = float("inf")
        return score
    if currentGameState.isLose():
        score = float("-inf")
        return score
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    "*** YOUR CODE HERE ***"
    numFood = currentGameState.getNumFood()
    closest_cap_distance = closestCapsuleDistance(currentGameState)
    closetGhost = closestGhostDistance(currentGameState)
    currentClosestFood = closestFoodDistance(currentGameState)
    score = scoreEvaluationFunction(currentGameState)
    cap_score = 0
    if closest_cap_distance > currentClosestFood > 0:
        # make food value worth less if pacman is getting closer to cap than food!
        food_score = 50 * 1 / currentClosestFood
    else:
        food_score = 100 * 1 / currentClosestFood

    if numFood == 0:
        numFood = 1
    total_food_left = 300 * 1 / numFood

    ghost_score = 0
    if 4 > closetGhost > 0:
        ghost_score = -1 * (50 * 1 / closetGhost)
    if newScaredTimes[0] > 0:
        ghost_score = 20
    if closest_cap_distance != 0:
        cap_score = 5 * (1 / closest_cap_distance)
    score = score + ghost_score + food_score + total_food_left + cap_score
    return score


def closestGhostDistance(currentGameState):
    newPos = currentGameState.getPacmanPosition()
    newGhostStates = currentGameState.getGhostStates()
    ghosts = currentGameState.getGhostPositions()
    if len(ghosts) == 0:
        return 0
    ghostState = newGhostStates[0]
    ghostPos = ghostState.configuration.pos
    pacmanPos = newPos
    return util.manhattanDistance(pacmanPos, ghostPos)

def closestCapsuleDistance(currentGameState):
    pacmanPos = currentGameState.getPacmanPosition()
    caps = currentGameState.getCapsules()
    min_distance = float("inf")
    if len(caps) == 0:
        return 0
    for tuple in caps:
        if util.manhattanDistance(pacmanPos, tuple) < min_distance:
            min_distance = util.manhattanDistance(pacmanPos, tuple)
            # don't need closest_cap_pos but may use later ? keeping for now
            # closest_capPos = tuple
    return min_distance

def closestFoodDistance( currentGameState):
    newFood = currentGameState.getFood()  # .asList()
    pacPos = currentGameState.getPacmanPosition()
    minDistance = float('inf')
    foodDistance = 1
    for col in range(newFood.width):
        # current_column = newFood[col]
        int_col = int(col)
        for row in range(newFood.height):
            int_row = int(row)

            # (col, row)
            # currentPosition = currentRow[y]
            if newFood[int_col][int_row]:
                # positionTuple = (int_col, int_row)
                # foodDistance = float(util.manhattanDistance(pacPos, positionTuple))
                pac_x = int(pacPos[0])
                pac_y = int(pacPos[1])
                foodDistance = abs(pac_x - int_col) + abs(pac_y - int_row)
                if float(foodDistance) < minDistance:
                    minDistance = foodDistance

    return minDistance


def numGhosts(currentGameState):
    number = currentGameState.getGhostPositions()
    return len(number)


# Abbreviation
better = betterEvaluationFunction
