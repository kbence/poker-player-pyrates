
class Player:
    VERSION = "Default Python 3 folding player"

    def betRequest(self, game_state):
        current_buy_in = game_state['current_buy_in']
        player = game_state['players'][game_state['in_action']]
        minimum_raise = game_state['minimum_raise']

        if player['hole_cards'][0]['rank'] == player['hole_cards'][1]['rank']:
            return current_buy_in - player['bet'] + minimum_raise

        return 0

    def showdown(self, game_state):
        pass

