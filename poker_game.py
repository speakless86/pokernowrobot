#!/usr/bin/env python3
"""Poker Game"""
import logging
import threading
import time
import re
from enum import Enum

from poker_range import PokerRange
from utils.pokernow_control_utils import bet, send_message, fold, check, call
from utils.openai_utils import get_completion_response


class PokerGameState(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    DONE = 4


class PokerGame:
    def __init__(self, driver):
        self._driver = driver
        self._has_acted = False
        self._current_bets = dict()
        self._state = None
        self._lock = threading.Lock()
        self._current_action_player_id = None
        self._player_seats = list()
        self._player_stacks = list()
        self._dealer_id = None
        self._dealer_seat = None
        self._prompt = str()
        self._preflop_play_range = PokerRange(
            'A2s+ K2s+ Q2s+ J7s+ T6s+ 96s+ 85s+ 74s+ 63s+ 52s+ 42s+ 32s+ A2o+ K9o+ Q9o+ J9o+ T9o+ 22+ 27s')

    def set_state(self, public_cards, is_first_message):
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
            if new_state == PokerGameState.PREFLOP:
                self._prompt = 'Playing no limit poker. Small blind is {} and big blind is {}.\n'.format(self._small_blind, self._big_blind)
                self._prompt += 'bb=big bind, s=spade, c=club, h=heart, d=diamond\n'
                self._prompt += '8-max Seat #{} is the button\n'.format(self._dealer_seat)
                for idx, stack in enumerate(self._player_stacks):
                    self._prompt += '{} has {:.1f}bb\n'.format(self._get_seat_name(self._player_seats[idx]), stack / self._big_blind)
                self._update_player_stack(self._small_blind_player, self._small_blind)
                self._prompt += '{} posts the small blind {}{}\n'.format(self._get_seat_name(self._small_blind_player), self._small_blind, self._is_allin(self._small_blind_player))
                self._update_player_stack(self._big_blind_player, self._big_blind)
                self._prompt += '{} posts the big blind {}{}\n'.format(self._get_seat_name(self._big_blind_player), self._big_blind, self._is_allin(self._big_blind_player))
                self._prompt += 'Dealt to hero [{}]\n'.format(' '.join(self._hero_cards))
            elif new_state == PokerGameState.FLOP:
                self._prompt += '*** FLOP *** [{}]\n'.format(' '.join(public_cards[0:3]))
            elif new_state == PokerGameState.TURN:
                self._prompt += '*** TURN *** [{}] [{}]\n'.format(' '.join(public_cards[0:3]), public_cards[3])
            elif new_state == PokerGameState.RIVER:
                self._prompt += '*** RIVER *** [{}] [{}]\n'.format(' '.join(public_cards[0:4]), public_cards[4])

        self._state = new_state
        logging.info(public_cards)

    def set_fold(self, actions):
        for player_id, action in actions.items():
            seat_name = self._get_seat_name(player_id)
            if 'fold' in action:
                self._prompt += '{} folds\n'.format(seat_name)

    def set_players(self, players):
        self._player_seats = list()
        self._player_stacks = list()
        for player_id, stats in players.items():
            self._player_seats.append(player_id)
            self._player_stacks.append(float(stats['stack']))
        print(self._player_stacks)

    def set_hero(self, hero_id, hero_name):
        self.hero_id = hero_id
        self._hero_name = hero_name
        logging.info('set hero id={}'.format(hero_id))

    def set_big_blind(self, big_blind):
        self._big_blind = big_blind
        logging.info('set big blind')

    def set_small_blind(self, small_blind):
        self._small_blind = small_blind

    def set_big_blind_player(self, player_id):
        self._big_blind_player = player_id
        bb_index = self._player_seats.index(player_id)
        if bb_index == 0:
          self._small_blind_player = self._player_seats[-1]
        else:
          self._small_blind_player = self._player_seats[bb_index - 1]
        print('small blind player:' + self._small_blind_player)

    def set_dealer_id(self, player_id):
        self._dealer_id = player_id

    def set_dealer_seat(self, seat):
        self._dealer_seat = seat

    def set_hero_cards(self, hero_cards):
        self._hero_cards = hero_cards
        logging.info('Found hero cards {}'.format(self._hero_cards))

    def set_current_bets(self, current_bets, is_first_message):
        for player_id in current_bets:
            current_bet = current_bets[player_id]
            seat_name = self._get_seat_name_or_hero(player_id)
            if current_bet == '<D>':
                continue

            if current_bet == 'check':
                if player_id not in self._current_bets:
                    self._prompt += '{} checks\n'.format(seat_name)
                self._current_bets[player_id] = 0
                continue

            current_bet = float(current_bet)
            if player_id not in self._current_bets or self._current_bets[
                    player_id] != current_bet:
                current_max = 0
                for bet in self._current_bets.values():
                    current_max = max(current_max, bet)
                action = None
                if self._state == PokerGameState.PREFLOP:
                    if current_bet == self._big_blind and player_id != self._big_blind_player:
                        action = 'calls'
                    elif current_bet > self._big_blind and current_bet == current_max:
                        action = 'calls'
                    elif current_bet > self._big_blind and current_bet > current_max:
                        action = 'raises'
                else:
                    if current_bet == current_max:
                        action = 'calls'
                    else:
                        action = 'raises'
                if action:
                    if action == 'calls':
                        self._update_player_stack(player_id, current_bet)
                        self._prompt += '{} calls{}\n'.format(seat_name, self._is_allin(player_id))
                    elif action == 'raises':
                        self._update_player_stack(player_id, current_bet) 
                        self._prompt += '{} raises to {}bb{}\n'.format(seat_name, current_bet / self._big_blind, self._is_allin(player_id))

                        if player_id != self.hero_id:
                            self._has_acted = False
                    else:
                        print('Unknown action:{}\n'.format(action))

                self._current_bets[player_id] = current_bet

    def set_current_action_player(self, player_id):
        self._current_action_player_id = player_id

    def set_game_result(self, game_result):
        self._state = PokerGameState.DONE

    def decide(self):
        try:
            self._lock.acquire()
            if self._current_action_player_id != self.hero_id:
                return

            if self._has_acted:
                return

            if self._prompt.startswith('Playing no limit poker'):
                print(self._prompt)
                openai_response = get_completion_response(self._prompt)
                self._execute_action(openai_response.strip().split('\n')[0])
            self._has_acted = True
        finally:
            self._lock.release()

    def _get_seat_name(self, player_id):
        player_index = self._player_seats.index(player_id)
        seat_name = 'Seat {}'.format(player_index + 1)
        if player_id == self.hero_id:
            seat_name += '(hero)'
        return seat_name

    def _get_seat_name_or_hero(self, player_id):
        if player_id == self.hero_id:
            return 'hero'
        else:
            return 'Seat {}'.format(self._player_seats.index(player_id) + 1)

    def _update_player_stack(self, player_id, bet_size):
        player_index = self._player_seats.index(player_id)
        self._player_stacks[player_index] -= bet_size

    def _is_allin(self, player_id):
        player_index = self._player_seats.index(player_id)
        if self._player_stacks[player_index] <= 0:
            return ' and allins'
        else:
            return ''

    def _execute_action(self, completion):
        print(completion)
        if 'hero folds' in completion:
            logging.info('Hero is going to fold.')
            fold(self._driver)
            return

        result = re.search('hero raises (\d+.\d+)bb', completion)
        if not result:
            result = re.search('hero raises to (\d+.\d+)bb', completion)
        if result:
            bet_size = max(float(result.group(1)), 2) * self._big_blind * 1.5
            logging.info('Hero is going to raise {}.'.format(bet_size))
            bet(self._driver, bet_size)
            return

        if 'hero checks' in completion:
            logging.info('Hero is going to check.')
            check(self._driver)
            return

        if 'hero calls' in completion:
            logging.info('Hero is going to call.')
            call(self._driver)
            return

    def _preflop(self):
        is_big_blind = self._big_blind_player == self.hero_id

        has_someone_opened = False
        for player_id in self._current_bets:
            if player_id == self.hero_id:
                continue

            if self._current_bets[player_id] > self._big_blind:
                has_someone_opened = True

        is_in_play_range = self._preflop_play_range.is_in_range(self._hero_cards)
        if not is_big_blind or (is_big_blind and has_someone_opened):
            logging.info(f'Hero is holding {self._hero_cards}')
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
