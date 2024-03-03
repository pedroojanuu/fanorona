from heuristic import Heuristic
from state import State
from board import PlayerEnum
import numpy as np

class CenterControlHeuristic(Heuristic):
    def evaluate_board(self, state, player_to_win):
        rowMiddle = state.get_board_matrix().shape[0] // 2
        colMiddle = state.get_board_matrix().shape[1] // 2
        return 1 if state.board.board[rowMiddle][colMiddle] == player_to_win else -1

def test_center_control_heuristic():
    h = CenterControlHeuristic()
    s = State()

    board = np.zeros((s.get_board_matrix().shape), dtype=PlayerEnum)
    s.board.board = board   # clear the board

    row_center = s.get_board_matrix().shape[0] // 2
    col_center = s.get_board_matrix().shape[1] // 2
    s.get_board_matrix()[row_center][col_center] = PlayerEnum.WHITE
    print(s.get_board_matrix())

    white_eval = h.evaluate_board(s, PlayerEnum.WHITE)
    black_eval = h.evaluate_board(s, PlayerEnum.BLACK)
    print(white_eval, black_eval)
    assert white_eval > 0, f"Expected white advantage, but got {white_eval}"
    assert black_eval < 0, f"Expected black disadvantage, but got {black_eval}"

if __name__ == "__main__":
    test_center_control_heuristic()
