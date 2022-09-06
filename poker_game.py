#!/usr/bin/env python3
"""Poker Game"""
import logging
from enum import Enum

from pokernow_control_utils import fold


class PokerGameState(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3


class PokerGame:
    def __init__(self, driver):
        logging.info('Started')
        self._driver = driver

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

    def set_self_cards(self, self_cards, is_on_button):
        logging.info("Found self cards!")
        logging.info(self_cards)
        if is_on_button:
            logging.info('Can not fold on button!')
            return

        if not self._state:
            logging.info('Can not fold because state is unknown!')
            return

        if self._state == PokerGameState.PREFLOP:
            fold(self._driver)
