from CoupGame import CoupGame
from CoupStrategy import *
from Agents.AutomatedAgent import AutomatedAgent

class TruthfulLongVisionAgent(AutomatedAgent):
    def __init__(self):
        super().__init__("Truthful-Long")

    def getAction(self, possibleActions) -> int:
        return longTermTruthfulStrategy(self, self.game)

