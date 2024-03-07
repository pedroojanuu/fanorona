if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np

from heuristics.heuristic import Heuristic
from state import State
from board import Player


class CenterControlHeuristic(Heuristic):
    def evaluate_board(self, state, player_to_win):
        rowMiddle = state.get_board_matrix().shape[0] // 2
        colMiddle = state.get_board_matrix().shape[1] // 2
        valueAtMiddle = state.get_board_matrix()[rowMiddle][colMiddle]  # lacks even/odd check
        if valueAtMiddle == Player.EMPTY:
            return 0
        return 1 if valueAtMiddle == player_to_win else -1

def test_center_control_heuristic():
    h = CenterControlHeuristic()
    s = State()

    s.get_board_matrix().fill(Player.BLACK) # fill with black pieces

    row_center = s.get_board_matrix().shape[0] // 2
    col_center = s.get_board_matrix().shape[1] // 2
    s.get_board_matrix()[row_center][col_center] = Player.WHITE
    print(s.get_board_matrix())

    white_eval = h.evaluate_board(s, Player.WHITE)
    black_eval = h.evaluate_board(s, Player.BLACK)
    print(white_eval, black_eval)
    assert white_eval > 0, f"Expected white advantage, but got {white_eval}"
    assert black_eval < 0, f"Expected black disadvantage, but got {black_eval}"

if __name__ == "__main__":
    test_center_control_heuristic()
