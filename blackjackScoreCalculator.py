def list_of_hand(hand, card_access):
    cards = []
    for card in hand:
        value = card_access[str(card.get_value())]
        cards.append(value)
    return cards


def calculate(hand):
    score = 0
    score = sum(hand)

    if score > 21:
        if 11 in hand:
            score -= 10
            hand.remove(11)
            calculate(hand)
        else:
            return -1
    else:
        return score
