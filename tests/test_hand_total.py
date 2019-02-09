import json
import os
import unittest

import hand_value
from hand_value import HandType
from tests.test_hand_value import to_deck


TEST_SCALE_CONFIG = {
    HandType.PAIR: {'min': 0, 'max': 10},
    HandType.TWO_PAIRS : {'min': 20, 'max': 40},
    HandType.DRILL: {'min': 100, 'max': 150},
    HandType.ROW: {'min': 300, 'max': 400},
    HandType.FLUSH: {'min': 500, 'max': 600},
    HandType.FULL_HOUSE: {'min': 900, 'max': 1000}
}


class MyTestCase(unittest.TestCase):

    def setUp(self):
        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures/game_state.json')
        with open(fixture_path, 'r') as f:
            self.game_state = json.loads(f.read())

    def test_deck_value(self):
        val = hand_value.get_deck_value(self.game_state)
        self.assertGreater(val, 0)

    def test_hand_pair(self):
        val = hand_value.get_cards_value(to_deck([('A', 's'), ('J', 's'), ('10', 'c'), ('10', 'd'), ('4', 's')]), scale_config=TEST_SCALE_CONFIG)
        self.assertEquals(5, val)

    def test_hand_drill(self):
        val = hand_value.get_cards_value(to_deck([('A', 's'), ('J', 's'), ('10', 'c'), ('10', 'd'), ('10', 's')]), scale_config=TEST_SCALE_CONFIG)
        self.assertEquals(125, val)

if __name__ == '__main__':
    unittest.main()
