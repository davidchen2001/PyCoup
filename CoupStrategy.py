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

    if action == ACTION_FOR:
        #Duke Probability - Dukes don't lose anything from not blocking, so they should block

        remainingDukes = STARTING_CARDS_NUM-removedCards[CARD_DUKE]

        if playerRoles == GAMECARDS[CARD_DUKE]:
            #One less Duke in Deck
            probability = (remainingDukes-1)/remainingCardsNum

        else:
            probability = remainingDukes/remainingCardsNum
        
        #Return probability that you won't be blocked
        return 1-probability
    
    elif action == ACTION_TAX: #What's the probability a player can tax

        #Duke Probability - Duke can get tax - 3 coins

        remainingDukes = STARTING_CARDS_NUM-removedCards[CARD_DUKE]

        if playerRoles == GAMECARDS[CARD_DUKE]:
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
    
    elif action == ACTION_COU:
        #Assuming player has enough money, coup should always be a valid option
        return 1
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

        if playerRoles == GAMECARDS[CARD_DUKE]:
            #One less Duke in Deck
            probability = (remainingDukes-1)/remainingCardsNum

        else:
            probability = remainingDukes/remainingCardsNum
        
        #Return probability that you won't be blocked
        return 1-probability
    
    elif action == ACTION_TAX: #What's the probability a player can tax

        #Duke Probability - Duke can get tax - 3 coins

        remainingDukes = STARTING_CARDS_NUM-removedCards[CARD_DUKE]

        if playerRoles == GAMECARDS[CARD_DUKE]:
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
    
    elif action == ACTION_COU:
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
        utility = successfulUtilityFunction(actions[i])

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

def successfulUtilityFunction(action):
    utility = 1
        
    if action == ACTION_FOR or action == ACTION_STL:
        utility = 2/10
    elif action == ACTION_TAX:
        utility = 3/10
    
    return utility
    