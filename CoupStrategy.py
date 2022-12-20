from CoupActions import *
from CoupDeck import GAMECARDS, CARD_AMBR, CARD_ASSN, CARD_CONT, CARD_CAPT, CARD_DUKE

def potentialToWin(player, players, game):

    totalPotential = 0
    totalAgentCoinsToKillPotential = 0

    for p in players:
        if player != p and p.getIsPlayer() == True:
            getCoinsPotential = calculateCoinsPotential(p, game)
            playerCoinsToKillPotential = coinsToKillPotential(p, player, game)

            #1 represents number of active cards. It will be 1 due to endgame scenario
            playerPotential = 1 * (p.getCoins() + getCoinsPotential)/playerCoinsToKillPotential
            totalPotential += playerPotential

            agentPlayerCoinToKillPotential = coinsToKillPotential(player, p, game)
            totalAgentCoinsToKillPotential += agentPlayerCoinToKillPotential
    
    agentCoinPotential = calculateCoinsPotential(player, game)
    agentCoinsToKillPotential = totalAgentCoinsToKillPotential/(len(players))
    agentPotential = 1 * (player.getCoins() + agentCoinPotential)/agentCoinsToKillPotential
    totalPotential += agentPotential

    return agentPotential/totalPotential

def calculateCoinsPotential(player, players, game):
    incomeProb = 1 #No player can block this action
    foreignAidProb = calculateActionSuccessProbability(player, ACTION_FOR, game)
    taxProb = calculateActionSuccessProbability(player, ACTION_TAX, game)
    stealProb = calculateActionSuccessProbability(player, ACTION_STL, game)

    gettingStolenProb = 0

    for p in players:
        if p != player and p.getIsPlaying() == True:
            stolenProb = probabilityGetStolenFrom(player, p, game)
            gettingStolenProb += stolenProb

    return 3 * taxProb + 2* foreignAidProb + 1 * incomeProb + 2 *stealProb - 2 *gettingStolenProb

def coinsToKillPotential(player, game):
    assassinateProb = calculateActionSuccessProbability(player, ACTION_ASS, game)
    coinsToKill = 3 * assassinateProb
    return coinsToKill

def generateNextStrategy(player, game):
    availableActions = player.getPossibleActions()
    regretForNotPlayingActions = {}

    for action in availableActions:
        generalStratUtility = 0
        actionsUtility = 0

        possibleOutcomes = game.generatePossibleOutcomes(action) #Need to implement

        #for outcome in possibleOutcomes:
            #utility += 

    return 0

def generateNextCardAction(player, players, game):
    availableActions = player.getPossibleActions() #Need to implement a version of truthful vs non-truthful player
    bestUtility = -2
    bestAction = 0

    for action in availableActions:
        outcome = player.generateCardOutcome(action) #Need to implement hypothetical perform card action that doesn't actually change game state
        actionUtility = potentialToWin(player, players, game)
        if actionUtility > bestUtility:
            bestUtility = actionUtility
            bestAction = action
    
    return bestAction

