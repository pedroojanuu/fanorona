import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np

from tests.test import test
from state import State
from player import Player
from game import Game
from game_simulator import GameSimulator
from heuristics.heuristic import Heuristic
from heuristics.nr_pieces_heuristic import NrPiecesHeuristic
from heuristics.adjacent_pieces_heuristic import AdjacentPiecesHeuristic
from heuristics.heuristics_list import HeuristicsList
from heuristics.win_heuristic import WinHeuristic
from heuristics.groups_heuristic import GroupsHeuristic
from heuristics.center_control_heuristic import CenterControlHeuristic
from minimax import execute_minimax_move, execute_random_move


def run_n_times(ai_white, ai_black, nr: int):
    wins = {}
    for _ in range(nr):
        game = GameSimulator()
        try:
            winner = game.run_ais(ai_white, ai_black, log_states=False)
            wins[winner] = wins.get(winner, 0) + 1
        except Exception as e:
            print(e)
            game.state.draw()
            print(game.state.get_available_moves())
            raise e
    return wins


def test_heuristic(ai_white, ai_black, nr: int):
    wins = run_n_times(ai_white, ai_black, nr)
    print(wins)


@test
def test_random_vs_random(nr: int):
    test_heuristic(execute_random_move, execute_random_move, nr)


@test
def test_random_vs_pieces(nr: int):
    test_heuristic(
        execute_random_move,
        execute_minimax_move(NrPiecesHeuristic().evaluate_board, 2),
        nr=nr,
    )


@test
def test_win_vs_random(nr: int):
    test_heuristic(
        execute_minimax_move(WinHeuristic().evaluate_board, 2),
        execute_random_move,
        nr=nr,
    )


@test
def test_win_pieces_vs_random(nr: int):
    test_heuristic(
        execute_minimax_move(
            HeuristicsList(
                [WinHeuristic(), NrPiecesHeuristic()], [10000, 1]
            ).evaluate_board,  # does not make the most sense since WinHeuristic is based on the nr of pieces on the board
            2,
        ),
        execute_random_move,
        nr=nr,
    )


@test
def test_win_adjacent_vs_random(nr: int):
    test_heuristic(
        execute_minimax_move(
            HeuristicsList(  # an heuristic like this is not very good (it is not considering the number of pieces)
                [WinHeuristic(), AdjacentPiecesHeuristic()], [10000, 1]
            ).evaluate_board,
            2,
        ),
        execute_random_move,
        nr=nr,
    )


@test
def test_win_groups_vs_random(nr: int):
    test_heuristic(
        execute_minimax_move(
            HeuristicsList(
                [WinHeuristic(), GroupsHeuristic()], [10000, 1]
            ).evaluate_board,
            2,
        ),
        execute_random_move,
        nr=nr,
    )


@test
def test_win_center_vs_random(nr: int):
    test_heuristic(
        execute_minimax_move(
            HeuristicsList(
                [WinHeuristic(), CenterControlHeuristic()], [10000, 1]
            ).evaluate_board,
            2,
        ),
        execute_random_move,
        nr=nr,
    )


@test
def test_win_center_groups_vs_random(nr: int):
    test_heuristic(
        execute_minimax_move(
            HeuristicsList(
                [WinHeuristic(), CenterControlHeuristic(), GroupsHeuristic()],
                [10000, 1, 1],
            ).evaluate_board,
            2,
        ),
        execute_random_move,
        nr=nr,
    )


@test
def test_pieces_adjacent_groups_vs_random(nr: int):
    test_heuristic(
        execute_minimax_move(
            HeuristicsList(
                [
                    NrPiecesHeuristic(),
                    AdjacentPiecesHeuristic(),
                    GroupsHeuristic(),
                ],
                [10, 2, 1],
            ).evaluate_board,
            2,
        ),
        execute_random_move,
        nr=nr,
    )


@test
def test_different_weights_pieces_adjacent_groups(nr: int):
    test_heuristic(
        execute_minimax_move(
            HeuristicsList(
                [
                    NrPiecesHeuristic(),
                    AdjacentPiecesHeuristic(),
                    GroupsHeuristic(),
                ],
                [100, 2, 1],
            ).evaluate_board,
            2,
        ),
        execute_minimax_move(
            HeuristicsList(
                [
                    NrPiecesHeuristic(),
                    AdjacentPiecesHeuristic(),
                    GroupsHeuristic(),
                ],
                [10, 2, 1],
            ).evaluate_board,
            2,
        ),
        nr=nr,
    )


if __name__ == "__main__":
    nr = 100  # The same for all to allow easy time comparison
    test_random_vs_random(nr)

    test_random_vs_pieces(nr)
    test_win_vs_random(nr)
    test_win_pieces_vs_random(nr)
    test_win_adjacent_vs_random(nr)
    test_win_groups_vs_random(nr)
    test_win_center_vs_random(nr)
    test_pieces_adjacent_groups_vs_random(nr)

    test_different_weights_pieces_adjacent_groups(nr)
