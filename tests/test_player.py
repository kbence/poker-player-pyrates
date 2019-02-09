import json
import os
import unittest

from mock import MagicMock

from player import Player
from tests.test_hand_value import to_deck


class TestPlayer(unittest.TestCase):
    def setUp(self):
        super(TestPlayer, self).setUp()
        self.player = Player()
        self.player.log = MagicMock()

        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures/game_state.json')
        with open(fixture_path, 'r') as f:
            self.game_state = json.loads(f.read())

    def create_game_state(self, **kwargs):
        return dict(
            minimum_raise=kwargs.get('minimum_raise', 10),
            in_action=0,
            players=[dict(
                dict(
                    name='PyRates',
                    stack=kwargs.get('stack', 1000),
                    bet=kwargs.get('bet', 25),
                    hole_cards=to_deck(kwargs.get('hole_cards', [('A', 'd'), ('2', 'c')])),
                )
            )],
            community_cards=[],
            current_buy_in=kwargs.get('buy_in', 25)
        )

    def test_responds_something(self):
        result = self.player.betRequest(self.game_state)
        print(result)

        self.assertIsInstance(result, int)

    def test_post_flop(self):
        cases = [
            (30, dict(bet=25, hole_cards=[('A', 's'), ('A', 'c')])),
            (1,  dict(bet=100, hole_cards=[('A', 's'), ('A', 'c')])),
        ]

        for expected, case in cases:
            result = self.player.get_post_flop_decision(self.create_game_state(**case))
            self.assertEqual(expected, result)
