if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from heuristics.heuristic import Heuristic
from state import State, PlayerEnum
from board import Board, opponent_player
import numpy as np
from enum import Enum

from heuristics.groups_heuristic import GroupsHeuristic, test_groups_heuristic
from heuristics.center_control_heuristic import CenterControlHeuristic, test_center_control_heuristic
from heuristics.win_heuristic import WinHeuristic, test_win_heuristic
from heuristics.adjacent_pieces_heuristic import AdjacentPiecesHeuristic, test_adjacent_pieces_heuristic
from heuristics.nr_pieces_heuristic import NrPiecesHeuristic, test_nr_pieces_heuristic


class HeuristicsList(Heuristic):
    def __init__(self, heuristics, weights):
        self.heuristics = heuristics
        self.weights = weights

    def evaluate_board(self, state, player_to_win):
        map_func = lambda h, w: h.evaluate_board(state, player_to_win) * w
        map_list = np.vectorize(map_func)(self.heuristics, self.weights)
        print(map_list)
        return sum(map_list)


def test_heuristic_list():
    s = State()
    h = HeuristicsList(
        heuristics=np.array([
            WinHeuristic(),
            NrPiecesHeuristic(),
            AdjacentPiecesHeuristic(),
            GroupsHeuristic(),
            CenterControlHeuristic(),
        ]),
        weights=np.array([100000, 50, 25, 10, 5]),
    )

    s.get_board_matrix().fill(PlayerEnum.EMPTY)  # clear the board

    s.get_board_matrix()[0,0:5] = PlayerEnum.WHITE
    s.get_board_matrix()[1,0:4] = PlayerEnum.BLACK

    print(s.get_board_matrix())
    white_eval = h.evaluate_board(s, PlayerEnum.WHITE)
    black_eval = h.evaluate_board(s, PlayerEnum.BLACK)
    print(white_eval, black_eval)
    assert white_eval > 0, f"Expected white advantage, but got {white_eval}"
    assert black_eval < 0, f"Expected black disadvantage, but got {black_eval}"


if __name__ == "__main__":
    test_win_heuristic()
    test_nr_pieces_heuristic()
    test_adjacent_pieces_heuristic()
    test_groups_heuristic()
    test_center_control_heuristic()
    test_heuristic_list()
