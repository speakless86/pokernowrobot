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
            # if 'tB' in data and len(data['tB']) == 1:
            #    logging.info(data['tB'])
            #    if 'pGS' in data:
            #        logging.info(data['pGS'])
            if 'oTC' in data:
                self._poker_game.set_state(data['oTC']['1'])
            # elif 'pGS' in data:
            #    logging.info(data['pGS'])