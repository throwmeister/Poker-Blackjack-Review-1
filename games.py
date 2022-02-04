from cardAndDeck import Deck
from threading import Thread
import pokerScoreCalculator as p_scoreCalc
import blackjackScoreCalculator as b_scoreCalc


class Game:
    # Game parent class shared by both poker and blackjack
    def __init__(self, player_type, num):
        self.threads = None
        self.players = []
        self.deck = Deck(num)
        self.pot = 0
        self.type = player_type
        self.players_scores = []

    def add_player(self, player_name, money):
        self.players.append(self.type(player_name, money))

    def bet(self):
        for this_player in self.players:
            print(f'You have {this_player.get_funds()} in your bank')
            bet = int(input(f'How much would you like to bet, {this_player.say_name()}? '))
            this_player.take_away(bet)
            self.pot += bet

    def deal_cards(self):
        if isinstance(self, Blackjack):
            num = 2
        else:
            num = 5
        for i in range(num):
            for player in self.players:
                card = self.deck.draw()
                player.hand.append(card)

    def calculate_winner(self):
        duple = 0
        # A counter for if there is more than one winner
        new = sorted(self.players_scores, key=lambda x: x[1], reverse=True)
        while True:
            # Logic to check for multiple winners
            try:
                if new[duple][1] == new[duple + 1][1]:
                    duple += 1
                else:
                    break
            except IndexError:
                break
        for i in range(duple + 1):
            # Calculates all the winners and gives them their money
            winner = new[i][0]
            print(f'{winner.say_name()} is the winner!')
            winner.add_money(self.pot / (duple + 1))

    def create_threads(self):
        self.threads = [Thread(target=x.calculate_player_score, args=(self.players_scores,)) for x in self.players]

    def run_thread(self, i):
        self.threads[i].start()

    def join_threads(self):
        for thread in self.threads:
            if thread.is_alive():
                thread.join()

    def calculate_scores(self):
        # Uses the calculated player scores to determine the winner
        scores = []
        for this_player in self.players:
            score = this_player.calculate_player_score()
            scores.append([this_player, score])
        return scores


class Poker(Game):
    # Poker child class
    def __init__(self, player_type):
        # Initialise the game
        super().__init__(player_type, 1)

    def remove_hands(self):
        # Handles the poker specific way of handling replacing cards
        # Also makes use of the Threading module to calculate the score while receiving inputs
        for i, this_player in enumerate(self.players):
            print(f'My name is {this_player.say_name()}')
            this_player.show_hand()
            choice = int(input(f'{this_player.say_name()}, would you like to replace 0, 1, 2 or 3 cards? '))
            if choice == 0:
                pass
            elif choice == 1 or 2 or 3:
                this_player.change_cards(choice, self.deck)
            else:
                pass
            self.run_thread(i)
        self.join_threads()


class Blackjack(Game):
    # Blackjack child class
    def __init__(self, player_type):
        super().__init__(player_type, 8)

    def add_to_hand(self):
        # Handles the blackjack specific way adding and removing cards
        # Also makes use of the Threading module to calculate the score while receiving inputs
        count = 0
        while count != len(self.players):
            for i, player in enumerate(self.players):
                if player.hold:
                    pass
                else:
                    print('Current hand:')
                    player.show_hand()
                    choice = input(f'''
{player.say_name()}, would you like to (d)raw or (h)old?
If you hold you will be locked out of replacing your hand                
''').upper()
                    if choice == 'D':
                        player.draw(self.deck)
                        player.show_drawn_card()
                        if player.calculate_player_score() == -1:
                            print('''You have gone bust!
                            ''')
                            player.hold = True
                            count += 1
                    elif choice == 'H':
                        player.hold = True
                        count += 1
                        self.run_thread(i)
                    else:
                        print('wrong input')
        self.join_threads()


class Player:
    def __init__(self, name, money):
        self.name = name
        self.hand = []
        self.money = money

    def take_away(self, bet):
        # Create bets for players
        while bet > self.money:
            bet = int(input("'You don't have enough funds"))
        self.money -= bet

    def draw(self, deck):
        self.hand.append(deck.draw())
        return self

    def start_thread(self):
        pass

    def show_hand(self):
        # print(list(map(lambda h: str(h), self.hand)))
        for c in self.hand:
            c.display()

    def say_name(self):
        return self.name

    def get_funds(self):
        return self.money

    def add_money(self, pot):
        # Adds the pot money to the winner
        self.money += pot

    def show_drawn_card(self):
        print(f'''{self.hand[-1]} had been drawn
''')

    def __str__(self):
        return self.hand


class BlackjackPlayer(Player):
    def __init__(self, name, money):
        super().__init__(name, money)
        self.hold = False

    def calculate_player_score(self, player_score=None):
        card_access = {
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'Jack': 10,
            'Queen': 10,
            'King': 10,
            'Ace': 11
        }
        hand = b_scoreCalc.list_of_hand(self.hand, card_access)
        score = b_scoreCalc.calculate(hand)
        if player_score is None:
            return score
        player_score.append([self, score])
        return player_score


class PokerPlayer(Player):
    def __init__(self, name, money):
        super().__init__(name, money)

    def change_cards(self, number, deck):
        # Change the cards of the player
        card_change = set()
        for i in range(number):
            card_change.add(int(input('Which card would you like to replace? (1/2/3/4/5): ')))
        for f in card_change:
            self.hand[f - 1] = deck.draw()
            print(f'{self.hand[f - 1]} is your new card')

    def calculate_player_score(self, player_score):
        # Calculates the score of all players

        card_access = {
            '3': 3,
            '2': 2,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'Jack': 11,
            'Queen': 12,
            'King': 13,
            'Ace': 14
        }
        cards = p_scoreCalc.list_of_values(self.hand, card_access)
        num_score = p_scoreCalc.value_calc(cards)
        if num_score == 0:
            flush = p_scoreCalc.suit_calc(self.hand)
            num_score = p_scoreCalc.straight_calc(cards, flush)
            if num_score == 0:
                num_score = p_scoreCalc.high_calc(cards)

        else:
            pass
        print(num_score)
        player_score.append([self, num_score])
        return player_score
