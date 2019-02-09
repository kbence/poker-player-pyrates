import json
import os
import unittest

import hand_value
from tests.test_hand_value import to_deck


class MyTestCase(unittest.TestCase):

    def setUp(self):
        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures/game_state.json')
        with open(fixture_path, 'r') as f:
            self.game_state = json.loads(f.read())

    def test_deck_value(self):
        val = hand_value.get_deck_value(self.game_state)
        self.assertGreater(val, 0)

    def test_hand(self):
        val = hand_value.get_cards_value(to_deck([('A', 's'), ('J', 's'), ('10', 'c'), ('10', 'd'), ('4', 's')]))

        self.assertEquals(5, val)

if __name__ == '__main__':
    unittest.main()
