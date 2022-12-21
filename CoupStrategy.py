from CoupActions import *
from CoupDeck import GAMECARDS, CARD_AMBR, CARD_ASSN, CARD_CONT, CARD_CAPT, CARD_DUKE

STARTING_CARDS_NUM = 3

def longTermNonTruthfulStrategy(player, game):
    actions = player.getPossibleActions()
    return longTermStrategy(player, actions, game)

def longTermTruthfulStrategy(player, game):
    actions = player.getPossibleTruthfulActions()
    return longTermStrategy(player, actions, game)

def longTermStrategy(player, actions, game):
    utilityMap = {}
    maxUtility = 0

    for i in range(len(actions)):

        #Find each outcome that could come from each action
        #Find utility of each outcome
        #Find probability of each outcome happening
        outcomes = game.generatePossibleOutcomes(player, actions[i], game)

        utilityMap[actions[i]] = outcomes[actions[i]]
        if maxUtility < outcomes[actions[i]]:
            maxUtility = outcomes[actions[i]]
    
    bestAction = actions[0]

    for key in utilityMap:
        if utilityMap[key] == maxUtility:
            bestAction = key

    return bestAction

def calculateActionSuccessProbability(player, action, game):
    playerRoles = player.getHandString()
    remainingCardsNum = game.getNumCardsRemaining()
    removedCards = game.getCardsRemoved()
    
    probability = 0

        
    if action in [ACTION_INC, ACTION_COU]:
        #Income and Coup always have 100% probability
        #Assuming player has enough money, coup should always be a valid option
        return 1

    elif action == ACTION_FOR:
        #Duke Probability - Dukes don't lose anything from not blocking, so they should block

        remainingDukes = STARTING_CARDS_NUM-removedCards[CARD_DUKE]

        # subtract number of dukes in player's hand
        myDukeCount = playerRoles.count(GAMECARDS[CARD_DUKE])
        remainingDukes -= myDukeCount

        probability = remainingDukes/remainingCardsNum
        
        #Return probability that you won't be blocked
        return 1-probability
    
    elif action == ACTION_TAX: #What's the probability a player can tax

        #Duke Probability - Duke can get tax - 3 coins

        remainingDukes = STARTING_CARDS_NUM-removedCards[CARD_DUKE]

        if GAMECARDS[CARD_DUKE] in playerRoles:
            probability = 1
        else:
            probability = remainingDukes/remainingCardsNum
        
        return probability
    
    elif action == ACTION_STL:

        #Probability that player is a captain and another captain/ambassador doesn't block it

        remainingCaptains = STARTING_CARDS_NUM - removedCards[CARD_CAPT]
        remainingAmbassador = STARTING_CARDS_NUM - removedCards[CARD_AMBR]

        # count how many captains are in current player's hand
        myCaptCount = playerRoles.count(GAMECARDS[CARD_CAPT])
        remainingCaptains -= myCaptCount            

        probability = (remainingCaptains + remainingAmbassador)/remainingCardsNum
        probability = 1-probability
        
        return probability
    elif action == ACTION_ASS:
        #Probability that a player is not contessa - and that will be when assassination is successful

        remainingContessa = STARTING_CARDS_NUM - removedCards[CARD_CONT]

        probability = remainingContessa/remainingCardsNum

        return 1-probability

    elif action == ACTION_EXC:
        #Probability that a player has ambassador
        remainingAmbassador = STARTING_CARDS_NUM - removedCards[CARD_AMBR]

        probability = remainingAmbassador/remainingCardsNum
        return probability

def calculateShortTermActionSuccessProbability(player, action, actions, game):
    playerRoles = player.getHandString()
    remainingCardsNum = game.getNumCardsRemaining()
    removedCards = game.getCardsRemoved()

    probability = 0

    if action in actions:
        return 1

    elif action == ACTION_FOR:
        #Duke Probability - Dukes don't lose anything from not blocking, so they should block

        remainingDukes = STARTING_CARDS_NUM-removedCards[CARD_DUKE]

        # subtract number of dukes in player's hand
        myDukeCount = playerRoles.count(GAMECARDS[CARD_DUKE])
        remainingDukes -= myDukeCount

        probability = remainingDukes/remainingCardsNum
        
        #Return probability that you won't be blocked
        return 1-probability
    
    elif action == ACTION_TAX: #What's the probability a player can tax

        #Duke Probability - Duke can get tax - 3 coins

        remainingDukes = STARTING_CARDS_NUM-removedCards[CARD_DUKE]

        if GAMECARDS[CARD_DUKE] in playerRoles:
            probability = 1
        else:
            probability = remainingDukes/remainingCardsNum
        
        return probability
    
    elif action == ACTION_STL:

        #Probability that player is a captain and another captain and ambassador doesn't block it

        remainingCaptains = STARTING_CARDS_NUM - removedCards[CARD_CAPT]
        remainingAmbassador = STARTING_CARDS_NUM - removedCards[CARD_AMBR]

        if playerRoles == GAMECARDS[CARD_CAPT]:
            
            probability = (remainingCaptains-1 + remainingAmbassador)/remainingCardsNum
            probability = 1-probability
        
        else:
            probability = (remainingCaptains + remainingAmbassador)/remainingCardsNum
            probability = 1-probability
        
        return probability
    elif action == ACTION_ASS:
        #Probability that a player is not contessa - and that will be when assassination is successful

        remainingContessa = STARTING_CARDS_NUM - removedCards[CARD_CONT]

        probability = remainingContessa/remainingCardsNum

        return 1-probability
    
    elif action in [ACTION_INC, ACTION_COU]:
        #Income and Coup always have 100% probability
        #Assuming player has enough money, coup should always be a valid option
        return 1
    elif action == ACTION_EXC:

        #Probability that a player has ambassador
        remainingAmbassador = STARTING_CARDS_NUM - removedCards[CARD_AMBR]

        probability = remainingAmbassador/remainingCardsNum
        return probability

def shortTermStrategy(player, actions, game):
    utilityMap = {}
    maxUtility = 0

    for i in range(len(actions)):
        probability = calculateShortTermActionSuccessProbability(player, actions[i], actions, game)
        utility = utilityGainFunction(actions[i])

        utility *= probability

        utilityMap[actions[i]] = utility
        if maxUtility < utility:
            maxUtility = utility
    
    bestAction = actions[0]

    for key in utilityMap:
        if utilityMap[key] == maxUtility:
            bestAction = key

    return bestAction

def shortTermNonTruthfulStrategy(player, game):
    actions = player.getPossibleActions()
    return shortTermStrategy(player, actions, game)

def shortTermTruthfulStrategy(player, game):
    actions = player.getTruthfulActions()
    return shortTermStrategy(player, actions, game)

def utilityGainFunction(action):
    #Assuming action was successful

    utility = 0
    killUtility = 100

    if action == ACTION_ASS:
        utility = killUtility - 3
    
    elif action == ACTION_COU:
        utility = killUtility - 7
    
    elif action == ACTION_STL:
        utility += 2
    
    elif action == ACTION_TAX:
        utility += 3

    elif action == ACTION_INC:
        utility += 1
    
    elif action == ACTION_FOR:
        utility += 2

    else:
        #Exchange
        utility = 0
    return utility

def utilityLossFunction(action):
    
    utility = 0
    deathUtility = -100

    if action == ACTION_COU or action == ACTION_ASS:
        utility = deathUtility

    elif action == ACTION_STL:
        utility -= 2


