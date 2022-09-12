"""
Runs a Montecarlo simulation to calculate the probability
of winning with a certain pokerhand and a given amount of player.
From: https://github.com/dickreuter/neuron_poker
"""

from tools.hand_evaluator import eval_best_hand

__author__ = 'Nicolas Dickreuter'

import logging
import operator
import time
from collections import Counter
from copy import copy

import numpy as np


from tools.hand_evaluator import eval_best_hand


log = logging.getLogger(__name__)

class MonteCarlo(object):

    def get_two_short_notation(self, input_cards, add_O_to_pairs=False):
        card1 = input_cards[0][0]
        card2 = input_cards[1][0]
        suited_str = 's' if input_cards[0][1] == input_cards[1][1] else 'o'
        if card1[0] == card2[0]:
            if add_O_to_pairs:
                suited_str = "o"
            else:
                suited_str = ''

        return card1 + card2 + suited_str, card2 + card1 + suited_str

    def get_opponent_allowed_cards_list(self, opponent_ranges):
        self.preflop_equities = {
            "23o": 0.354,
            "24o": 0.36233333333333334,
            "26o": 0.3758666666666667,
            "34o": 0.3792,
            "25o": 0.3804666666666667,
            "27o": 0.3807333333333333,
            "23s": 0.3876,
            "36o": 0.39,
            "35o": 0.3900666666666667,
            "37o": 0.3957333333333333,
            "38o": 0.40013333333333334,
            "24s": 0.4024,
            "27s": 0.405,
            "28o": 0.4060666666666667,
            "25s": 0.4076,
            "26s": 0.41046666666666665,
            "46o": 0.4108,
            "47o": 0.41713333333333336,
            "34s": 0.4176666666666667,
            "45o": 0.4179333333333333,
            "29o": 0.4215333333333333,
            "48o": 0.4234,
            "37s": 0.424,
            "35s": 0.4246,
            "36s": 0.4268,
            "39o": 0.42733333333333334,
            "56o": 0.428,
            "28s": 0.42873333333333336,
            "57o": 0.4331333333333333,
            "49o": 0.43473333333333336,
            "38s": 0.4358,
            "2To": 0.4362666666666667,
            "58o": 0.4378666666666667,
            "45s": 0.4434666666666667,
            "46s": 0.4444,
            "47s": 0.4448666666666667,
            "67o": 0.4461333333333333,
            "3To": 0.4532,
            "48s": 0.4534,
            "56s": 0.4538,
            "29s": 0.45466666666666666,
            "39s": 0.45686666666666664,
            "68o": 0.4570666666666667,
            "59o": 0.45866666666666667,
            "57s": 0.4640666666666667,
            "4To": 0.46526666666666666,
            "49s": 0.46546666666666664,
            "2Jo": 0.466,
            "69o": 0.4666,
            "5To": 0.4672,
            "2Ts": 0.46786666666666665,
            "78o": 0.4722,
            "58s": 0.4756,
            "6To": 0.4768,
            "3Ts": 0.47733333333333333,
            "79o": 0.4788,
            "67s": 0.4808,
            "3Jo": 0.4808,
            "59s": 0.48133333333333334,
            "68s": 0.48346666666666666,
            "4Jo": 0.48633333333333334,
            "2Qo": 0.4928666666666667,
            "2Js": 0.49406666666666665,
            "69s": 0.49546666666666667,
            "3Qo": 0.4965333333333333,
            "4Ts": 0.49706666666666666,
            "6Jo": 0.4971333333333333,
            "5Jo": 0.49793333333333334,
            "5Ts": 0.5010666666666667,
            "7To": 0.5022,
            "89o": 0.5038,
            "6Ts": 0.5054,
            "78s": 0.5059333333333333,
            "3Js": 0.5124,
            "8To": 0.5130666666666667,
            "7Jo": 0.5150666666666667,
            "4Js": 0.5166,
            "79s": 0.5176666666666667,
            "7Ts": 0.5187333333333334,
            "2Qs": 0.5188666666666667,
            "22": 0.5194666666666666,
            "4Qo": 0.5205333333333333,
            "6Js": 0.5217333333333334,
            "5Qo": 0.5253333333333333,
            "5Js": 0.5254,
            "2Ko": 0.5275333333333333,
            "3Ko": 0.5282666666666667,
            "89s": 0.5294,
            "8Jo": 0.5295333333333333,
            "9To": 0.5298,
            "6Qo": 0.5319333333333334,
            "4Qs": 0.5332666666666667,
            "3Qs": 0.5352,
            "7Qo": 0.5357333333333333,
            "7Js": 0.5391333333333334,
            "4Ko": 0.5392,
            "8Ts": 0.5393333333333333,
            "5Ko": 0.5412666666666667,
            "9Jo": 0.5472666666666667,
            "5Qs": 0.5484666666666667,
            "2Ks": 0.5512666666666667,
            "33": 0.5556,
            "9Ts": 0.5558666666666666,
            "8Qo": 0.557,
            "6Qs": 0.5571333333333334,
            "8Js": 0.5590666666666667,
            "7Qs": 0.5597333333333333,
            "6Ko": 0.5597333333333333,
            "4Ks": 0.5641333333333334,
            "9Qo": 0.5652666666666667,
            "3Ks": 0.5654666666666667,
            "2Ao": 0.5668,
            "8Ko": 0.5674,
            "TJo": 0.5682666666666667,
            "7Ko": 0.5684,
            "3Ao": 0.5736666666666667,
            "8Qs": 0.5752,
            "5Ks": 0.5762666666666667,
            "9Js": 0.5798666666666666,
            "44": 0.5818666666666666,
            "6Ks": 0.5852,
            "TQo": 0.5856666666666667,
            "2As": 0.5878666666666666,
            "9Qs": 0.5883333333333334,
            "7Ks": 0.5898666666666667,
            "9Ko": 0.5908,
            "JQo": 0.5912,
            "4Ao": 0.5918666666666667,
            "6Ao": 0.5934666666666667,
            "5Ao": 0.5938,
            "TJs": 0.5943333333333334,
            "8Ks": 0.5964666666666667,
            "7Ao": 0.6003333333333334,
            "3As": 0.6010666666666666,
            "TQs": 0.6062,
            "TKo": 0.6062666666666666,
            "4As": 0.6072,
            "9Ao": 0.6084,
            "JQs": 0.6100666666666666,
            "JKo": 0.6107333333333334,
            "9Ks": 0.6149333333333333,
            "8Ao": 0.6162666666666666,
            "55": 0.6185333333333334,
            "6As": 0.6204666666666667,
            "QKo": 0.6242666666666666,
            "5As": 0.6255333333333334,
            "7As": 0.6282666666666666,
            "8As": 0.6311333333333333,
            "TKs": 0.6348666666666667,
            "TAo": 0.6371333333333333,
            "66": 0.6403333333333333,
            "QKs": 0.6410666666666667,
            "9As": 0.6426,
            "JKs": 0.6436,
            "JAo": 0.6460666666666667,
            "TAs": 0.6498,
            "QAo": 0.6514,
            "77": 0.6592,
            "KAo": 0.6592,
            "JAs": 0.6612666666666667,
            "QAs": 0.6670666666666667,
            "KAs": 0.6816666666666666,
            "88": 0.6978,
            "99": 0.7197333333333333,
            "TT": 0.7524666666666666,
            "JJ": 0.7754,
            "QQ": 0.8024,
            "KK": 0.8305333333333333,
            "AA": 0.8527333333333333}
        peflop_equity_list = sorted(
            self.preflop_equities.items(),
            key=operator.itemgetter(1))

        counts = len(peflop_equity_list)
        take_top = int(counts * opponent_ranges)
        allowed = set(list(peflop_equity_list)[-take_top:])
        allowed_cards = [i[0] for i in allowed]
        # log.debug("Allowed range: "+str(allowed_cards))
        return set(allowed_cards)

    def create_card_deck(self):
        values = "23456789TJQKA"
        suites = "CDHs"
        Deck = []
        [Deck.append(x + y) for x in values for y in suites]
        return Deck

    def distribute_cards_to_players(
            self,
            deck,
            player_amount,
            player_card_list,
            known_table_cards,
            opponent_allowed_cards,
            passes):

        # rmove table cards from deck
        CardsOnTable = []
        for known_table_card in known_table_cards:
            # remove cards that are on the table from the deck
            CardsOnTable.append(deck.pop(deck.index(known_table_card)))

        all_players = []
        knownPlayers = 0  # for potential collusion if more than one bot is running on the same table

        for player_cards in player_card_list:
            known_player = []

            if isinstance(player_cards, set):
                while True:
                    passes += 1
                    random_card1 = np.random.randint(0, len(deck))
                    random_card2 = np.random.randint(0, len(deck) - 1)
                    if not random_card1 == random_card2:
                        crd1, crd2 = self.get_two_short_notation(
                            [deck[random_card1], deck[random_card2]], add_O_to_pairs=False)
                        if crd1 in player_cards or crd2 in player_cards:
                            break
                player_cards = []
                player_cards.append(deck[random_card1])
                player_cards.append(deck[random_card2])

            known_player.append(player_cards[0])
            known_player.append(player_cards[1])
            all_players.append(known_player)

            try:
                deck.pop(deck.index(player_cards[0]))
            except BaseException:
                pass
            try:
                deck.pop(deck.index(player_cards[1]))
            except BaseException:
                pass

            knownPlayers += 1  # my own cards are known

        for _ in range(player_amount - knownPlayers):
            random_player = []
            while True:
                passes += 1
                random_card1 = np.random.randint(0, len(deck))
                random_card2 = np.random.randint(0, len(deck) - 1)

                if not random_card1 == random_card2:
                    crd1, crd2 = self.get_two_short_notation(
                        [deck[random_card1], deck[random_card2]], add_O_to_pairs=False)
                    if crd1 in opponent_allowed_cards or crd2 in opponent_allowed_cards:
                        break

            random_player.append(deck.pop(random_card1))
            random_player.append(deck.pop(random_card2))

            all_players.append(random_player)

        return all_players, deck, passes

    def distribute_cards_to_table(self, Deck, table_card_list):
        remaningRandoms = 5 - len(table_card_list)
        for n in range(0, remaningRandoms):
            table_card_list.append(
                Deck.pop(
                    np.random.randint(
                        0, len(Deck) - 1)))
        return table_card_list

    def run_montecarlo(
            self,
            original_player_card_list,
            original_table_card_list,
            player_amount,
            ui,
            maxRuns,
            timeout,
            ghost_cards,
            opponent_range=1):

        if isinstance(
                opponent_range,
                float) or isinstance(
                opponent_range,
                int):
            opponent_allowed_cards = self.get_opponent_allowed_cards_list(
                opponent_range)
            log.debug('Preflop reverse tables for ranges for opponent: NO')
        elif type(opponent_range == set):
            log.debug('Preflop reverse tables for ranges for opponent: YES')
            opponent_allowed_cards = opponent_range

        winnerCardTypeList = []
        wins = 0
        runs = 0
        passes = 0
        OriginalDeck = self.create_card_deck()
        if ghost_cards != '':
            OriginalDeck.pop(OriginalDeck.index(ghost_cards[0]))
            OriginalDeck.pop(OriginalDeck.index(ghost_cards[1]))

        for m in range(maxRuns):
            runs += 1
            Deck = copy(OriginalDeck)
            PlayerCardList = copy(original_player_card_list)
            TableCardsList = copy(original_table_card_list)
            Players, Deck, passes = self.distribute_cards_to_players(
                Deck, player_amount, PlayerCardList, TableCardsList, opponent_allowed_cards, passes)
            Deck5Cards = self.distribute_cards_to_table(Deck, TableCardsList)
            PlayerFinalCardsWithTableCards = []
            for o in range(0, player_amount):
                PlayerFinalCardsWithTableCards.append(Players[o] + Deck5Cards)

            bestHand, winnerCardType = eval_best_hand(
                PlayerFinalCardsWithTableCards)
            winner = (PlayerFinalCardsWithTableCards.index(bestHand))

            # print (winnerCardType)

            CollusionPlayers = 0
            if winner < CollusionPlayers + 1:
                wins += 1
                # winnerlist.append(winner)  # self.equity=wins/m  # if
                # self.equity>0.99: self.equity=0.99  #
                # EquityList.append(self.equity)
                winnerCardTypeList.append(winnerCardType)

            self.equity = np.round(wins / runs, 3)

            if passes > 999 and time.time() > timeout:
                log.debug("Cutting short montecarlo due to timeout")
                log.debug("Passes: " + str(passes))
                log.debug("Runs: " + str(runs))
                break

                # if passes >= maxruns: break

        self.equity = wins / runs
        self.winnerCardTypeList = Counter(winnerCardTypeList)
        for key, value in self.winnerCardTypeList.items():
            self.winnerCardTypeList[key] = value / runs

        self.winTypesDict = self.winnerCardTypeList.items()
        self.runs = runs
        self.passes = passes

        return self.equity, self.winTypesDict


