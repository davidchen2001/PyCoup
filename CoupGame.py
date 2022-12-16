from turtle import pos
from CoupActions import *
from CoupDeck import *
from CoupPlayer import CoupPlayer
import math

class CoupGame:
    ''' 
    ACTIONS:
    1: Assassinate
    2: Exchange
    3: Steal
    4: Tax
    5: Income
    6: Foreign Aid
    7: Coup
    '''

    def __init__(self):
        self.playerCount = 0
        self.currentPlayer = 0
        # Lists of names
        self.alive = []
        self.dead = []
        self.cardsRemoved = [0,0,0,0,0]
        self.deck = CoupDeck()

    def addPlayer(self, player):
        if(self.playerCount >= 6):
            return

        if isinstance(player, str):
            # if we need to create a player with the supplied name
            self.alive.append(CoupPlayer(player))

        elif isinstance(player, CoupPlayer):
            # if the player is already created and we just need to add it
            self.alive.append(player)

        else:
            return
        
        self.playerCount += 1

    def deal(self):
        for i in range(self.playerCount):
            self.alive[i].cards[0] = self.deck.draw()
            self.alive[i].cards[1] = self.deck.draw()

    def takeTurn(self, action):
        player = self.alive[self.currentPlayer]
        possibleActions = player.getPossibleActions()

        if action not in possibleActions:
            return False

        if (ACTION_STL in possibleActions and self.noSteal()):
            possibleActions.remove(3)
        action = self.getChosenAct(possibleActions, player)
        target = self.getTarget(action)
        self.displayAction(action, target)
        # assass must spend
        if action == ACTION_ASS:
            player.coins -= 3
        if action == ACTION_COU:
            player.coins -= 7

        # challenge
        challenger = self.challenge(action, player)
        if challenger:
            actionWentThrough = self.resolveChallenge(challenger, player, action)

        # block
        if actionWentThrough:
            card, blocker = self.getBlocker(action, target)
            if card != -1:
                actionWentThrough = False
                # challenge block
                challenger = self.challenge(card, blocker)
                if challenger:
                    actionWentThrough = not self.resolveChallenge(challenger, blocker, card)

        # execute
        if actionWentThrough:

            if action == ACTION_ASS:
                self.assass(player, target)
            elif action == ACTION_EXC:
                self.exchange(player)
            elif action == ACTION_STL:
                self.steal(player, target)
            elif action == ACTION_TAX:
                self.tax(player)
            elif action == ACTION_INC:
                self.income(player)
            elif action == ACTION_FOR:
                self.foreignAid(player)
            else:
                self.coup(player, target)

        self.currentPlayer += 1
        self.currentPlayer %= self.playerCount
        return True

    def tax(self, player):
        player.coins += 3

    def income(self, player):
        player.coins += 1

    def foreignAid(self, player):
        player.coins += 2

    def steal(self, player, target):
        player.coins += min(2, target.coins)
        target.coins -= min(2, target.coins)

    def exchange(self, player):
        newHand = []
        toChoose = []
        for card in player.cards:
            if card == -2:
                newHand.append(card)
            else:
                toChoose.append(card)
        toChoose.append(self.deck.draw())
        toChoose.append(self.deck.draw())
        # Ask player which of the cards in toChoose they want
        # Choose 2 - len(newHand) of them
        # newHand.append(choice) for each choice
        player.cards = newHand

        # player mentioned so that x assassinated y could be displayed
    def assass(self, player, target):
        self.loseCard(target)

    # player mentioned so that x couped y could be displayed
    def coup(self, player, target):
        self.loseCard(target)    
        

    # getBlocker requires player input
    def getBlocker(action, target):
        # returns card, blocker
        # card is integer
        # blocker is a player object
        if action == ACTION_ASS:
            # Ask target if they want to block with contessa (card 4)
            pass
        elif action == ACTION_STL:
            # Give all players a chance to block with captain (card 3) or ambassador (card 2)
            pass
        elif action == ACTION_FOR:
            # Give all players a chance to block with duke (card 0)
            pass

        return -1, None

    # challenge method requires player input
    def challenge(self, action, target):
        if action > 4:
            # Universal actions
            return None
        ind = self.alive.index(target)
        # Start timer
        # send this message to each player:
        for i in range(self.playerCount):
            if i != ind:
                numLeft = 3 - self.cardsRemoved[action]
                totalLeft = 15 - sum(self.cardsRemoved) - self.alive[i].numCards - target.numCards
                for card in self.alive[i]:
                    if card == action:
                        numLeft -= 1
                prob = 1 - math.comb(totalLeft, numLeft) / math.comb(totalLeft + target.numCards, numLeft)
                # tell alive[i]
                pass
        # If someone clicks challenge in that time, that player object
        # Otherwise return None
        return None

    def resolveChallenge(self, challenger, personChallenged, action):
        if (action in personChallenged.cards):
            personChallenged.cards.remove(action)
            self.deck.add(action)
            personChallenged.cards.append(self.deck.draw())

            self.loseCard(challenger)
            return True
        else:
            self.loseCard(personChallenged)
            return False

    def loseCard(self, player):
        lostCard = player.lose_card()
        self.cardsRemoved[lostCard] += 1
        if not player.isAlive:
            self.playerCount -= 1
            ind = self.alive.index(player)
            self.dead.append(self.alive.pop(ind))
            if ind <= self.currentPlayer:
                # to offset adding 1
                self.currentPlayer -= 1

    # return true if you CAN'T steal at all
    def noSteal(self):
        for i in range(self.playerCount):
            if (i != self.currentPlayer and self.alive[i].coins > 0):
                return False
        return True

    # getChosenAct requires player input
    def getChosenAct(actions, player) -> int:
        # Ask player which action they want to take
        # Return an integer corresponding to the action
        return player.getAction()


    # returns a player object
    def getTarget(self, action) -> CoupPlayer:
        if action == ACTION_ASS or action == ACTION_COU:
            return self.askForTarget()
        if action == ACTION_STL:
            return self.askForTarget(True)
        return None

    def displayTargets(self, listOfPlayers):
        print("------- Possible targets: ")
        for i in range(len(listOfPlayers)):
            print("------- " + str(listOfPlayers[i]) + " - " + self.alive[listOfPlayers[i]].name)

    def displayAction(self, action, target):
        pass

    # returns a player object, requires input
    def askForTarget(self, steal = False) -> CoupPlayer:
        possibleTargets = []
        for i in range(self.playerCount):
            if (i != self.currentPlayer) and (not steal or self.alive[i].coins > 0):
                possibleTargets.append(i)
        self.displayTargets(possibleTargets)

        user_input = self.alive[self.currentPlayer].getTarget(possibleTargets)
        return self.alive[user_input]

if __name__ == "__main__":
    game = CoupGame();
    player0 = CoupPlayer("Player 0");
    game.addPlayer(player0)
    game.addPlayer("Player 1")
    game.addPlayer("Player 2")
    game.addPlayer("Player 3")
    game.addPlayer("Player 4")
    game.addPlayer("Player 5")
    game.deal()
    #for player in game.alive:
        #print(player.cards)
        
    #target = game.askForTarget()
    #print(target, game.alive[target].name)


            


