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

    def takeTurn(self):
        player = self.alive[self.currentPlayer]
        possibleActions = player.getPossibleActions()

        if (ACTION_STL in possibleActions and self.noSteal()):
            possibleActions.remove(3)

        action = -1
        while (action < 0):
            action = self.getChosenAct(possibleActions, player)
            if action not in possibleActions:
                print("*** INVALID ACTION")
                action = -1

        target = self.getTarget(action)
        self.displayAction(action, target)
        # assass must spend
        if action == ACTION_ASS:
            player.coins -= 3
        if action == ACTION_COU:
            player.coins -= 7
        
        actionWentThrough = True
        # challenge
        challenger = self.challenge(action, player)
        if challenger:
            actionWentThrough = self.resolveChallenge(challenger, player, action)
            self.displayChallengeResults(challenger, player, action, actionWentThrough)

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

            print(player.getStatusString())
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
        handSize = player.numCards
        for card in player.cards:
            if card != -2:
                toChoose.append(card)
        toChoose.append(self.deck.draw())
        toChoose.append(self.deck.draw())
        newHand = player.exchange(toChoose)
        assert len(toChoose) == 2
        self.deck.add(toChoose[0], toChoose[1])
        assert (len(newHand) == handSize)
        player.cards = newHand

        # player mentioned so that x assassinated y could be displayed
    def assass(self, player, target):
        self.loseCard(target)

    # player mentioned so that x couped y could be displayed
    def coup(self, player, target):
        self.loseCard(target)    
        
    # getBlocker requires player input
    def getBlocker(self, action: int, target: CoupPlayer):
        # returns card, blocker
        # card is integer (-1 if no block) that blocker uses to block
        # blocker is a player object
        card = -1
        blocker = None

        if action == ACTION_ASS:
            # Ask target if they want to block with contessa (card 0)
            card = target.getBlock(action)
            if (card != -1):
                blocker = target 
            
        elif action == ACTION_STL:
            # Ask target if they want to block with captain (card 3) or ambassador (card 2)
            card = target.getBlock(action)
            if (card != -1):
                blocker = target 

        elif action == ACTION_FOR:
            # Give all players a chance to block with duke (card 4)
            for player in self.alive:
                if (player != self.alive[self.currentPlayer]):
                    card = player.getBlock(action)
                    if (card != -1):
                        blocker = player
                        break 

        return card, blocker

    # challenge method requires player input
    def challenge(self, action, target) -> CoupPlayer:
        if action > 4:
            # Universal actions
            return None

        ind = self.alive.index(target)
        # send this message to each player:
        for i in range(self.playerCount):
            if i != ind:
                numLeft = 3 - self.cardsRemoved[action]
                totalLeft = 15 - sum(self.cardsRemoved) - self.alive[i].numCards - target.numCards
                for card in self.alive[i].cards:
                    if card == action:
                        numLeft -= 1
                prob = round(1 - math.comb(totalLeft, numLeft) / math.comb(totalLeft + target.numCards, numLeft), 3)
                
                # tell alive[i]
                if (self.alive[i].getChallenge(target.name, action, prob) == True):
                    return self.alive[i]

        # Otherwise return None
        return None

    # after a player has indicated they want to challenge an action
    # returns True if player was truthful (action succeeds)
    # returns False if player was lying and the challenge was successful (action fails)
    def resolveChallenge(self, challenger, personChallenged, action) -> bool:
        if (action in personChallenged.cards):
            # action codes correspond with card codes
            # Ex) ACTN_STL = 3 = CARD_CAPT
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
    def getChosenAct(self, actions, player) -> int:
        # Ask player which action they want to take
        # Return an integer corresponding to the action
        return player.getAction(actions)


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
        output = self.alive[self.currentPlayer].name
        if(action > 4):
            # universal action
            output += " will "
        else:
            output += " wants to "
        output += actionToString[action]

        if (target is not None):
            output += ", target = "
            output += target.name

        print(output)

    def displayChallengeResults(self, challenger, personChallenged, card, actionWentThrough):
        output = challenger.name
        output += " challenged the "
        output += GAMECARDS[card]
        output += " of "
        output += personChallenged.name
        output += ". The challenge was "
        if (actionWentThrough):
            output += "unsuccessful!"
        else:
            output += "successful!"
        print(output)


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
    player0 = CoupPlayer("Player 0")
    player1 = CoupPlayer("Player 1")

    game.addPlayer(player0)
    game.addPlayer(player1)
    game.addPlayer("Player 2")
    game.addPlayer("Player 3")
    #game.addPlayer("Player 4")
    #game.addPlayer("Player 5")
    game.deal()
    while (game.playerCount > 0):
        game.takeTurn()

