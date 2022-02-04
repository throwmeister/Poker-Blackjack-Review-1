import random


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def display(self):
        print(f'{self.value} of {self.suit}')

    def return_card(self):
        return f'{self.value} of {self.suit}'

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value

    def __str__(self):
        return f'{self.value} of {self.suit}'


class Deck:
    def __init__(self, num, game_type=Card):
        self.cards = []
        self.game_type = game_type
        self.build(num)

    def build(self, num):
        # Create the deck
        for _ in range(num):
            for suit in ['Spades', 'Diamonds', 'Clubs', 'Hearts']:
                for j in range(2, 11):
                    self.cards.append(self.game_type(suit, j))
                for i in ['Jack', 'Queen', 'King', 'Ace']:
                    self.cards.append(self.game_type(suit, i))
        random.shuffle(self.cards)

    def display(self):
        # Displays each card individually
        for card in self.cards:
            card.display()

    def draw(self):
        # Draw cards from the deck
        return self.cards.pop()

    def show_card(self, val):
        # Shows a specific card value
        self.cards[val].display()
