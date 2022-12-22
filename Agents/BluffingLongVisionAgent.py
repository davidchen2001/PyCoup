from CoupGame import CoupGame
from CoupStrategy import *
from Agents.AutomatedAgent import AutomatedAgent

class BluffingLongVisionAgent(AutomatedAgent):
    def __init__(self):
        super().__init__("Bluffing-Long")

    def getAction(self, possibleActions) -> int:
        return longTermNonTruthfulStrategy(self, self.game)




