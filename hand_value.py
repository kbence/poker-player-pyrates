
def get_value(state):
    all_cards = []
    player = get_self(state['players'])


    all_cards.extend(player['hole_cards'])
    all_cards.extend(state['community_cards'])
    print(all_cards)


def get_self(players):
    for player in players:
        if player['name'] == 'PyRates':
            return player

def get_pair_value(cards):
    """Value between 0.0 and 1.0"""
    pass
