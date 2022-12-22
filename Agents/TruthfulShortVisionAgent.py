from CoupGame import CoupGame
from CoupStrategy import *
from Agents.AutomatedAgent import AutomatedAgent

class TruthfulShortVisionAgent(AutomatedAgent):
    def __init__(self):
        super().__init__("Truthful-Short")

    def getAction(self, possibleActions) -> int:
        return shortTermTruthfulStrategy(self, self.game)

