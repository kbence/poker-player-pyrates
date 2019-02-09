import math


CARD_VAL_MAP = {'A': 10, 'K': 8, 'Q': 7, 'J': 6}
RANKS = ['A', 'K', 'Q', 'J'] + list(map(str, range(10, 1, -1)))


class PlayerCard:
    def __init__(self, card):
        self.rank = card['rank']
        self.suit = card['suit']
        self.index = RANKS.index(card['rank'])
        self.chen_value = int(math.ceil(CARD_VAL_MAP[self.rank] if self.rank in CARD_VAL_MAP else int(self.rank) / 2))

    def __str__(self):
        return '[{} {} {}]'.format(self.rank, self.suit, self.chen_value)

    def __lt__(self, other):
        return self.index>other.index