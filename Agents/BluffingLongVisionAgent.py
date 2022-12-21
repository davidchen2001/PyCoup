from .. import CoupPlayer, CoupStrategy, CoupGame

class BluffingLongVisionAgent(CoupPlayer):
    def getAction(self, possibleActions) -> int:
        return CoupStrategy.longTermNonTruthfulStrategy(self, self.game)

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