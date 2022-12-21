from CoupPlayer import CoupPlayer
from CoupGame import CoupGame
from CoupStrategy import *

class BluffingLongVisionAgent(CoupPlayer):
    def __init__(self):
        super().__init__("Bluffing-Long")

    def getAction(self, possibleActions) -> int:
        return longTermNonTruthfulStrategy(self, self.game)

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