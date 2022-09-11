#!/usr/bin/env python3
"""Poker Rangei Unit Tests"""

import unittest
import logging

from poker_range import PokerRange


class TestPokerRange(unittest.TestCase):

    def setUp(self):
        self._suited_poker_range = PokerRange('A7s+')
        self._offsuit_poker_range = PokerRange('97o+')
        self._pair_poker_range = PokerRange('66+')

    def _test_range(self, poker_range, in_range_list, out_of_range_list):
        for cards in in_range_list:
            logging.warning(cards)
            self.assertEqual(poker_range.is_in_range(cards), True)
            cards.reverse()
            self.assertEqual(poker_range.is_in_range(cards), True)

        for cards in out_of_range_list:
            logging.warning(cards)
            self.assertEqual(poker_range.is_in_range(cards), False)
            cards.reverse()
            self.assertEqual(poker_range.is_in_range(cards), False)
   
    def test_is_in_suited_range(self):
        in_range_list = [['Ah', '7h'], ['Ad', '7d'], ['Ac', '9c']]
        out_of_range_list = [['Kh', '7h'], ['Kc', 'Qc'], ['Ah', '7c'], ['Ac', '7h'], ['Kc', 'Ks']]
        self._test_range(self._suited_poker_range, in_range_list, out_of_range_list)

    def test_is_in_offsuit_range(self):
        in_range_list = [['9h', '7c'], ['9s', '8d']]
        out_of_range_list = [['Ts', '9d'], ['9c', '6s'], ['9s', '9h']]
        self._test_range(self._offsuit_poker_range, in_range_list, out_of_range_list)

    def test_is_in_pair_range(self):
        in_range_list = [['6s', '6c'], ['7h', '7d'], ['Ad', 'Ah']]
        out_of_range_list = [['5c', '5s'], ['6s', '7c']]
        self._test_range(self._pair_poker_range, in_range_list, out_of_range_list)


if __name__ == '__main__':
    unittest.main()
