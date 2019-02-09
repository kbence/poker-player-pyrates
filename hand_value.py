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