def run_montecarlo_wrapper(
        p,
        ui_action_and_signals,
        config,
        ui,
        t,
        L,
        preflop_state,
        h):
    # Prepare for montecarlo simulation to evaluate equity (probability of
    # winning with given cards)
    m = MonteCarlo()

    if t.gameStage == "PreFlop":
        t.assumedPlayers = 2
        opponent_range = 1

    elif t.gameStage == "Flop":

        if t.isHeadsUp:
            for i in range(5):
                if t.other_players[i]['status'] == 1:
                    break
            n = t.other_players[i]['utg_position']
            log.debug("Opponent utg position: " + str(n))
            opponent_range = float(p.selected_strategy['range_utg' + str(n)])
        else:
            opponent_range = float(
                p.selected_strategy['range_multiple_players'])

        t.assumedPlayers = t.other_active_players - \
            int(round(t.playersAhead * (1 - opponent_range))) + 1

    else:

        if t.isHeadsUp:
            for i in range(5):
                if t.other_players[i]['status'] == 1:
                    break
            n = t.other_players[i]['utg_position']
            log.debug("Opponent utg position: " + str(n))
            opponent_range = float(p.selected_strategy['range_utg' + str(n)])
        else:
            opponent_range = float(
                p.selected_strategy['range_multiple_players'])

        t.assumedPlayers = t.other_active_players + 1

    t.assumedPlayers = min(max(t.assumedPlayers, 2), 4)

    t.PlayerCardList = []
    t.PlayerCardList.append(t.mycards)
    t.PlayerCardList_and_others = copy(t.PlayerCardList)

    ghost_cards = ''
    m.collusion_cards = ''

    if p.selected_strategy['collusion'] == 1:
        collusion_cards, collusion_player_dropped_out = L.get_collusion_cards(
            h.game_number_on_screen, t.gameStage)

        if collusion_cards != '':
            m.collusion_cards = collusion_cards
            if not collusion_player_dropped_out:
                t.PlayerCardList_and_others.append(collusion_cards)
                log.debug(
                    "Collusion found, player still in game. " +
                    str(collusion_cards))
            elif collusion_player_dropped_out:
                log.debug(
                    "COllusion found, but player dropped out." +
                    str(collusion_cards))
                ghost_cards = collusion_cards
        else:
            log.debug("No collusion found")

    else:
        m.collusion_cards = ''

    if t.gameStage == "PreFlop":
        maxRuns = 1000
    else:
        maxRuns = 7500

    if t.gameStage != 'PreFlop':
        try:
            for abs_pos in range(5):
                if t.other_players[abs_pos]['status'] == 1:
                    sheet_name = preflop_state.get_reverse_sheetname(
                        abs_pos, t, h)
                    ranges = preflop_state.get_rangecards_from_sheetname(
                        abs_pos, sheet_name, t, h, p)
                    # log.debug("Ranges from reverse table: "+str(ranges))

                    # the last player's range will be relevant
                    if t.isHeadsUp:
                        opponent_range = ranges

        except Exception as e:
            log.error("Opponent reverse table failed: " + str(e))

    ui_action_and_signals.signal_status.emit(
        "Running range Monte Carlo: " + str(maxRuns))
    log.debug("Running Monte Carlo")
    t.montecarlo_timeout = float(config['montecarlo_timeout'])
    timeout = t.mt_tm + t.montecarlo_timeout
    log.debug("Used opponent range for montecarlo: " + str(opponent_range))
    log.debug("maxRuns: " + str(maxRuns))
    log.debug("Player amount: " + str(t.assumedPlayers))

    # calculate range equity
    if t.gameStage != 'PreFlop' and p.selected_strategy['use_relative_equity']:
        if p.selected_strategy['preflop_override'] and preflop_state.preflop_bot_ranges is not None:
            t.player_card_range_list_and_others = t.PlayerCardList_and_others[:]
            t.player_card_range_list_and_others[0] = preflop_state.preflop_bot_ranges

            t.range_equity, _ = m.run_montecarlo(t.player_card_range_list_and_others, t.cardsOnTable,
                                                 int(t.assumedPlayers), ui, maxRuns=maxRuns, ghost_cards=ghost_cards,
                                                 timeout=timeout, opponent_range=opponent_range)
            t.range_equity = np.round(t.range_equity, 2)
            log.debug(
                "Range montecarlo completed successfully with runs: " + str(m.runs))
            log.debug("Range equity (range for bot): " + str(t.range_equity))

    if preflop_state.preflop_bot_ranges is None and p.selected_strategy[
            'preflop_override'] and t.gameStage != 'PreFlop':
        log.error("No preflop range for bot, assuming 50% relative equity")
        t.range_equity = .5

    ui_action_and_signals.signal_progressbar_increase.emit(10)
    ui_action_and_signals.signal_status.emit(
        "Running card Monte Carlo: " + str(maxRuns))

    # run montecarlo for absolute equity
    t.abs_equity, _ = m.run_montecarlo(t.PlayerCardList_and_others, t.cardsOnTable, int(t.assumedPlayers), ui,
                                       maxRuns=maxRuns, ghost_cards=ghost_cards, timeout=timeout,
                                       opponent_range=opponent_range)
    ui_action_and_signals.signal_status.emit(
        "Monte Carlo completed successfully")
    log.debug("Cards Monte Carlo completed successfully with runs: " + str(m.runs))
    log.debug("Absolute equity (no ranges for bot) " +
              str(np.round(t.abs_equity, 2)))

    if t.gameStage == "PreFlop":
        crd1, crd2 = m.get_two_short_notation(t.mycards)
        if crd1 in m.preflop_equities:
            m.equity = m.preflop_equities[crd1]
        elif crd2 in m.preflop_equities:
            m.equity = m.preflop_equities[crd2]
        elif crd1 + 'O' in m.preflop_equities:
            m.equity = m.preflop_equities[crd1 + 'O']
        else:
            log.warning(
                "Preflop equity not found in lookup table: " +
                str(crd1))
        t.abs_equity = m.equity

    t.abs_equity = np.round(t.abs_equity, 2)
    t.winnerCardTypeList = m.winnerCardTypeList

    ui_action_and_signals.signal_progressbar_increase.emit(15)
    m.opponent_range = opponent_range

    if t.gameStage != 'PreFlop' and p.selected_strategy['use_relative_equity']:
        t.relative_equity = np.round(t.abs_equity / t.range_equity / 2, 2)
        log.info("Relative equity (equity/range equity/2): " +
                 str(t.relative_equity))
    else:
        t.range_equity = ''
        t.relative_equity = ''
    return m


