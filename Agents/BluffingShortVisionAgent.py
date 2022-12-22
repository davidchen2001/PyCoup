from CoupGame import CoupGame
from CoupStrategy import *
from Agents.AutomatedAgent import AutomatedAgent

class BluffingShortVisionAgent(AutomatedAgent):
    def __init__(self):
        super().__init__("Bluffing-Short")

    def getAction(self, possibleActions) -> int:
        return shortTermNonTruthfulStrategy(self, self.game)

