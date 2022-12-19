from CoupActions import *
from CoupDeck import *

class CoupTurn:

    def __init__(self):
        # whose turn
        self.player = None

        # which action took place and was it successful in the end
        self.action = None
        self.actionSuccessful = None

        # who challenged the action and was the challenge successful
        self.challenger = None
        self.challengeSuccessful = None

        # who blocked the action and with which card
        self.blocker = None
        self.block_card = None

        # when someone challenges a block (e.g. I challenge Contessa)
        self.blockChallenger = None
        self.blockChallengeSuccessful = None


class CoupHistory:
    def __init__(self):
        self.turns = []
    
    def addTurn(self, turn: CoupTurn):
        if turn is not None:
            self.turns.append(turn)
