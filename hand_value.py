from itertools import combinations

from player import PlayerCard


def get_value(state):
    all_cards = []
    player = get_self(state['players'])

    all_cards.extend(player['hole_cards'])
    all_cards.extend(state['community_cards'])


def get_self(players):
    for player in players:
        if player['name'] == 'PyRates':
            return player


def get_pair_value(cards):
    chen_cards = [PlayerCard(card) for card in cards]

    highest_value = 0
    combos = combinations(chen_cards, 2)

    for c in combos:
        if c[0].rank == c[1].rank and c[0].chen_value > highest_value:
            highest_value = c[0].chen_value

    return highest_value


def get_two_pair_value(cards):
    chen_cards = set([PlayerCard(card) for card in cards])

    highest_value_r1 = 0
    matches_r1 = set()

    combos = combinations(chen_cards, 2)
    for c in combos:
        if c[0].rank == c[1].rank and c[0].chen_value > highest_value_r1:
            highest_value_r1 = c[0].chen_value
            matches_r1.add(c[0])
            matches_r1.add(c[1])
            break

    highest_value_r2 = 0
    chen_cards = chen_cards.difference(matches_r1)
    combos = combinations(chen_cards, 2)
    for c in combos:
        if c[0].rank == c[1].rank and c[0].chen_value > highest_value_r2:
            highest_value_r2 = c[0].chen_value

    return max(highest_value_r1, highest_value_r2) if highest_value_r2 else 0


def get_drill_value(cards):
    chen_cards = [PlayerCard(card) for card in cards]

    highest_value = 0
    combos = combinations(chen_cards, 3)

    for c in combos:
        if c[0].rank == c[1].rank and c[1].rank == c[2].rank and c[0].chen_value > highest_value:
            highest_value = c[0].chen_value

    return highest_value


def get_full_value(cards):
    chen_cards = set([PlayerCard(card) for card in cards])

    if len(chen_cards) < 5:
        return 0

    highest_value_r1 = 0
    matches_r1 = set()
    combos = combinations(chen_cards, 3)

    for c in combos:
        if c[0].rank == c[1].rank and c[1].rank == c[2].rank and c[0].chen_value > highest_value_r1:
            highest_value_r1 = c[0].chen_value
            matches_r1.add(c[0])
            matches_r1.add(c[1])
            matches_r1.add(c[2])
            break

    highest_value_r2 = 0
    chen_cards = chen_cards.difference(matches_r1)
    combos = combinations(chen_cards, 2)
    for c in combos:
        if c[0].rank == c[1].rank and c[0].chen_value > highest_value_r2:
            highest_value_r2 = c[0].chen_value

    # Use the value of the drill
    return highest_value_r1 if highest_value_r2 else 0
