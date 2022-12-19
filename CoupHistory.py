from CoupActions import *
from CoupDeck import *

class CoupTurn:

    def __init__(self, playerId : int, action : int, target:int = None):
        # whose turn
        self.playerId = playerId

        # which action took place and was it successful in the end
        self.action = action
        self.actionSuccessful = True

        # player id of the target
        self.targetId = target

        # who challenged the action and was the challenge successful
        self.challengerId = None
        self.challengeSuccessful = None

        # who blocked the action and with which card
        self.blockerId = None
        self.blockerCard = -1

        # when someone challenges a block (e.g. I challenge Contessa)
        self.blockChallengerId = None
        self.blockChallengeSuccessful = None

    def __str__(self) -> str:
        output = "---CURRENT TURN---"
        output += "\n Player Id: "
        output += str(self.playerId)
        output += "\n Action: "
        output += actionToString[self.action]
        if(self.targetId is not None):
            output += "\n Target Id: "
            output += str(self.targetId)
        if(self.challengerId is not None):
            output += "\n Challenger Id: "
            output += str(self.challengerId)
            assert self.challengeSuccessful is not None
            output += ", Challenge Success: "
            output += str(self.challengeSuccessful)
        if(self.blockerId is not None):
            output += "\n Blocker Id: "
            output += str(self.blockerId)
            assert self.blockerCard is not None
            output += " with "
            output += GAMECARDS[self.blockerCard]
        if(self.blockChallengerId is not None):
            output += "\n Block Challenger Id: "
            output += str(self.blockChallengerId)
            assert self.blockChallengeSuccessful is not None
            output += ", Block challenge success: "
            output += str(self.blockChallengeSuccessful)

        output += "\n Current action success: "
        output += str(self.actionSuccessful)

        return output

class CoupHistory:
    def __init__(self):
        self.currentOrder = []  # stores the sequence of play in terms of player id
        self.turns = []
        self.currentTurn = -1
        self.currentPlayerId = -1
        self.currentCoins = {}  # dictionary mapping player id to number of coins
    
    def newTurn(self, playerId:int, action:int, target:int = None):
        self.currentTurn += 1
        self.currentPlayerId = playerId
        self.turns.append(CoupTurn(playerId, action, target))

        #print(self.turns[self.currentTurn])

    def logChallenge(self, challengerId : int, challengeSuccess: bool):
        self.turns[self.currentTurn].challengerId = challengerId
        self.turns[self.currentTurn].challengeSuccessful = challengeSuccess

        if(challengeSuccess):
            self.turns[self.currentTurn].actionSuccessful = False    

        #print(self.turns[self.currentTurn]) 
    
    def logBlock(self, blockerId : int, blockerCard : int):
        self.turns[self.currentTurn].blockerId = blockerId
        self.turns[self.currentTurn].blockerCard = blockerCard
        self.turns[self.currentTurn].actionSuccessful = False
        #print(self.turns[self.currentTurn])

    def logBlockChallenge(self, blockChallengerId : int, blockChallengeSuccess : bool):
        self.turns[self.currentTurn].blockChallengerId = blockChallengerId
        self.turns[self.currentTurn].blockChallengeSuccessful = blockChallengeSuccess

        self.turns[self.currentTurn].actionSuccessful = not blockChallengeSuccess

        #print(self.turns[self.currentTurn])
