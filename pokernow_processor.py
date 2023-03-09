#!/usr/bin/env python3
"""Process Pokernow Events"""
import json
import logging

from poker_game import PokerGame


class PokerNowProcessor:
    def __init__(self, driver):
        self._poker_game = PokerGame(driver)
        self._has_registered = False

    def _process_game_state(self, data, is_first_message):
        if 'pC' in data:
            # logging.info(f'pC={data["pC"]}')
            show_card_dict = dict()
            for player_id in data['pC']:
                if player_id != self._poker_game.hero_id:
                    continue
                player_cards = data['pC'][player_id]
                if not isinstance(player_cards, dict):
                    continue
                self._poker_game.set_hero_cards(player_cards['cards'])
                break

        if 'players' in data and is_first_message:
            self._poker_game.set_players(data['players'])

        if 'cPI' in data:
            # logging.info(f'cPI={data["cPI"]}')
            self._poker_game.set_current_action_player(data['cPI'])

        if 'bigBlind' in data:
            self._poker_game.set_big_blind(data['bigBlind'])

        if 'bBPI' in data:
            self._poker_game.set_big_blind_player(data['bBPI'])

        if 'smallBlind' in data:
            self._poker_game.set_small_blind(data['smallBlind'])

        if 'gameResult' in data:
            self._poker_game.set_game_result(data['gameResult'])

        if 'dealerId' in data:
            self._poker_game.set_dealer_id(data['dealerId'])

        if 'dealerSeat' in data:
            self._poker_game.set_dealer_seat(data['dealerSeat'])

        if 'oTC' in data:
            # logging.info(f'oTC={data["oTC"]}')
            public_cards = data['oTC']['1']
            self._poker_game.set_state(public_cards, is_first_message)

        if 'pGS' in data and not is_first_message:
            self._poker_game.set_fold(data['pGS'])

        if 'tB' in data:
            # logging.info(f'tB={data["tB"]}')
            self._poker_game.set_current_bets(data['tB'], is_first_message)

    def process(self, event, data):
        if event == 'registered':
            self._poker_game.set_hero(
                data['currentPlayer']['id'],
                data['currentPlayer']['networkUsername'])
            print("Registered")
            print(data['gameState'])
            self._process_game_state(data['gameState'], True)
            self._has_registered = True
        elif event == 'gC':
            print("GC!")
            print(data)
            self._process_game_state(data, False)

        # Start to decide once the game state is refreshed by the `registered` message.
        if self._has_registered:
            self._poker_game.decide()
