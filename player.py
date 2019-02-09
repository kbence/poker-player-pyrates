import logging
import math
import operator

from hand_value import get_deck_value
from player_card import PlayerCard, RANKS

logging.basicConfig(level=logging.DEBUG)


class GameStateLogger(object):
    def __init__(self, game_state):
        self.game_state = game_state
        self.log = logging.getLogger(__name__)
        self.prefix = '{} '.format(game_state['game_id'])

    def info(self, msg, *args, **kwargs):
        self.log.info(self.prefix + msg.format(*args, **kwargs))


class Player:
    VERSION = "Special algorithm update2"

    def betRequest(self, game_state):
        self.log = GameStateLogger(game_state)

        current_buy_in = game_state['current_buy_in']
        player = game_state['players'][game_state['in_action']]
        dealer = game_state['dealer']
        minimum_raise = game_state['minimum_raise']

        c1 = PlayerCard(player['hole_cards'][0])
        c2 = PlayerCard(player['hole_cards'][1])

        chen_sum = 0
        high_card = sorted([c1, c2], key=operator.attrgetter('chen_value'), reverse=True)[0]

        chen_sum += high_card.chen_value

        if self.is_pair(c1, c2):
            chen_sum += high_card.chen_value * 2

        if self.is_suited(c1, c2):
            chen_sum += 2

        gap = self.calc_gap(c1, c2)
        chen_sum -= gap

        chen_sum += self.calc_extra_point(c1, c2, gap)

        chen_sum = math.ceil(chen_sum)

        # Starting hand calculation
        if len(game_state['community_cards']) == 0:
            self.log.info('This is a starter hand')
            when_to_raise = 9
            if len(game_state['players']) == 6:
                position = self.get_position(dealer, player['id'], len(game_state['players']))
                self.log.info('We are in position %s' % position )
                if 0 <= position <= 1:
                    when_to_raise = 9
                elif 2 <= position < 4:
                    when_to_raise = 8
                else:
                    when_to_raise = 7
                self.log.info('We are going to raise over Chen value {}', when_to_raise)
            else:
                self.log.info('We dont care about positions')

            if chen_sum >= when_to_raise:
                self.log.info('CHEN value of hand is %s, raising' % chen_sum)
                return min(int(player['stack'] * 0.3), current_buy_in - player['bet'] + minimum_raise)
            else:
                self.log.info('CHEN value of hand is %s, folding' % chen_sum)
                return 0

        return self.get_post_flop_decision(game_state)

    def get_post_flop_decision(self, game_state):
        minimum_raise = game_state['minimum_raise']

        value = get_deck_value(game_state)

        self.log.info('Deck value is estimated to: {}', value)

        if value > 0:
            max_raise = int(minimum_raise * (1 + value / 20))
            raise_value = max(minimum_raise, max_raise // 2)
            player = game_state['players'][game_state['in_action']]
            print(max_raise, raise_value)

            if raise_value < player['stack'] * 0.3:
                self.log.info('Raising by {}, max raise is {}', raise_value, max_raise)

                return game_state['current_buy_in'] - player['bet'] + raise_value
            else:
                self.log.info('Not putting more then 30% of our {} stack', player['stack'])
        else:
            self.log.info('We have nothing, let\'s fold')

        return 0

    def showdown(self, game_state):
        pass

    @staticmethod
    def get_position(dealer, player, numPlayers):
        if player <= dealer:
            return (numPlayers - dealer + player) % 6
        else:
            return player - dealer


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


