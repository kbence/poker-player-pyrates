import logging
import math
import operator

CARD_VAL_MAP = {'A': 10, 'K': 8, 'Q': 7, 'J': 6}
RANKS = ['A', 'K', 'Q', 'J'] + list(map(str, range(10, 1, -1)))


logging.basicConfig(level=logging.DEBUG)


class PlayerCard:
    def __init__(self, card):
        self.rank = card['rank']
        self.suit = card['suit']
        self.index = RANKS.index(card['rank'])
        self.chen_value = int( CARD_VAL_MAP[self.rank] if self.rank in CARD_VAL_MAP else int(self.rank) / 2)

    def __str__(self):
        return '[{} {} {}]'.format(self.rank, self.suit, self.chen_value)


class Player:
    VERSION = "super-duper python3 version"

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)

    def betRequest(self, game_state):

        current_buy_in = game_state['current_buy_in']
        player = game_state['players'][game_state['in_action']]
        minimum_raise = game_state['minimum_raise']

        c1 = PlayerCard(player['hole_cards'][0])
        c2 = PlayerCard(player['hole_cards'][1])

        chen_sum = 0
        high_card = sorted([c1, c2], key=operator.attrgetter('chen_value'), reverse=True)[0]

        chen_sum += high_card.chen_value
        self.log.info(chen_sum)

        if self.is_pair(c1, c2):
            chen_sum += high_card.chen_value * 2
            self.log.info(chen_sum)

        if self.is_suited(c1, c2):
            chen_sum += 2
            self.log.info(chen_sum)

        gap = self.calc_gap(c1, c2)
        self.log.info(gap)
        chen_sum -= gap

        chen_sum += self.calc_extra_point(c1, c2, gap)

        chen_sum = math.ceil(chen_sum)

        # Starting hand calculation
        if len(game_state['community_cards']) == 0:
            self.log.info('CHEN')
            if chen_sum >= 9:
                return min(int(player['stack'] * 0.3), current_buy_in - player['bet'] + minimum_raise)
            else:
                return 0

        # Not a starting hand
        if self.is_pair(c1, c2):
            self.log.info('Minimum raise due to pair: {} {}', c1, c2)
            return min(int(player['stack'] * 0.3), current_buy_in - player['bet'] + minimum_raise)

        return 0

    def showdown(self, game_state):
        pass



    @staticmethod
    def is_pair(c1, c2):
        return c1.rank == c2.rank

    @staticmethod
    def is_suited(c1, c2):
        return c1.suit == c2.suit

    @staticmethod
    def calc_gap(c1, c2):
        return min(4, abs(c1.index - c2.index))

    @staticmethod
    def calc_extra_point(c1, c2, gap):
        if gap <= 1 and c1.index > RANKS.index('Q') and c2.index > RANKS.index('Q'):
            return 1
        return 0
