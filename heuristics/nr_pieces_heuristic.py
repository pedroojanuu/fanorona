if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from heuristics.heuristic import Heuristic
from board import opponent_player
from state import State
from board import PlayerEnum

class NrPiecesHeuristic(Heuristic):
    def evaluate_board(self, state, player_to_win):
        adversary = opponent_player(player_to_win)
        return len(state.board.get_pieces(player_to_win)) - len(state.board.get_pieces(adversary))

def test_nr_pieces_heuristic():
    s = State()
    h = NrPiecesHeuristic()

    s.get_board_matrix().fill(PlayerEnum.EMPTY) # clear the board

    s.get_board_matrix()[0][0:5] = PlayerEnum.WHITE
    s.get_board_matrix()[1][0:4] = PlayerEnum.BLACK

    print(s.get_board_matrix())
    white_eval = h.evaluate_board(s, PlayerEnum.WHITE)
    black_eval = h.evaluate_board(s, PlayerEnum.BLACK)
    print(white_eval, black_eval)
    assert white_eval > 0, f"Expected white advantage, but got {white_eval}"
    assert black_eval < 0, f"Expected black disadvantage, but got {black_eval}"

if __name__ == "__main__":
    test_nr_pieces_heuristic()
