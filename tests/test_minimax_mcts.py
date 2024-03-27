import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np

from tests.test import test
from state import State, DRAW_COUNTER_THRESHOLD
from player import Player
from game import Game
from heuristics.heuristic import Heuristic
from heuristics.nr_pieces_heuristic import NrPiecesHeuristic
from heuristics.adjacent_pieces_heuristic import AdjacentPiecesHeuristic
from heuristics.heuristics_list import HeuristicsList
from heuristics.win_heuristic import WinHeuristic
from heuristics.groups_heuristic import GroupsHeuristic
from heuristics.center_control_heuristic import CenterControlHeuristic
from heuristics.approximate_enemy_heuristic import ApproximateEnemyHeuristic

from minimax import execute_minimax_move, get_minimax_move
from monte_carlo_tree_search.tree import MonteCarloTree
from monte_carlo_tree_search.tree_heuristics import MonteCarloTreeHeuristic
import time

"""
Minimax: state -> move
move -> state (execute_move)

MCTS:
(state)
move -> move
move -> state (execute_move)

"""

@test
def test_mcts_vs_minimax(
    minimax,
    mcts: MonteCarloTree,
    width: int,
    height: int,
    mcts_limit: int,
    mcts_is_white: bool,
    nr: int,
    log_states=True,
):
    wins = {}
    time_minimax = 0
    time_mcts = 0

    for _ in range(nr):
        state = State(width, height)
        mcts = MonteCarloTree(width, height, 2, 10)  # white: 2, 10; black: 10, 2
        # try:
        while not state.game_over():
            if log_states:
                state.draw()
            if state.is_white_turn():
                if mcts_is_white:
                    start = time.time()

                    mcts.train_until(mcts_limit)
                    move = mcts.get_best_move()
                    mcts.update_move(move)
                    state = state.execute_move(move)

                    end = time.time()
                    time_mcts += end - start
                else:
                    start = time.time()

                    move = minimax(state)
                    state = state.execute_move(move)
                    mcts.update_move(move)

                    end = time.time()
                    time_minimax += end - start
            else:
                if mcts_is_white:
                    start = time.time()

                    move = minimax(state)
                    state = state.execute_move(move)
                    mcts.update_move(move)

                    end = time.time()
                    time_minimax += end - start
                else:
                    start = time.time()

                    mcts.train_until(mcts_limit)
                    move = mcts.get_best_move()
                    mcts.update_move(move)
                    state = state.execute_move(move)

                    end = time.time()
                    time_mcts += end - start

        if state.count == DRAW_COUNTER_THRESHOLD:
            # if X moves have passed without a capture, the game is a draw
            print(f"Draw by {DRAW_COUNTER_THRESHOLD} moves rule (no captures)")

        if log_states:
            state.draw()

        winner = state.check_winner()

        if log_states:
            print(f"Winner: {winner}")

        wins[winner] = wins.get(winner, 0) + 1
        # except Exception as e:
        #     print(e)
        #     state.draw()
        #     print(state.get_available_moves())
        #     raise e
    return wins


def test_nr_pieces_vs_mcts_quick():
    minimax = get_minimax_move(NrPiecesHeuristic().evaluate_board, 2)
    width, height = 9, 5
    mcts = MonteCarloTree(width, height, 2, 10)  # white: 2, 10; black: 10, 2
    nr = 100
    test_mcts_vs_minimax(
        minimax,
        mcts,
        nr=nr,
        mcts_is_white=True,
        mcts_limit=100,  # mcts quick
        width=width,
        height=height,
    )
    mcts = MonteCarloTree(width, height, 10, 2)  # white: 2, 10; black: 10, 2
    test_mcts_vs_minimax(
        minimax,
        mcts,
        nr=nr,
        mcts_is_white=False,
        mcts_limit=100,  # mcts quick
        width=width,
        height=height,
    )

