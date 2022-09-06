#!/usr/bin/env python3
"""Process Pokernow Events"""
import json
import logging

from poker_game import PokerGame


class PokerNowProcessor:
    def __init__(self, driver):
        self._poker_game = PokerGame(driver)

    def process(self, event, data):
        has_registered = False
        if event == 'registered':
            self._poker_game.set_hero(
                data['currentPlayer']['id'],
                data['currentPlayer']['networkUsername'])
            self._poker_game.set_big_bind(data['gameState']['bigBlind'])
            self._poker_game.set_small_bind(
                data['gameState']['smallBlind'])
            self._poker_game.set_current_bets(data['gameState']['tB'])
            has_registered = True
        elif event == 'gC':
            logging.info(data)
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

            if 'tB' in data:
                self._poker_game.set_current_bets(data['tB'])

            if 'pGS' in data:
                logging.warning(data['pGS'])
                self._poker_game.set_player_status(data['pGS'])

        # Only start to process if the `registered` message has been delivered.
        if has_registered:
            self._poker_game.decide()
