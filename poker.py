import games as poker


if __name__ == '__main__':
    # player_num = 4
    # int(input('How many players?: '))
    game = poker.Poker(poker.PokerPlayer)

    game.add_player('Bob', 100)
    game.add_player('Gary', 100)
    game.create_threads()
    game.bet()
    game.deal_cards()
    game.remove_hands()
    game.bet()
    game.calculate_winner()
