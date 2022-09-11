#!/usr/bin/env python3
"""Poker Range"""


class PokerRange:
    """Support to analyze poker range.
       Supported representation:
       a6o+, 78s+, 66+
    """
    _CARD_ORDER = [
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        'T',
        'J',
        'Q',
        'K',
        'A']

    def __init__(self, poker_range_string):
        self._range_items = poker_range_string.split()

    def is_in_range(self, cards):
        card0 = cards[0]
        card1 = cards[1]
        is_suited = card0[1] == card1[1]
        is_pair = card0[0] == card1[0]

        if self._compare_cards(card0[0], card1[0]) < 0:
            card0, card1 = card1, card0

        for range_item in self._range_items:
            if is_pair:
                if 'o' in range_item or 's' in range_item:
                    continue
                if self._compare_cards(
                        card0[0], range_item[0]) > 0 and '+' in range_item:
                    return True
                if self._compare_cards(card0[0], range_item[0]) == 0:
                    return True
            else:
                range_is_suited = range_item[2] == 's'
                if is_suited != range_is_suited:
                    continue
                if card0[0] != range_item[0]:
                    continue
                if self._compare_cards(
                        card1[0], range_item[1]) > 0 and '+' in range_item:
                    return True
                if self._compare_cards(card1[0], range_item[1]) == 0:
                    return True
        return False

    def _compare_cards(self, card0, card1):
        index0 = self._CARD_ORDER.index(card0)
        index1 = self._CARD_ORDER.index(card1)
        if index0 == index1:
            return 0
        elif index0 > index1:
            return 1
        else:
            return -1


if __name__ == '__main__':
    poker_range = PokerRange('66+')
    print(poker_range.is_in_range('ahad'))
