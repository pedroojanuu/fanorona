from heuristics.heuristic import Heuristic
from player import Player
from state import State
from board import Player
import numpy as np

class ApproximateEnemyHeuristic(Heuristic):
    """
    This heuristic evaluates the board by reducing the distance from my pieces to the enemy pieces
    The heuristic returns the negative sum of the minimum distances for each of my pieces.

    It should never be used alone, but as part of a list of heuristics. And it should always have a relatively lower weight.
    """
    def evaluate_board(self, state, player_to_win):
        adversary = Player.opponent_player(player_to_win)
        my_pieces = state.board.get_pieces(player_to_win)
        enemy_pieces = state.board.get_pieces(adversary)
        if len(my_pieces) == 0 or len(enemy_pieces) == 0:
            return 0

        distances = np.linalg.norm(my_pieces[:, None] - enemy_pieces, axis=2)

        min_distances = np.min(distances, axis=1)

        # Return the negative sum of the minimum distances for each of my pieces
        return -np.sum(min_distances) / len(my_pieces)

 
def test_approximate_enemy_heuristic():
    s = State()
    h = ApproximateEnemyHeuristic()

    s.get_board_matrix().fill(Player.EMPTY)  # clear the board

    s.get_board_matrix()[0][0:5] = Player.WHITE

    s.get_board_matrix()[3][0:4] = Player.BLACK

    print(s.get_board_matrix())
    white_eval = h.evaluate_board(s, Player.WHITE)
    black_eval = h.evaluate_board(s, Player.BLACK)
    print(white_eval, black_eval)
    assert white_eval < 0, f"Expected negative value, but got {white_eval}"
    assert black_eval < 0, f"Expected negative value, but got {black_eval}"

if __name__ == "__main__":
    test_approximate_enemy_heuristic()
