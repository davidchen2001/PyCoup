from CoupActions import *
from CoupDeck import GAMECARDS, CARD_AMBR, CARD_ASSN, CARD_CAPT, CARD_CONT, CARD_DUKE
from CoupHistory import *

class CoupPlayer:
    next_id = 100

    def __init__(self, name):
        self.name = name
        self.newGame()
        self.id = CoupPlayer.next_id
        CoupPlayer.next_id += 1
        
    def newGame(self):
        self.coins = 2
        self.cards = [-2, -2]
        self.numCards = 0
        self.isAlive = True
        self.isPlaying = False
        self.history = None
        self.game = None
        
    def getIsPlaying(self):
        return self.isPlaying
    
    def setIsPlaying(self, value):
        self.isPlaying = value
    
    def getCoins(self):
        return self.coins

    def die(self):
        self.isAlive = False

    # add CoupGame reference to player
    def attachGame(self, game):
        self.game = game

    # add CoupHistory reference to player
    def attachHistory(self, history):
        assert isinstance(history, CoupHistory)
        self.history = history

    # ask player which card to lose from their hand
    # returns card ID (not indice)
    def chooseLostCard(self):
        print("--- (" + self.name + ") Choose which cards to lose:")
        chosen = -1
        while (chosen == -1):
            for i in range(len(self.cards)):
                print("------ " + str(i) + ") " + GAMECARDS[self.cards[i]])
            user_input = input()
            try:
                user_input = int(user_input)
                assert (user_input < len(self.cards))
                assert (user_input >= 0)
                chosen = self.cards[user_input]
                return chosen

            except:
                print("------- Invalid input received.")
        
    def lose_card(self):
        lost = self.cards[0]
        if (self.numCards == 2):
            lost = self.chooseLostCard()

        self.numCards -= 1
        if(lost==self.cards[0]):
            self.cards[0] = -2
        else:
            self.cards[1] = -2
        
        #check if player is alive
        if(self.numCards <= 0):
            self.die()
        elif(self.cards[0] == -2):
            # make the "dead" card second in their hand
            self.cards[0], self.cards[1] = self.cards[1], self.cards[0]

        return lost
    
    def getStatusString(self):
        output = "------ Current hand: "
        output += self.getHandString()
        output += " and "
        output += str(self.coins)
        output += " coins"
        return output

    def getHandString(self):
        if ((self.isAlive == False) or (self.numCards == 0)):
            return "No cards"
        else:
            if self.cards[0] == -2:
                assert self.cards[1] == -2

            output = []
            for i in range(self.numCards):
                if (self.cards[i] >= 0):
                    output.append(GAMECARDS[self.cards[i]])
                else:
                    print("Card at index x is:", i, self.cards[i], self.cards)
            return str(output)

    def getPossibleActions(self):
        actions = []
        if self.coins < 3:
            actions = ([ACTION_EXC, ACTION_STL, ACTION_TAX, ACTION_INC, ACTION_FOR])
        elif self.coins < 7:
            actions = ([ACTION_ASS, ACTION_EXC, ACTION_STL, ACTION_TAX, ACTION_INC, ACTION_FOR])
        elif self.coins < 10:
            actions = ([ACTION_ASS, ACTION_EXC, ACTION_STL, ACTION_TAX, ACTION_INC, ACTION_FOR, ACTION_COU])
        else:
            actions = ([ACTION_COU])
        
        if (self.game.noSteal()):
            # if it is not possible to steal (i.e. all players have 0 coins)
            actions.remove(ACTION_STL)

        return actions
    
    def getPossibleTruthfulActions(self):
        actions = self.getPossibleActions()

        if (ACTION_EXC in actions) and (CARD_AMBR not in self.cards):
            actions.remove(ACTION_EXC)
        if (ACTION_ASS in actions) and (CARD_ASSN not in self.cards):
            actions.remove(ACTION_ASS)               
        if (ACTION_STL in actions) and (CARD_CAPT not in self.cards):
            actions.remove(ACTION_STL)
        if (ACTION_TAX in actions) and (CARD_DUKE not in self.cards):
            actions.remove(ACTION_TAX)

        return actions.sort()

    def getAction(self, possibleActions) -> int:
        #how will we ensure player knows game state?
        
        while(True):
            print("--- Type H for help, C for my cards and coins")
            user_input = input("--- (" + self.name + ") Which action to play? ")
            if (user_input.lower() == "h") or (user_input.lower() == "help"):
                for i in possibleActions:
                    print("------ " + str(i) + " - " + actionToString[i])
                continue
            elif (user_input.lower() == "c") or ("coin" in user_input.lower()) or ("card" in user_input.lower()):
                print(self.getStatusString())
                continue

            try:
                action = int(user_input)
                assert(action in possibleActions)
                return action
            except:
                print("------- Invalid action input received.")

    # for actions with a target, return player # to target
    def getTarget(self, possibleTargets) -> int:
        #how will we ensure player knows game state?
        
        while(True):
            user_input = input("--- Who would you like to target? ")
            try:
                player_index = int(user_input)
                assert player_index in possibleTargets
                return player_index
            except:
                print("------- Invalid target input received.")

    # ask player which card to block with, or don't block at all (-1)
    def getBlock(self, action) -> int:
        possibleBlocks = []

        prompt = "--- (" + self.name + ") You are the target of "
        
        if action == ACTION_ASS:
            possibleBlocks.append(CARD_CONT)

        elif action == ACTION_STL:
            possibleBlocks.append(CARD_AMBR)
            possibleBlocks.append(CARD_CAPT)

        elif action == ACTION_FOR:
            prompt = "--- (" + self.name + ") A player wants to use "
            possibleBlocks.append(CARD_DUKE)

        prompt += actionToString[action]
        prompt += ". Do you want to block this action?\n"
        prompt += "------ Type N for no block\n"
        prompt += "------ Type C to view my cards and coins\n"

        for card in possibleBlocks:
            prompt += "------ Type " + str(card) + " to block with " + GAMECARDS[card] + "\n"

        while(True):
            user_input = input(prompt)
            try:
                if (user_input.lower() == "n"):
                    user_input = -1
                elif ((user_input.lower() == "c") or (user_input.lower() == "n")):
                    print(self.getStatusString())
                    continue
                else:
                    user_input = int(user_input)
                assert (user_input in possibleBlocks) or (user_input == -1)
                break
            except:
                print("------- Invalid input received.")

        return user_input   

    # asks user whether they want to challenge an action
    # returns True if they want to challenge, False if they do not
    def getChallenge(self, currentPlayerInfo, card, prob) -> bool:

            prompt = "--- (" + self.name + ") "
            prompt += currentPlayerInfo["name"]
            prompt += " claims to have " 
            prompt += GAMECARDS[card]
            prompt += ", probability of truth = "
            prompt += str(prob)
            prompt += ". Challenge? (Y/N) "

            while(True):
                user_input = input(prompt)
                if (user_input.lower() == "n"):
                    return False
                elif (user_input.lower() == "y"):
                    return True
                elif ((user_input.lower() == "c") or (user_input.lower() == "n")):
                    print(self.getStatusString())
                    continue
                else:
                    print("------- Invalid input received.")
    
    # ask player which cards to keep out of possibleCards
    # returns array of Card IDs (not indices)
    def exchange(self, possibleCards):
        print("--- (" + self.name + ") Choose which cards to keep from the following:")
        chosenCards = []
        while (len(possibleCards) != 2):
            for i in range(len(possibleCards)):
                print("------ " + str(i) + ") " + GAMECARDS[possibleCards[i]])
            user_input = input()
            try:
                user_input = int(user_input)
                assert (user_input < len(possibleCards))
                assert (user_input >= 0)
                chosenCards.append(possibleCards.pop(user_input))

            except:
                print("------- Invalid input received.")
        return chosenCards



if __name__ == "__main__":
    player1 = CoupPlayer("Player 1");
    player1.cards[0] = 4
    player1.cards[1] = 2

    #action = player1.getAction()
    #print(action, actionToString[action])
    '''
    block = player1.getBlock(ACTION_ASS)
    print(block, GAMECARDS[block])

    block = player1.getBlock(ACTION_STL)
    print(block, GAMECARDS[block])

    block = player1.getBlock(ACTION_FOR)
    print(block, GAMECARDS[block])
    '''


