from CoupPlayer import CoupPlayer
from CoupGame import CoupGame
from CoupStrategy import *

class BluffingShortVisionAgent(CoupPlayer):
    def getAction(self, possibleActions) -> int:
        return shortTermNonTruthfulStrategy(self, self.game)

    def getTarget(self, possibleTargets) -> int:
        raise NotImplementedError()
    
    def getBlock(self, action) -> int:
        raise NotImplementedError()

    def getChallenge(self, currentPlayerInfo, card, prob) -> bool:
        raise NotImplementedError()

    def exchange(self, possibleCards):
        raise NotImplementedError()

    def chooseLostCard(self):
        return self.cards[0]