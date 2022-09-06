#!/usr/bin/env python3
"""Process Pokernow Events"""
import json
import logging

from poker_game import PokerGame


class PokerNowProcessor:
    def __init__(self):
        self._poker_game = PokerGame()

    def process(self, event, data):
        if event == 'gC':
            if 'oTC' in data:
                public_cards = data['oTC']['1']
                self._poker_game.set_state(public_cards)

            if 'pC' in data:
                for player_id in data['pC']:
                    player_cards = data['pC'][player_id]
                    if player_cards == '<D>':
                        continue
                    self_cards = player_cards['cards']
                    self._poker_game.set_self_cards(self_cards)
                    break
            # logging.info(json.dumps(data, indent=2))
