import unittest

import hand_value

SUITES = {'s': 'spades', 'h': 'hearts', 'c': 'clubs', 'd': 'diamonds'}


class MyTestCase(unittest.TestCase):
    def test_pair_nothing(self):
        deck = to_deck([('A', 's'), ('J', 's'), ('9', 'c'), ('10', 'd'), ('4', 's')])
        value = hand_value.get_pair_value(deck)
        self.assertEqual(value, 0)

    def test_pair_tens(self):
        deck = to_deck([('A', 's'), ('J', 's'), ('10', 'c'), ('10', 'd'), ('4', 's')])
        value = hand_value.get_pair_value(deck)
        self.assertEqual(value, 5)

    def test_pair_aces(self):
        deck = to_deck([('A', 's'), ('J', 's'), ('A', 'c'), ('10', 'd'), ('4', 's')])
        value = hand_value.get_pair_value(deck)
        self.assertEqual(value, 10)

    def test_2_pair_nothing(self):
        deck = to_deck([('A', 's'), ('J', 's'), ('9', 'c'), ('10', 'd'), ('4', 's')])
        value = hand_value.get_two_pair_value(deck)
        self.assertEqual(value, 0)

    def test_2_pair_nothing_2(self):
        deck = to_deck([('A', 's'), ('J', 's'), ('A', 'c'), ('10', 'd'), ('4', 's')])
        value = hand_value.get_two_pair_value(deck)
        self.assertEqual(value, 0)

    def test_2_pair_aces(self):
        deck = to_deck([('A', 's'), ('A', 'd'), ('2', 'c'), ('2', 'h'), ('4', 's')])
        value = hand_value.get_two_pair_value(deck)
        self.assertEqual(value, 10)

    def test_2_pair_eights(self):
        deck = to_deck([('4', 's'), ('4', 'd'), ('8', 'c'), ('A', 'h'), ('8', 'h')])
        value = hand_value.get_two_pair_value(deck)
        self.assertEqual(value, 4)

    def test_2_pair_threes(self):
        deck = to_deck([('2', 's'), ('2', 'd'), ('3', 'c'), ('A', 'h'), ('3', 'h')])
        value = hand_value.get_two_pair_value(deck)
        self.assertEqual(value, 1)

    def test_drill_nothing(self):
        deck = to_deck([('2', 's'), ('2', 'd'), ('3', 'c')])
        value = hand_value.get_drill_value(deck)
        self.assertEqual(value, 0)

    def test_drill_simple(self):
        deck = to_deck([('2', 's'), ('2', 'd'), ('2', 'c')])
        value = hand_value.get_drill_value(deck)
        self.assertEqual(value, 1)

    def test_drill_queens(self):
        deck = to_deck([('Q', 's'), ('Q', 'd'), ('2', 'c'), ('Q', 's')])
        value = hand_value.get_drill_value(deck)
        self.assertEqual(value, 7)

    def test_drill_aces(self):
        deck = to_deck([('2', 's'), ('A', 'd'), ('3', 'c'), ('A', 'h'), ('A', 'h')])
        value = hand_value.get_drill_value(deck)
        self.assertEqual(value, 10)

    def test_drill_fives(self):
        deck = to_deck([('5', 's'), ('2', 'd'), ('5', 'c'), ('A', 'h'), ('5', 'h')])
        value = hand_value.get_drill_value(deck)
        self.assertEqual(value, 2)

    def test_full_not_enough_cards(self):
        deck = to_deck([('5', 's'), ('2', 'd'), ('5', 'c'), ('A', 'h')])
        value = hand_value.get_full_value(deck)
        self.assertEqual(value, 0)

    def test_full_nothing(self):
        deck = to_deck([('5', 's'), ('2', 'd'), ('5', 'c'), ('A', 'h'), ('A', 's')])
        value = hand_value.get_full_value(deck)
        self.assertEqual(value, 0)

    def test_full_fives(self):
        deck = to_deck([('5', 's'), ('5', 'd'), ('5', 'c'), ('2', 'h'), ('2', 's')])
        value = hand_value.get_full_value(deck)
        self.assertEqual(value, 2)

    def test_full_aces(self):
        deck = to_deck([('5', 's'), ('A', 'd'), ('5', 'c'), ('A', 'h'), ('A', 's')])
        value = hand_value.get_full_value(deck)
        self.assertEqual(value, 10)

    def test_poker_not_enough_cards(self):
        deck = to_deck([('5', 's'), ('A', 'd')])
        value = hand_value.get_poker_value(deck)
        self.assertEqual(value, 0)

    def test_poker_nothing(self):
        deck = to_deck([('5', 's'), ('A', 'd'), ('5', 'c'), ('A', 'h'), ('A', 's')])
        value = hand_value.get_poker_value(deck)
        self.assertEqual(value, 0)

    def test_poker_twos(self):
        deck = to_deck([('2', 's'), ('2', 'd'), ('5', 'c'), ('2', 'h'), ('2', 'h')])
        value = hand_value.get_poker_value(deck)
        self.assertEqual(value, 1)

    def test_poker_fives(self):
        deck = to_deck([('5', 's'), ('5', 'd'), ('5', 'c'), ('2', 'h'), ('5', 'h')])
        value = hand_value.get_poker_value(deck)
        self.assertEqual(value, 2)

    def test_poker_kings(self):
        deck = to_deck([('K', 's'), ('5', 'd'), ('K', 'c'), ('K', 'h'), ('K', 'd')])
        value = hand_value.get_poker_value(deck)
        self.assertEqual(value, 8)

    def test_poker_j(self):
        deck = to_deck([('K', 's'), ('J', 's'), ('J', 'c'), ('J', 'h'), ('J', 'd')])
        value = hand_value.get_poker_value(deck)
        self.assertEqual(value, 6)

    def test_get_pair_value_with_own_hand_nothing(self):
        own = to_deck([('K', 's'), ('J', 's')])
        table = to_deck([('A', 'c'), ('2', 'h'), ('5', 'd')])

        value = hand_value.get_pair_value_with_own_hand(own, table)
        self.assertEqual(value, 0)

    def test_get_pair_value_with_own_hand_twos(self):
        own = to_deck([('K', 's'), ('2', 's')])
        table = to_deck([('A', 'c'), ('2', 'h'), ('5', 'd')])

        value = hand_value.get_pair_value_with_own_hand(own, table)
        self.assertEqual(value, 1)

    def test_get_pair_value_with_own_hand_aces(self):
        own = to_deck([('A', 's'), ('2', 's')])
        table = to_deck([('A', 'c'), ('2', 'h'), ('5', 'd')])

        value = hand_value.get_pair_value_with_own_hand(own, table)
        self.assertEqual(value, 10)

    def test_get_pair_value_with_own_hand_j(self):
        own = to_deck([('A', 's'), ('J', 's')])
        table = to_deck([('J', 'c'), ('2', 'h'), ('5', 'd')])

        value = hand_value.get_pair_value_with_own_hand(own, table)
        self.assertEqual(value, 6)

    def test_get_drill_value_with_own_hand_not_enough_cards(self):
        own = to_deck([('K', 's'), ('J', 's')])
        table = to_deck([])

        value = hand_value.get_drill_value_with_own_hand(own, table)
        self.assertEqual(value, 0)

    def test_get_drill_value_with_own_hand_nothing(self):
        own = to_deck([('K', 's'), ('J', 's')])
        table = to_deck([('A', 'c'), ('2', 'h'), ('5', 'd')])

        value = hand_value.get_drill_value_with_own_hand(own, table)
        self.assertEqual(value, 0)

    def test_get_drill_value_with_own_hand_nothing_tricky(self):
        own = to_deck([('K', 's'), ('J', 's')])
        table = to_deck([('A', 'c'), ('A', 'h'), ('A', 'd')])

        value = hand_value.get_drill_value_with_own_hand(own, table)
        self.assertEqual(value, 0)

    def test_get_drill_value_with_own_hand_twos(self):
        own = to_deck([('2', 's'), ('2', 's')])
        table = to_deck([('A', 'c'), ('2', 'h'), ('5', 'd')])

        value = hand_value.get_drill_value_with_own_hand(own, table)
        self.assertEqual(value, 1)

    def test_get_drill_value_with_own_hand_aces(self):
        own = to_deck([('A', 's'), ('2', 's')])
        table = to_deck([('A', 'c'), ('2', 'h'), ('A', 'd')])

        value = hand_value.get_drill_value_with_own_hand(own, table)
        self.assertEqual(value, 10)

    def test_get_drill_value_with_own_hand_j(self):
        own = to_deck([('A', 's'), ('J', 's')])
        table = to_deck([('J', 'c'), ('2', 'h'), ('J', 'd')])

        value = hand_value.get_drill_value_with_own_hand(own, table)
        self.assertEqual(value, 6)