def calculateActionSuccessProbability(player, action, game):
    playerRoles = player.getHandString()
    remainingCardsNum = game.getNumCardsRemaining()
    removedCards = game.getCardsRemoved()
    
    probability = 0

    if action == ACTION_FOR:
        #Duke Probability - Dukes don't lose anything from not blocking, so they should block

        remainingDukes = 5-removedCards[CARD_DUKE]

        if playerRoles == GAMECARDS[CARD_DUKE]:
            #One less Duke in Deck
            probability = (remainingDukes-1)/remainingCardsNum

        else:
            probability = remainingDukes/remainingCardsNum
        
        #Return probability that you won't be blocked
        return 1-probability
    
    elif action == ACTION_TAX: #What's the probability a player can tax

        #Duke Probability - Duke can get tax - 3 coins

        remainingDukes = 5-removedCards[CARD_DUKE]

        if playerRoles == GAMECARDS[CARD_DUKE]:
            probability = 1
        else:
            probability = remainingDukes/remainingCardsNum
        
        return probability
    
    elif action == ACTION_STL:

        #Probability that player is a captain and another captain and ambassador doesn't block it

        remainingCaptains = 5 - removedCards[CARD_CAPT]
        remainingAmbassador = 5 - removedCards[CARD_AMBR]

        if playerRoles == GAMECARDS[CARD_CAPT]:
            
            probability = (remainingCaptains-1 + remainingAmbassador)/remainingCardsNum
            probability = 1-probability
        
        else:
            probability = (remainingCaptains + remainingAmbassador)/remainingCardsNum
            probability = 1-probability
        
        return probability
    elif action == ACTION_ASS:
        #Probability that a player is not contessa - and that will be when assassination is successful

        remainingContessa = 5 - removedCards[CARD_CONT]

        probability = remainingContessa/remainingCardsNum

        return 1-probability
    
    elif action == ACTION_COU:
        #Assuming player has enough money, coup should always be a valid option
        return 1
    elif action == ACTION_EXC:
        #Probability that a player has ambassador
        remainingAmbassador = 5 - removedCards[CARD_AMBR]

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

        remainingDukes = 5-removedCards[CARD_DUKE]

        if playerRoles == GAMECARDS[CARD_DUKE]:
            #One less Duke in Deck
            probability = (remainingDukes-1)/remainingCardsNum

        else:
            probability = remainingDukes/remainingCardsNum
        
        #Return probability that you won't be blocked
        return 1-probability
    
    elif action == ACTION_TAX: #What's the probability a player can tax

        #Duke Probability - Duke can get tax - 3 coins

        remainingDukes = 5-removedCards[CARD_DUKE]

        if playerRoles == GAMECARDS[CARD_DUKE]:
            probability = 1
        else:
            probability = remainingDukes/remainingCardsNum
        
        return probability
    
    elif action == ACTION_STL:

        #Probability that player is a captain and another captain and ambassador doesn't block it

        remainingCaptains = 5 - removedCards[CARD_CAPT]
        remainingAmbassador = 5 - removedCards[CARD_AMBR]

        if playerRoles == GAMECARDS[CARD_CAPT]:
            
            probability = (remainingCaptains-1 + remainingAmbassador)/remainingCardsNum
            probability = 1-probability
        
        else:
            probability = (remainingCaptains + remainingAmbassador)/remainingCardsNum
            probability = 1-probability
        
        return probability
    elif action == ACTION_ASS:
        #Probability that a player is not contessa - and that will be when assassination is successful

        remainingContessa = 5 - removedCards[CARD_CONT]

        probability = remainingContessa/remainingCardsNum

        return 1-probability
    
    elif action == ACTION_COU:
        #Assuming player has enough money, coup should always be a valid option
        return 1
    elif action == ACTION_EXC:
        #Probability that a player has ambassador
        remainingAmbassador = 5 - removedCards[CARD_AMBR]

        probability = remainingAmbassador/remainingCardsNum
        return probability

def probabilityGetStolenFrom(player, opponent, game):
    #player steals from opponent

    #Probability that you are a ambassador/captain
    remainingCardsNum = game.getNumCardsRemaining()
    removedCards = game.getCardsRemoved()

    remainingCaptains = 5 - removedCards[CARD_CAPT]
    remainingAmbassador = 5 - removedCards[CARD_AMBR]

    probability = (remainingCaptains + remainingAmbassador)/remainingCardsNum
    return probability

def probabilityOutcome(player):
    return 1/player.getPossibleActions()

def shortTermStrategy(player, actions, game):
    utilityMap = {}
    maxUtility = 0

    for i in range(len(actions)):
        probability = calculateShortTermActionSuccessProbability(player, actions[i], actions, game)
        utility = 1
        
        if actions[i] == ACTION_FOR or actions[i] == ACTION_STL:
            utility = 2/10
        elif actions[i] == ACTION_TAX:
            utility = 3/10

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
