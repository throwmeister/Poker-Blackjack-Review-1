def list_of_values(deck, card_access):
    cards = []
    for card in deck:
        value = card_access[str(card.get_value())]
        cards.append(value)
    return cards


def value_calc(cards):
    # This function calculates whether the deck contains any sort of pair, three of a kind, full house or four of a kind
    single = []
    score = 0
    pair_values = []
    tri_val = 0
    pair = 0
    triple = 0

    set_cards = set(cards)
    for card in set_cards:
        num = cards.count(card)
        if num == 2:
            pair += 1
            pair_values.append(card)
        elif num == 3:
            triple = 1
            tri_val = card
        elif num == 4:
            score = 105 + card
            return score
        else:
            single.append(card)
    values = sorted(pair_values, reverse=True) + sorted(single, reverse=True)
    seq = geometric_sequence()
    if triple == 1:
        if pair == 1:
            score = 90 + (tri_val / 100)
        else:
            score = 45 + (tri_val / 100)
    elif pair == 1:
        score = 15
        for i in range(0, 4):
            score += values[i] / seq[i]
    elif pair == 2:
        score = 30
        for i in range(0, 3):
            score += values[i] / seq[i]

    return score


def geometric_sequence():
    return [1 * 100 ** (n - 1) for n in range(1, 5 + 1)]


def high_calc(cards):
    # This function calculates the value of the deck if there only contains high cards
    score = 0
    sorted_cards = sorted(cards, reverse=True)

    seq = geometric_sequence()
    for i in range(len(sorted_cards)):
        score += sorted_cards[i] / seq[i]
    return score


def straight_calc(cards, flush):
    # Calculates whether the deck contains a straight
    score = 0

    sorted_cards = sorted(cards)
    if sorted_cards[4] - sorted_cards[0] == 4 or (sorted_cards[4] == 14 and sorted_cards[3] == 5):
        if flush:
            score = 120 + sorted_cards[4]
        else:
            score = 60 + sorted_cards[4]
        return score

    elif flush:
        score = 75 + sorted_cards[4]

    else:
        pass
    return score


def suit_calc(hand):
    # Calculates a flush
    spades = 0
    hearts = 0
    clubs = 0
    diamonds = 0
    for card in hand:
        if 'Spades' in str(card):
            spades += 1
        elif 'Diamonds' in str(card):
            diamonds += 1
        elif 'Clubs' in str(card):
            clubs += 1
        else:
            hearts += 1

    if (hearts or diamonds or spades or clubs) == 5:
        return True
    else:
        return False
