def potentialToWin(player, players, strategies):
    #strategies parameter?

    totalPotential = 0
    totalAgentCoinsToKillPotential = 0

    for p in players:
        if player != p and p.getIsPlayer() == True:
            getCoinsPotential = calculateCoinsPotential(p, strategies)
            playerCoinsToKillPotential = coinsToKillPotential(p, player, strategies)

            #1 represents number of active cards. It will be 1 due to endgame scenario
            playerPotential = 1 * (p.getCoins() + getCoinsPotential)/playerCoinsToKillPotential
            totalPotential += playerPotential

            agentPlayerCoinToKillPotential = coinsToKillPotential(player, p, strategies)
            totalAgentCoinsToKillPotential += agentPlayerCoinToKillPotential
    
    agentCoinPotential = calculateCoinsPotential(player, strategies)
    agentCoinsToKillPotential = totalAgentCoinsToKillPotential/(len(players))
    agentPotential = 1 * (player.getCoins() + agentCoinPotential)/agentCoinsToKillPotential
    totalPotential += agentPotential

    return agentPotential/totalPotential

def calculateCoinsPotential(player, strategy):
    return 0

def coinsToKillPotential(player, targetPlayer, strategy):
    return 0

def generateNextStrategy(player, strategies):
    return 0

def generateNextCardAction(player, players, strategy):
    availableActions = player.getPossibleActions() #Need to implement a version of truthful vs non-truthful player
    bestUtility = -2
    bestAction = 0

    for action in availableActions:
        outcome = player.generateCardOutcome(action) #Need to implement hypothetical perform card action that doesn't actually change game state
        actionUtility = potentialToWin(player, players, strategy)
        if actionUtility > bestUtility:
            bestUtility = actionUtility
            bestAction = action
    
    return bestAction
