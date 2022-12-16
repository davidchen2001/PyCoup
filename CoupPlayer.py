from CoupActions import *

class CoupPlayer:

    def __init__(self, name):
        self.name = name
        self.coins = 2
        self.cards = [-2, -2]
        self.numCards = 2
        self.isAlive = True

    def die(self):
        self.isAlive = False

    def lose_card(self, lost):
        # replace the card with the "dead" card
        self.numCards -= 1
        if(lost==self.cards[0]):
            self.cards[0] = -2
        else:
            self.cards[1] = -2
        
        #check if player is alive
        if(self.numCards <= 0):
            self.die()

        return lost
    
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
                for i in range(1, len(actionToString)):
                    print("------ " + str(i) + " - " + actionToString[i])
                continue
            try:
                action = int(user_input)
                assert((action <= 7) and (action > 0))
                return action
            except:
                print("------- Invalid action input received.")
                    
                

if __name__ == "__main__":
    player1 = CoupPlayer("Player 1");
    action = player1.getAction()
    print(action, actionToString[action])
        




