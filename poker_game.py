#!/usr/bin/env python3
"""Poker Game"""
import logging
import threading
import time
from enum import Enum

from poker_range import PokerRange
from utils.pokernow_control_utils import bet, send_message, fold


class PokerGameState(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3


class PokerGame:
    def __init__(self, driver):
        self._driver = driver
        self._has_acted = False
        self._current_bets = dict()
        self._state = None
        self._lock = threading.Lock()
        self._current_action_player_id = None
        self._preflop_play_range = PokerRange(
            'A2s+ K2s+ Q2s+ J7s+ T6s+ 96s+ 85s+ 74s+ 63s+ 52s+ 42s+ 32s+ A2o+ K9o+ Q9o+ J9o+ T9o+ 22+ 27s')

    def set_state(self, public_cards):
        new_state = None
        if len(public_cards) == 0:
            new_state = PokerGameState.PREFLOP
        elif len(public_cards) == 3:
            new_state = PokerGameState.FLOP
        elif len(public_cards) == 4:
            new_state = PokerGameState.TURN
        elif len(public_cards) == 5:
            new_state = PokerGameState.RIVER
        if new_state != self._state:
            logging.info(f'State changes from {self._state} to {new_state}')
            self._has_acted = False
            self._current_bets = dict()
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
                if current_bets[player_id] == '<D>' and player_id in self._current_bets:
                    del self._current_bets[player_id]
                else:
                    self._current_bets[player_id] = current_bets[player_id]

    def set_current_action_player(self, player_id):
        self._current_action_player_id = player_id

    def set_game_result(self, game_result):
        # It is possible to change state from PREFLOP to PREFLOP.
        logging.info('A new round is started.')
        self._has_acted = False

    def decide(self):
        try:
            self._lock.acquire()
            if self._current_action_player_id != self.hero_id:
                return

            if self._has_acted:
                return

            if self._state == PokerGameState.PREFLOP:
                self._preflop()
        finally:
            self._lock.release()

    def _preflop(self):
        is_big_blind = self._big_blind_player == self.hero_id

        has_someone_opened = False
        for player_id in self._current_bets:
            if player_id == self.hero_id:
                continue

            if self._current_bets[player_id] > self._big_blind:
                has_someone_opened = True

        is_in_play_range = self._preflop_play_range.is_in_range(self._self_cards)
        if not is_big_blind or (is_big_blind and has_someone_opened):
            logging.info(f'Hero is holding {self._self_cards}')
            if not is_in_play_range:
                logging.info('Hero is going to fold immediately.')
                fold(self._driver)
                self._has_acted = True
                return

        if is_in_play_range and not has_someone_opened:
            logging.info('Hero is going to open.')
            num_players = len(self._current_bets)
            bet(self._driver, self._big_blind * (num_players + 2))
            self._has_acted = True
        else:
            logging.info(f'has_someone_opened={has_someone_opened}')
            logging.info(f'is_big_blind={is_big_blind}')
            logging.info(f'is_in_play_range={is_in_play_range}')
