from heuristic import Heuristic
from board import opponent_player, PlayerEnum
from state import State
from position import ADJACENT_ALL
import numpy as np

class GroupsHeuristic(Heuristic):
    def flood_fill(self, board, row, col, visited, player):
        if board.inside_board(row, col) or visited[row][col] or board.board[row][col] != player:
            return
        visited[row][col] = True
        for r, c in ADJACENT_ALL:
            self.flood_fill(board, row + r, col + c, visited, player)

    def count_groups(self, board, player, visited):
        pieces = board.get_pieces(player)
        groups_count = 0

        for (row, col) in pieces:
            if not visited[row][col]:
                self.flood_fill(board, row, col, visited, player)
                groups_count += 1
        return groups_count        

    def evaluate_board(self, state, player_to_win):
        """
        perform a flood fill algorithm to find the groups of pieces
        count the number of groups of pieces for each player
        return the difference of the number of groups of pieces for each player
        """
        adversary_player = opponent_player(player_to_win)

        visited = np.zeros(state.get_board_matrix().shape, dtype=bool)
        my_groups = self.count_groups(state.board, player_to_win, visited)
        adv_groups = self.count_groups(state.board, adversary_player, visited)

        return my_groups - adv_groups   # better (> 0) if my pieces have more groups

def test_groups_heuristic():
    # TODO: fix test
    h = GroupsHeuristic()
    s = State()

    board = np.zeros((s.get_board_matrix().shape), dtype=PlayerEnum)
    s.board.board = board   # clear the board
    s.get_board_matrix()[0, 0:2] = PlayerEnum.WHITE
    s.get_board_matrix()[1, 0] = PlayerEnum.WHITE
    
    
    s.get_board_matrix()[2, 2:4] = PlayerEnum.BLACK
    
    s.get_board_matrix()[4, 4] = PlayerEnum.BLACK
    s.get_board_matrix()[3, 5] = PlayerEnum.BLACK
    print(s.get_board_matrix())

    white_eval = h.evaluate_board(s, PlayerEnum.WHITE)
    black_eval = h.evaluate_board(s, PlayerEnum.BLACK)
    print(white_eval, black_eval)
    assert white_eval < 0, f"Expected white disadvantage, but got {white_eval}"
    assert black_eval > 0, f"Expected black advantage, but got {black_eval}"

if __name__ == "__main__":
    test_groups_heuristic()
