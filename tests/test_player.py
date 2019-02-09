import json
import os
import unittest

from player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        super(TestPlayer, self).setUp()
        self.player = Player()

        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures/game_state.json')
        with open(fixture_path, 'r') as f:
            self.game_state = json.loads(f.read())

    def test_responds_something(self):
        result = self.player.betRequest(self.game_state)

        self.assertIsInstance(result, int)
