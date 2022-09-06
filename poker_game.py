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
        self._driver = driver
        self._state = None
        self._current_bets = None
        self._has_betting_changed = False
        self._has_state_changed = False
        self._has_folded = False

    def set_state(self, public_cards):
        new_state = None
        if len(public_cards) == 0:
            new_state = PokerGameState.PREFLOP
            logging.info('preflop')
            self._has_folded = False
        elif len(public_cards) == 3:
            new_state = PokerGameState.FLOP
            logging.info('flop')
        elif len(public_cards) == 4:
            new_state = PokerGameState.TURN
            logging.info('turn')
        elif len(public_cards) == 5:
            new_state = PokerGameState.RIVER
            logging.info('river')
        if new_state != self._state:
            self._has_state_changed = True
            self._current_bets = None
            self._has_betting_changed = True
        self._state = new_state
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
        if not self._current_bets or len(
                current_bets) != len(self._current_bets):
            self._has_betting_changed = True
        self._current_bets = current_bets

    def decide(self):
        if self._has_folded:
            return

        if not self._has_state_changed and not self._has_betting_changed:
            return

        if self._state == PokerGameState.PREFLOP:
            self._preflop()
        self._has_decided = True

    def _preflop(self):
        is_on_button = False
        has_someone_open = False
        for player_id in self._current_bets:
            if player_id == self.hero_id:
                self._current_bets[player_id] == self._big_bind
                is_on_button = True
                continue
            else:
                if int(self._current_bets[player_id]) > self._big_bind:
                    has_someone_open = True
        if not is_on_button or (is_on_button and has_someone_open):
            fold(self._driver)
            self._has_folded = True
