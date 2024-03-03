from position import ADJACENT_RIGHT
from heuristics.heuristic import Heuristic
import numpy as np

class AdjacentPiecesHeuristic(Heuristic):
    def calculate_max_adjacent_pieces(self, board, player):
        pieces = board.get_pieces(player)
        visited = np.zeros(board.shape, dtype=bool)

        max_adjacent = 0

        for (r, c) in ADJACENT_RIGHT:
            for (row, col) in pieces:
                if visited[row][col]:
                    continue
                adjacent = 0
                current_row = row + r
                current_col = col + c
                while board.inside_board(current_row, current_col) and board.board[current_row][current_col] == player:
                    visited[current_row][current_col] = True
                    adjacent += 1
                    current_row += r
                    current_col += c
            max_adjacent = max(max_adjacent, adjacent)
        return max_adjacent

    def evaluate_board(self, state, player_to_win):
        return self.calculate_max_adjacent_pieces(state.board, player_to_win) - self.calculate_max_adjacent_pieces(state.board, opponent_player(player_to_win))
