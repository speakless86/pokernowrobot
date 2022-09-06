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
        self._state = None

    def set_state(self, public_cards):
        if len(public_cards) == 0:
            self._state = PokerGameState.PREFLOP
            preflop()
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

    def set_hero(self, hero_id, hero_name):
        self.hero_id = hero_id
        self._hero_name = hero_name

    def set_big_bind(self, big_bind):
        self._big_bind = big_bind

    def set_small_bind(self, small_bind):
        self._small_bind = small_bind

    def set_self_cards(self, self_cards):
        self._self_cards = self_cards

    def set_current_bets(self, current_bets):
        self._current_bets = current_bets

    def decide(self):
        if not self._state:
            return
        if self._state == PokerGameState.PREFLOP:
            _preflop()

    def _preflop(self):
        if not self._state:
            logging.info('Can not fold because state is unknown!')
            return

        is_on_button = False
        has_someone_open = False
        for player_id in self._current_bets:
            if player_id == self.hero_id:
                self._current_bets[player_id] == self._big_bind
                is_on_button = True
                continue
            else:
                if self._current_bets[player_id] > self._big_bind:
                    has_someone_open = True

        if not is_not_button or (is_on_button and has_someone_open):
            fold(self._driver)
