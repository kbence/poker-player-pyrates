
class Player:
    VERSION = "Default Python 3 folding player"

    def betRequest(self, game_state):
        current_buy_in = game_state['current_buy_in']
        player = game_state['players'][game_state['in_action']]
        minimum_raise = game_state['minimum_raise']

        c1_card = player['hole_cards'][0]
        c2_card = player['hole_cards'][1]

        card_val_map = {
            'A' : 10,
            'K' : 8,
            'Q' : 7,
            'J' : 6
        }
        ranks = ['A', 'K', 'Q', 'J'] + list(map(str, range(10, 1, -1)))

        c1_rank = ranks.index(c1_card['rank'])
        c2_rank = ranks.index(c2_card['rank'])

        if c1_rank + c2_rank >= 18:
            return current_buy_in - player['bet'] + minimum_raise

        if player['hole_cards'][0]['rank'] == player['hole_cards'][1]['rank']:
            return current_buy_in - player['bet'] + minimum_raise * 2

        return 0

    def showdown(self, game_state):
        pass

    @staticmethod
    def is_pair(c1, c2):
        return c1['rank'] == c2['rank']
