from CoupActions import *
from CoupDeck import GAMECARDS, CARD_AMBR, CARD_ASSN, CARD_CAPT, CARD_CONT, CARD_DUKE

class CoupPlayer:

    def __init__(self, name):
        self.name = name
        self.coins = 2
        self.cards = [-2, -2]
        self.numCards = 2
        self.isAlive = True

    def die(self):
        self.isAlive = False

    def chooseLostCard(self):
        return self.cards[0]
        # TODO: replace the card with the "dead" card ###

    def lose_card(self):
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
    
    def getHandString(self):
        if ((self.isAlive == False) or (self.numCards == 0)):
            return "No cards"
        else:
            output = []
            for i in range(self.numCards):
                if (self.cards[i] >= 0):
                    output.append(GAMECARDS[self.cards[i]])
            return str(output)

    def getPossibleActions(self):
        if self.coins < 3:
            return([0, 2, 3, 5, 6])
        elif self.coins < 7:
            return([0, 1, 2, 3, 5, 6])
        elif self.coins < 10:
            return([0, 1, 2, 3, 5, 6, 7])
        else:
            return([7])

    def getAction(self) -> int:
        #how will we ensure player knows game state?
        
        while(True):
            user_input = input("--- Which action to play? ")
            if (user_input.lower() == "h") or (user_input.lower() == "help"):
                print("------ Type H for help, C for my cards and coins")
                for i in range(1, len(actionToString)):
                    print("------ " + str(i) + " - " + actionToString[i])
                continue
            elif (user_input.lower() == "c") or ("coin" in user_input.lower()) or ("card" in user_input.lower()):
                output = "------ Current hand: "
                output += self.getHandString()
                output += " and "
                output += str(self.coins)
                output += " coins"
                print(output)
                continue

            try:
                action = int(user_input)
                assert((action <= 7) and (action > 0))
                return action
            except:
                print("------- Invalid action input received.")

    # for actions with a target, return player # to target
    def getTarget(self, possibleTargets) -> int:
        #how will we ensure player knows game state?
        
        while(True):
            user_input = input("--- Who would you like to target? ")
            try:
                action = int(user_input)
                assert action in possibleTargets
                return action
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

        for card in possibleBlocks:
            prompt += "------ Type " + str(card) + " to block with " + GAMECARDS[card] + "\n"

        while(True):
            user_input = input(prompt)
            try:
                if (user_input.lower() == "n"):
                    user_input = -1
                else:
                    user_input = int(user_input)
                assert (user_input in possibleBlocks) or (user_input == -1)
                break
            except:
                print("------- Invalid input received.")

        return user_input     

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