def get_equity(player_cards, table_cards, players, runs):
    """Get equity from a monteacrlo run"""
    simulation = MonteCarlo()
    simulation.run_montecarlo([list(player_cards)],
                              list(table_cards),
                              players,
                              1,
                              maxRuns=runs,
                              timeout=time.time() + 1,
                              ghost_cards='',
                              opponent_range=1)
    return simulation.equity


if __name__ == '__main__':
    Simulation = MonteCarlo()
    log = logging.getLogger('Montecarlo main')
    log.setLevel(logging.DEBUG)
    # my_cards = [['2D', 'AD']]
    # cards_on_table = ['3S', 'AH', '8D']
    # my_cards = [['KS', 'KC']]
    my_cards = [{'AKO', 'AA'}]
    cards_on_table = ['3D', '9H', 'AS', '7S', 'QH']
    players = 3
    secs = 5
    maxruns = 10000
    start_time = time.time()
    timeout = start_time + secs
    ghost_cards = ''
    Simulation.run_montecarlo(
        my_cards,
        cards_on_table,
        player_amount=players,
        ui=None,
        maxRuns=maxruns,
        ghost_cards=ghost_cards,
        timeout=timeout,
        opponent_range=0.25)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Runs: " + str(Simulation.runs))
    print("Passes: " + str(Simulation.passes))
    equity = Simulation.equity  # considering draws as wins
    print("Equity: " + str(equity))
