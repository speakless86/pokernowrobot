#!/usr/bin/env python3
"""Poker Game"""
import logging
from enum import Enum


class PokerGameState(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3


class PokerGame:
    def __init__(self):
        logging.info('Started')

    def set_state(self, public_cards):
        if len(public_cards) == 0:
            self._state = PokerGameState.PREFLOP
            logging.info('preflop')
        elif len(public_cards) == 3:
            self._state = PokerGameState.FLOP
            logging.info('flop')
        elif len(public_cards) == 4:
            self._state = PokerGameState.TURN
            logging.info('turn')
        elif len(public_cards) == 5:
            self._state = PokerGameState.RIVER
            logging.info('river')
        logging.info(public_cards)

    def set_self_cards(self, self_cards):
        logging.info("Found self cards!")
        logging.info(self_cards)
