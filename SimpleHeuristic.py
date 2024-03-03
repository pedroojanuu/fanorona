from heuristic import Heuristic
from state import State
from board import PlayerEnum
import numpy as np

class SimpleHeuristic(Heuristic):
    def evaluate_board(self, state, player_to_win):
        if state.check_winner() != PlayerEnum.EMPTY:
            return 1 if state.check_winner() == player_to_win else -1
        return 0


def test_simple_heuristic():
    h = SimpleHeuristic()
    s = State()

    board = np.zeros((s.get_board_matrix().shape), dtype=PlayerEnum)
    s.board.board = board   # clear the board
    s.get_board_matrix()[0][0] = PlayerEnum.WHITE
    print(s.get_board_matrix())

    white_eval = h.evaluate_board(s, PlayerEnum.WHITE)
    black_eval = h.evaluate_board(s, PlayerEnum.BLACK)
    print(white_eval, black_eval)
    assert white_eval > 0, f"Expected white won, but got {white_eval}"
    assert black_eval < 0, f"Expected black lost, but got {black_eval}"

if __name__ == "__main__":
    test_simple_heuristic()
