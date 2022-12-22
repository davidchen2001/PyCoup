from CoupPlayer import CoupPlayer
from CoupStrategy import *

class AutomatedAgent(CoupPlayer):
    def __init__(self, name):
        super().__init__(name)
    
    def getBlock(self, action) -> int:
        block = calculateBlockUtility(self, action, self.game)
        if block in [-1, ACTION_INC]:
            # do not block
            return -1

        else:
            return block

    def getChallenge(self, currentPlayerInfo, card, prob) -> bool:
        return calculateChallengeUtility(self, card, self.game)

    def exchange(self, possibleCards):
        chosenCards = []
        removedCards = self.game.getCardsRemoved()

        removedCards[self.cards[0]] -= 1
        if (self.cards[1] >= 0):
            removedCards[self.cards[1]] -= 1

        while (len(possibleCards) != 2):
            if (CARD_CONT in possibleCards) and (removedCards[CARD_ASSN] == 0):
                chosenCards.append(CARD_CONT)
                possibleCards.remove(CARD_CONT)
            elif (CARD_CAPT in possibleCards) and (removedCards[CARD_CAPT] == 0):
                chosenCards.append(CARD_CAPT)
                possibleCards.remove(CARD_CAPT)
            elif (CARD_AMBR in possibleCards) and (removedCards[CARD_CAPT] == 0):
                chosenCards.append(CARD_AMBR)
                possibleCards.remove(CARD_AMBR)
            else:
                # placeholder for strategy
                chosenCards.append(possibleCards.pop(2))

        return chosenCards

    def chooseLostCard(self):
        return self.cards[0]

    def getStealBlockCard(self):
        if CARD_AMBR in self.cards:
            return CARD_AMBR
        elif CARD_CAPT in self.cards:
            return CARD_CAPT
        captainsRemaining = self.game.getCardsRemoved()[CARD_CAPT]
        ambassRemaining = self.game.getCardsRemoved()[CARD_AMBR]
        if (captainsRemaining >= ambassRemaining):
            return CARD_CAPT
        else:
            return CARD_AMBR

    def getTarget(self, possibleTargets) -> int:
        if (len(possibleTargets) == 1):
            return possibleTargets[0]

        else:
            maxCoins = -1
            richestId = -1
            for id in possibleTargets:
                coinCount = self.history.currentCoins[id]
                if (coinCount > maxCoins):
                    maxCoins = coinCount
                    richestId = id
            return richestId
            