def to_card(rank, s):
    suite = SUITES[s]
    return {'rank': rank, 'suit': suite}


def to_deck(cards):
    return [to_card(c[0], c[1]) for c in cards]


if __name__ == '__main__':
    unittest.main()


test_state = {
    "tournament_id":"550d1d68cd7bd10003000003",     # Id of the current tournament
    "game_id":"550da1cb2d909006e90004b1",           # Id of the current sit'n'go game. You can use this to link a
                                                    # sequence of game states together for logging purposes, or to
                                                    # make sure that the same strategy is played for an entire game
    "round":0,                                      # Index of the current round within a sit'n'go
    "bet_index":0,                                  # Index of the betting opportunity within a round
    "small_blind": 10,                              # The small blind in the current round. The big blind is twice the
                                                    #     small blind
    "current_buy_in": 320,                          # The amount of the largest current bet from any one player
    "pot": 400,                                     # The size of the pot (sum of the player bets)
    "minimum_raise": 240,                           # Minimum raise amount. To raise you have to return at least:
                                                    #     current_buy_in - players[in_action][bet] + minimum_raise
    "dealer": 1,                                    # The index of the player on the dealer button in this round
                                                    #     The first player is (dealer+1)%(players.length)
    "orbits": 7,                                    # Number of orbits completed. (The number of times the dealer
                                                    #     button returned to the same player.)
    "in_action": 1,                                 # The index of your player, in the players array
    "players": [                                    # An array of the players. The order stays the same during the
        {                                           #     entire tournament
            "id": 0,                                # Id of the player (same as the index)
            "name": "Albert",                       # Name specified in the tournament config
            "status": "active",                     # Status of the player:
                                                    #   - active: the player can make bets, and win the current pot
                                                    #   - folded: the player folded, and gave up interest in
                                                    #       the current pot. They can return in the next round.
                                                    #   - out: the player lost all chips, and is out of this sit'n'go
            "version": "Default random player",     # Version identifier returned by the player
            "stack": 1010,                          # Amount of chips still available for the player. (Not including
                                                    #     the chips the player bet in this round.)
            "bet": 320                              # The amount of chips the player put into the pot
        },
        {
            "id": 1,                                # Your own player looks similar, with one extension.
            "name": "PyRates",
            "status": "active",
            "version": "Default random player",
            "stack": 1590,
            "bet": 80,
            "hole_cards": [                         # The cards of the player. This is only visible for your own player
                                                    #     except after showdown, when cards revealed are also included.
                {
                    "rank": "6",                    # Rank of the card. Possible values are numbers 2-10 and J,Q,K,A
                    "suit": "hearts"                # Suit of the card. Possible values are: clubs,spades,hearts,diamonds
                },
                {
                    "rank": "K",
                    "suit": "spades"
                }
            ]
        },
        {
            "id": 2,
            "name": "Chuck",
            "status": "out",
            "version": "Default random player",
            "stack": 0,
            "bet": 0
        }
    ],
    "community_cards": [                            # Finally the array of community cards.
        {
            "rank": "4",
            "suit": "spades"
        },
        {
            "rank": "A",
            "suit": "hearts"
        },
        {
            "rank": "6",
            "suit": "clubs"
        }
    ]
}
