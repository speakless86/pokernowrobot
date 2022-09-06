#!/usr/bin/env python3
"""Process Pokernow Events"""
import json
import logging

from poker_game import PokerGame


class PokerNowProcessor:
    def __init__(self, driver):
        self._poker_game = PokerGame(driver)

    def process(self, event, data):
        if event == 'registered':
            try:
                self._poker_game.set_hero(
                    data['currentPlayer']['id'],
                    data['currentPlayer']['networkUsername'])
                self._poker_game.set_big_bind(data['gameState']['bigBlind'])
                self._poker_game.set_small_bind(
                    data['gameState']['smallBlind'])
                self._poker_game.set_current_bets(data['gameState']['tB'])
            except BaseException:
                logging.error(json.dumps(data, indent=2))
        elif event == 'gC':
            if 'oTC' in data:
                public_cards = data['oTC']['1']
                self._poker_game.set_state(public_cards)

            if 'pC' in data:
                show_card_dict = dict()
                for player_id in data['pC']:
                    if player_id != self._poker_game.hero_id:
                        continue
                    player_cards = data['pC'][player_id]
                    if not isinstance(player_cards, dict):
                        continue
                    self._poker_game.set_self_cards(player_cards['cards'])
                    break

            if 'nB' in data:
                self._poker_game.set_current_bets(data['tB'])

        self._poker_game.decide()
