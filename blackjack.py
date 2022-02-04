import games as blackjack

if __name__ == '__main__':
    game = blackjack.Blackjack(blackjack.BlackjackPlayer)
    game.add_player('Bob', 100)
    game.add_player('Gary', 100)
    game.create_threads()
    game.bet()
    game.deal_cards()
    game.add_to_hand()
    game.calculate_winner()
