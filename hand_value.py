from itertools import combinations

from player_card import PlayerCard

# scale within the same type eg. one pair
SAME_TYPE_SCALE = 10

class HandType():
    PAIR='pair'
    TWO_PAIRS='two_pairs'
    DRILL='drill'
    ROW='row'
    FLUSH = 'flush'
    FULL_HOUSE='full_house'
    POKER='poker'
    # TODO: STRAIGHT_FULSH, ROYAL_FLUSH


DEFAULT_SCALE_CONFIG = {
    HandType.PAIR: {'min': 0, 'max': 10},
    HandType.TWO_PAIRS : {'min': 20, 'max': 40},
    HandType.DRILL: {'min': 100, 'max': 150},
    HandType.ROW: {'min': 300, 'max': 400},
    HandType.FLUSH: {'min': 500, 'max': 600},
    HandType.FULL_HOUSE: {'min': 900, 'max': 1000},
    HandType.POKER: {'min': 1100, 'max': 1200}
}


def get_deck_value(game_state):

    player = get_self(game_state['players'])
    hand_cards = player['hole_cards']

    table_cards = game_state['community_cards']

    return get_cards_value(hand_cards=hand_cards, table_cards=table_cards)


def get_cards(game_state):
    all_cards = []
    player = get_self(game_state['players'])

    all_cards.extend(player['hole_cards'])
    all_cards.extend(game_state['community_cards'])
    return all_cards


def get_cards_value(cards=None, scale_config=DEFAULT_SCALE_CONFIG, hand_cards=None, table_cards=None):

    if not cards:
        cards = list(hand_cards)
        cards.extend(table_cards)
    if not table_cards:
        table_cards = []
    if not hand_cards:
        hand_cards = cards

    # Values by hand type
    all_values = []

    val = scale_hand_value(scale_config, HandType.PAIR, get_pair_value_with_own_hand(hand_cards, table_cards))
    all_values.append(val)

    val = scale_hand_value(scale_config, HandType.TWO_PAIRS, get_two_pair_value(cards))
    all_values.append(val)

    val = scale_hand_value(scale_config, HandType.DRILL, get_drill_value_with_own_hand(hand_cards, table_cards))
    all_values.append(val)

    val = scale_hand_value(scale_config, HandType.FLUSH, get_flush_value_with_own_hand(hand_cards, table_cards))
    all_values.append(val)

    val = scale_hand_value(scale_config, HandType.FULL_HOUSE, get_full_value(cards))
    all_values.append(val)

    val = scale_hand_value(scale_config, HandType.POKER, get_poker_value(cards))
    all_values.append(val)

    return int(max(all_values))

def scale_hand_value(config, hand_type, value):
    value = int(value) # just to make sure
    # We don't have this hand type
    if value == 0:
        return 0
    type_config = config[hand_type]
    diff = type_config['max'] - type_config['min']
    normalized_value = float(value) / SAME_TYPE_SCALE
    return type_config['min'] + diff * normalized_value


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


def get_pair_value_with_own_hand(hand_cards, table_cards):
    chen_hand_cards = set([PlayerCard(card) for card in hand_cards])
    chen_table_cards = set([PlayerCard(card) for card in table_cards])

    chen_cards = chen_hand_cards.union(chen_table_cards)

    highest_value = 0
    combos = combinations(chen_cards, 2)

    for c in combos:
        if c[0].rank == c[1].rank and c[0].chen_value > highest_value \
                and (c[0] in chen_hand_cards or c[1] in chen_hand_cards ):
            highest_value = c[0].chen_value

    return highest_value


def get_two_pair_value(cards):
    if len(cards) < 4:
        return 0

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
    if len(cards) < 3:
        return 0

    chen_cards = [PlayerCard(card) for card in cards]

    highest_value = 0
    combos = combinations(chen_cards, 3)

    for c in combos:
        if c[0].rank == c[1].rank and c[1].rank == c[2].rank and c[0].chen_value > highest_value:
            highest_value = c[0].chen_value

    return highest_value


def get_drill_value_with_own_hand(hand_cards, table_cards):
    chen_hand_cards = set([PlayerCard(card) for card in hand_cards])
    chen_table_cards = set([PlayerCard(card) for card in table_cards])

    chen_cards = chen_hand_cards.union(chen_table_cards)

    if len(chen_cards) < 3:
        return 0

    highest_value = 0
    combos = combinations(chen_cards, 3)

    for c in combos:
        if c[0].rank == c[1].rank and c[1].rank == c[2].rank and  c[0].chen_value > highest_value \
                and (c[0] in chen_hand_cards or c[1] in chen_hand_cards or c[2] in chen_hand_cards):
            highest_value = c[0].chen_value

    return highest_value


def get_full_value(cards):
    if len(cards) < 5:
        return 0

    chen_cards = set([PlayerCard(card) for card in cards])

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


def get_flush_value_with_own_hand(hand_cards, table_cards):
    l_chen_hand_cards = [PlayerCard(card) for card in hand_cards]
    l_chen_table_cards = [PlayerCard(card) for card in table_cards]

    chen_hand_cards = set(l_chen_hand_cards)
    chen_table_cards = set(l_chen_table_cards)

    chen_cards = chen_hand_cards.union(chen_table_cards)

    if len(chen_cards) < 5:
        return 0

    if l_chen_hand_cards[0].suit == l_chen_hand_cards[1].suit:
        same = 0
        highest = max(l_chen_hand_cards[0].chen_value, l_chen_hand_cards[1].chen_value)

        for c in l_chen_table_cards:
            if c.suit == l_chen_hand_cards[0].suit:
                same += 1
                highest = max(highest, c.chen_value)

        if same >= 3:
            return highest
    else:
        for s in l_chen_hand_cards:
            same = 0
            highest = s.chen_value

            for c in l_chen_table_cards:
                if c.suit == s.suit:
                    same += 1
                    highest = max(highest, c.chen_value)

            if same >= 4:
                return highest

    return 0


def get_poker_value(cards):
    if len(cards) < 4:
        return 0

    chen_cards = [PlayerCard(card) for card in cards]

    highest_value = 0
    combos = combinations(chen_cards, 4)

    for c in combos:
        if c[0].rank == c[1].rank \
                and c[1].rank == c[2].rank \
                and c[2].rank == c[3].rank \
                and c[0].chen_value > highest_value:
            highest_value = c[0].chen_value

    return highest_value


def get_row_value(cards):
    if len(cards)<5:
        return 0

    chen_cards = [PlayerCard(card) for card in cards]

    for i in range(len(chen_cards)):
        playing_cards.append(i)
        playing_cards_set.add(i)

    counter=0

    playing_cards.sort(reverese=True)


    if(len(playing_cards)>=5):
        for i in range(len(playing_cards)-1):
            if(playing_cards[i].index-playing_cards[i+1].index)==1:
                counter+=1
                if counter==5 :
                    return playing_cards[i-3].chen_value
            else:
                counter=0
        return 0
    else:
        return 0
