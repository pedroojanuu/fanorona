import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
from copy import deepcopy

from tests.test import test
from state import State
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

from monte_carlo_tree_search.tree import MonteCarloTree
from monte_carlo_tree_search.tree_heuristics import MonteCarloTreeHeuristic
import time


def play_one_game(state: State, mcts1: MonteCarloTree, no_rollouts1, mcts2: MonteCarloTree, no_rollouts2):
    # state.draw()
    time1 = 0
    time2 = 0
    while True:
        if state.player == Player.WHITE:
            start = time.time()
            mcts1.train_until(no_rollouts1)
            move_to_exe = mcts1.get_best_move()
            if(move_to_exe not in state.get_available_moves()):
                raise Exception("Invalid move: ", move_to_exe, " in ", state.get_available_moves())
            time1 += time.time() - start
        else:
            start = time.time()
            mcts2.train_until(no_rollouts2)
            move_to_exe = mcts2.get_best_move()
            if(move_to_exe not in state.get_available_moves()):
                raise Exception("Invalid move: ", move_to_exe, " in ", state.get_available_moves())
            time2 += time.time() - start
        # print()
        # print("Move to execute: ", move_to_exe)

        # print()
        # print('-'*50)
        # print()

        state = state.execute_move(move_to_exe)
        # state.draw()

        mcts1.update_move(move_to_exe)
        mcts2.update_move(move_to_exe)
        
        if state.check_winner() != Player.EMPTY:
            break
    
    state.draw()
    return (state.check_winner(), time1, time2)

def play_n_games(boardWidth, boardHeight, mcts1: MonteCarloTree, no_rollouts1, mcts2: MonteCarloTree, no_rollouts2, nr: int):
    wins = {}
    time1_total = 0
    time2_total = 0
    for _ in range(nr):
        state = State(boardWidth, boardHeight)
        mcts1_copy = deepcopy(mcts1)
        mcts2_copy = deepcopy(mcts2)
        try:
            winner, time1, time2 = play_one_game(state, mcts1_copy, no_rollouts1, mcts2_copy, no_rollouts2)
            wins[winner] = wins.get(winner, 0) + 1
            time1_total += time1
            time2_total += time2
        except Exception as e:
            print(e)
            state.draw()
            print(state.get_available_moves())
            raise e
    return (wins, time1_total, time2_total)


@test
def test_quick_vs_better(nr: int):
    boardWidth = 5
    boardHeight = 5
    mcts1 = MonteCarloTree(boardWidth, boardHeight, 2, 10)
    mcts2 = MonteCarloTree(boardWidth, boardHeight, 10, 2)
    wins, time1, time2 = play_n_games(boardWidth, boardHeight, mcts1, 100, mcts2, 1000, nr)
    print(wins)
    print(f"Time for quick: {time1}")
    print(f"Time for better: {time2}")

heuristicList = [
    None,
    NrPiecesHeuristic(),
    AdjacentPiecesHeuristic(),
    WinHeuristic(),
    GroupsHeuristic(),
    CenterControlHeuristic(),
    ApproximateEnemyHeuristic(),
    HeuristicsList(
        heuristics=np.array([
            WinHeuristic(),
            NrPiecesHeuristic(),
            AdjacentPiecesHeuristic(),
            GroupsHeuristic(),
            CenterControlHeuristic(),
        ]),
        weights=np.array([100000, 50, 25, 10, 5]),
    )
]

def test_heuruistic(nr : int):
    for i in range(len(heuristicList)):
        for j in range(i+1, len(heuristicList)):
            h1 = heuristicList[i]
            h2 = heuristicList[j]
            print(f"Playing {h1} vs {h2}")
            if(h1 is None):
                mcts1 = MonteCarloTree.from_player(5, 5, Player.WHITE)
            else:
                mcts1 = MonteCarloTreeHeuristic.from_player(h1, 5, 5, Player.WHITE)
            mcts2 = MonteCarloTreeHeuristic.from_player(h2, 5, 5, Player.BLACK)
            wins, time1, time2 = play_n_games(5, 5, mcts1, 1000, mcts2, 1000, nr)
            print(wins)
            print(f"Time for {h1}: {time1}")
            print(f"Time for {h2}: {time2}")

if __name__ == "__main__":
    nr = 100  # The same for all to allow easy time comparison
    test_quick_vs_better(nr)
    # test_heuruistic(nr)
    

