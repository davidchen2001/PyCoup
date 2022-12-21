import random

GAMECARDS = ["Contessa", "Assassin", "Ambassador", "Captain", "Duke"]
CARD_CONT = 0
CARD_ASSN = 1
CARD_AMBR = 2
CARD_CAPT = 3
CARD_DUKE = 4

class CoupDeck:
    def __init__(self):
        self.deck = [0,1,2,3,4]*3
        random.shuffle(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self):
        assert len(self.deck) > 0
        return self.deck.pop()

    def add(self, card1, card2 = -1):
        self.deck.append(card1)
        if card2 >= -1:
            self.deck.append(card2)
        self.shuffle()