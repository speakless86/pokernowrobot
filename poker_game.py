#!/usr/bin/env python3
"""Poker Game"""
import logging
import threading
import time
from enum import Enum

from poker_range import PokerRange
from pokernow_control_utils import send_message, fold


class PokerGameState(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3


class PokerGame:
    def __init__(self, driver):
        self._driver = driver
        self._has_betting_changed = False
        self._has_state_changed = False
        self._has_folded = False
        self._current_bets = dict()
        self._state = None
        self._lock = threading.Lock()
        self._preflop_play_range = PokerRange(
            'A2s+ K2s+ Q2s+ J7s+ T6s+ 96s+ 85s+ 74s+ 63s+ 52s+ 42s+ 32s+ A2o+ K9o+ Q9o+ J9o+ T9o+ 22+ 27s')

    def set_state(self, public_cards):
        new_state = None
        if len(public_cards) == 0:
            new_state = PokerGameState.PREFLOP
            self._has_folded = False
        elif len(public_cards) == 3:
            new_state = PokerGameState.FLOP
        elif len(public_cards) == 4:
            new_state = PokerGameState.TURN
        elif len(public_cards) == 5:
            new_state = PokerGameState.RIVER
        if new_state != self._state:
            logging.info(f'State changes from {self._state} to {new_state}')
            self._has_state_changed = True
            self._current_bets = dict()
            self._has_betting_changed = True
        self._state = new_state
        logging.info(public_cards)

    def set_hero(self, hero_id, hero_name):
        self.hero_id = hero_id
        self._hero_name = hero_name

    def set_big_blind(self, big_blind):
        self._big_blind = big_blind

    def set_small_blind(self, small_blind):
        self._small_blind = small_blind

    def set_big_blind_player(self, player_id):
        self._big_blind_player = player_id

    def set_self_cards(self, self_cards):
        self._self_cards = self_cards

    def set_current_bets(self, current_bets):
        for player_id in current_bets:
            if player_id not in self._current_bets or self._current_bets[
                    player_id] != current_bets[player_id]:
                self._has_betting_changed = True
                if current_bets[player_id] == '<D>' and player_id in self._current_bets:
                    del self._current_bets[player_id]
                else:
                    self._current_bets[player_id] = current_bets[player_id]

    def set_current_action_player(self, player_id):
        self._current_action_player_id = player_id

    def decide(self):
        try:
            self._lock.acquire()
            if self._current_action_player_id != self.hero_id:
                return

            if self._has_folded:
                return

            if self._state == PokerGameState.PREFLOP:
                self._preflop()
            self._has_decided = True
        finally:
            self._lock.release()

    def _preflop(self):
        is_big_blind = self._big_blind_player == self.hero_id

        has_someone_open = False
        for player_id in self._current_bets:
            if player_id == self.hero_id:
                continue

            if self._current_bets[player_id] > self._big_blind:
                has_someone_open = True

        if not is_big_blind or (is_big_blind and has_someone_open):
            logging.info(f'Hero is holding {self._self_cards}')
            if not self._preflop_play_range.is_in_range(self._self_cards):
                # send_message(self._driver, f'I am folding in 3 seconds')
                logging.info('Hero is going to fold in 3 seoncds.')
                time.sleep(3)
                fold(self._driver)
                self._has_folded = True
