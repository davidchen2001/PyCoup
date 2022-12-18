def potentialToWin(player, strategies):
    return 0

def calculateCoinsPotential(player, strategy):
    return 0

def coinsToKillPotential(player, targetPlayer, strategy):
    return 0

def generateNextStrategy(player, strategies):
    return 0

def generateNextCardAction(player, strategy):
    availableActions = player.getPossibleActions() #Need to implement a version of truthful vs non-truthful player
    bestUtility = -2
    bestAction = 0

    for action in availableActions:
        outcome = player.generateCardOutcome(action) #Need to implement hypothetical perform card action that doesn't actually change game state
        actionUtility = potentialToWin(player, strategy)
        if actionUtility > bestUtility:
            bestUtility = actionUtility
            bestAction = action
    
    return bestAction
