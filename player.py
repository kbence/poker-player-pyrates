import logging

CARD_VAL_MAP = {'A': 10, 'K': 8, 'Q': 7, 'J': 6}
RANKS = ['A', 'K', 'Q', 'J'] + list(map(str, range(10, 1, -1)))


logging.basicConfig(level=logging.DEBUG)


class PlayerCard:
    def __init__(self, card):
        self.rank = RANKS.index(card['rank'])
        self.suit = card['suit']

    def __str__(self):
        return '[{} {}]'.format(self.rank, self.suit)


class Player:
    VERSION = "Default Python 3 folding player"

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)

    def betRequest(self, game_state):

        current_buy_in = game_state['current_buy_in']
        player = game_state['players'][game_state['in_action']]
        minimum_raise = game_state['minimum_raise']

        c1 = PlayerCard(player['hole_cards'][0])
        c2 = PlayerCard(player['hole_cards'][1])

        if c1.rank + c2.rank >= 16:
            self.log.info('Minimum raise due to high cards: {} {}', c1, c2)
            return current_buy_in - player['bet'] + minimum_raise

        if self.is_pair(c1, c2):
            self.log.info('Minimum raise due to pair: {} {}', c1, c2)
            return current_buy_in - player['bet'] + minimum_raise * 2

        return 0

    def showdown(self, game_state):
        pass

    @staticmethod
    def is_pair(c1, c2):
        return c1.rank == c2.rank
