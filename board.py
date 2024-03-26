
# import pygame
import numpy as np
import math
from typing import List

from adjacent_positions import ADJACENT_4, ADJACENT_ALL
from player import Player
from moves.approach_move import ApproachMove
from moves.withdrawal_move import WithdrawalMove
from moves.free_move import FreeMove


class Board:
    def __init__(self, width: int = 9, height: int = 5):
        self.width = width
        self.height = height
        self.board = np.zeros((self.height, self.width), dtype=Player)
        self.board.fill(Player.EMPTY)

        halfHeight = (self.height - 1) // 2
        halfWidth = (self.width - 1) // 2

        self.num_pieces = 0
        for row in range(halfHeight):
            for col in range(self.width):
                self.board[row][col] = Player.BLACK
                self.board[self.height - 1 - row][col] = Player.WHITE
                self.num_pieces += 1

        if self.height % 2 == 0:
            for col in range(0, halfWidth, 2):
                self.num_pieces += 2
                self.board[halfHeight][col] = Player.BLACK
                self.board[halfHeight + 1][col] = Player.BLACK

                self.board[halfHeight][width - col - 1] = Player.WHITE
                self.board[halfHeight + 1][width - col - 1] = Player.WHITE

            for col in range(1, halfWidth, 2):
                self.num_pieces += 2
                self.board[halfHeight][col] = Player.WHITE
                self.board[halfHeight + 1][col] = Player.WHITE

                self.board[halfHeight][width - col - 1] = Player.BLACK
                self.board[halfHeight + 1][width - col - 1] = Player.BLACK
        else:
            for col in range(0, halfWidth, 2):
                self.num_pieces += 1
                self.board[halfHeight][col] = Player.BLACK
                self.board[halfHeight][width - col - 1] = Player.WHITE
            for col in range(1, halfWidth, 2):
                self.num_pieces += 1
                self.board[halfHeight][col] = Player.WHITE
                self.board[halfHeight][width - col - 1] = Player.BLACK

    def inside_board(self, r: int, c: int):
        return r >= 0 and r < self.height and c >= 0 and c < self.width

    def can_move_in_diagonal(self, r: int, c: int):
        return (r + c) % 2 == 0

    def get_pieces(self, player: Player) -> list[list[int, int]]:
        return np.argwhere(self.board == player)

    def get_adjacent_aproach(self, r: int, c: int):
        diff = ADJACENT_ALL if self.can_move_in_diagonal(r, c) else ADJACENT_4

        for dr, dc in diff:
            r2 = r  + dr
            c2 = c  + dc
            r3 = r2 + dr
            c3 = c2 + dc
            if self.inside_board(r2, c2) and self.inside_board(r3, c3):
                yield (r2, c2, r3, c3)

    def get_adjacent_withdrawal(self, r: int, c: int):
        diff = ADJACENT_ALL if self.can_move_in_diagonal(r, c) else ADJACENT_4

        for dr, dc in diff:
            r2 = r + dr
            c2 = c + dc
            r3 = r - dr
            c3 = c - dc
            if self.inside_board(r2, c2) and self.inside_board(r3, c3):
                yield (r2, c2, r3, c3)

    def get_adjacent_free(self, r: int, c: int):
        diff = ADJACENT_ALL if self.can_move_in_diagonal(r, c) else ADJACENT_4

        for dr, dc in diff:
            r2 = r + dr
            c2 = c + dc
            if self.inside_board(r2, c2):
                yield (r2, c2)

    def get_all_moves(self, player: Player):
        moves = []
        pieces = self.get_pieces(player)
        opponent = Player.opponent_player(player)
        for [r, c] in pieces:
            for r2, c2, r3, c3 in self.get_adjacent_aproach(r, c):
                if self.board[r2][c2] == Player.EMPTY and self.board[r3][c3] == opponent:
                    moves.append(ApproachMove(r, c, r2, c2))

            for r2, c2, r3, c3 in self.get_adjacent_withdrawal(r, c):
                if self.board[r2][c2] == Player.EMPTY and self.board[r3][c3] == opponent:
                    moves.append(WithdrawalMove(r, c, r2, c2))

        if moves == []:
            for [r, c] in pieces:
                for r2, c2 in self.get_adjacent_free(r, c):
                    if self.board[r2][c2] == Player.EMPTY:
                        moves.append(FreeMove(r, c, r2, c2))

        return moves
    
    def get_tile_moves(self, r: int, c: int):
        moves = []
        opponent = Player.opponent_player(self.board[r][c])
        for r2, c2, r3, c3 in self.get_adjacent_aproach(r, c):
            if self.board[r2][c2] == Player.EMPTY and self.board[r3][c3] == opponent:
                moves.append(ApproachMove(r, c, r2, c2))

        for r2, c2, r3, c3 in self.get_adjacent_withdrawal(r, c):
            if self.board[r2][c2] == Player.EMPTY and self.board[r3][c3] == opponent:
                moves.append(WithdrawalMove(r, c, r2, c2))

        return moves

    def set_place(self, r: int, c: int, player: Player):
        self.board[r][c] = player

    def get_place(self, r: int, c: int):
        return self.board[r][c]

    def draw(self):
        print(self.board)

if __name__ == '__main__':
    # b = Board()
    c = Board(9, 6)
    print(c.get_all_moves(Player.WHITE))

