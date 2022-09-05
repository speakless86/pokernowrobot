#!/usr/bin/env python3
"""Poker Game"""
import logging
from enum import Enum

class PokerGameState(Enum):
    WAITING = 0
    PREFLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4
    FINISHED = 5

class PokerGame:
    def __init__(players):
        self._players = players
        self._state = PokerGameState.WAITING

    def start_game():
        self._state = PokerGameState.PREFLOP

    def end_game():
        self._state = PokerGameState.FINISHED

    def next_state():
        '''Return the next state.
           If the game has not started or has finished, return -1.
           Otherwise, return the next state in game.'''
        if self._state in [PokerGameState.WAITING, PokerGameState.FINISHED]:
            return -1
        elif self._state == PokerGameState.PREFLOP:
            return PokerGameState.FLOP
        elif self._state == PokerGameState.FLOP:
            return PokerGameState.TURN
        elif self._state == PokerGameState.TURN:
            return PokerGameState.RIVER
        elif self._state == PokerGameState.RIVER:
            return PokerGameState.PREFLOP

