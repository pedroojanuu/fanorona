# import pygame
import numpy as np
import math
from enum import Enum
from move import Move, TypeOfMove
from typing import List

class PlayerEnum(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

def opponent_player(player):
    if player == PlayerEnum.BLACK:
        return PlayerEnum.WHITE
    return PlayerEnum.BLACK

class Board:
    def __init__(self, width: int = 9, height: int = 5):
        self.width = width
        self.height = height
        self.board = np.zeros((self.height, self.width), dtype=PlayerEnum)
        self.board.fill(PlayerEnum.EMPTY)

        halfHeight = (self.height - 1) // 2
        halfWidth = (self.width - 1) // 2
        for row in range(halfHeight):
            for col in range(self.width):
                self.board[row][col] = PlayerEnum.BLACK
                self.board[self.height - 1 - row][col] = PlayerEnum.WHITE

        if self.height % 2 == 0:
            for col in range(0, halfWidth, 2):
                self.board[halfHeight][col] = PlayerEnum.BLACK
                self.board[halfHeight + 1][col] = PlayerEnum.BLACK

                self.board[halfHeight][width - col - 1] = PlayerEnum.WHITE
                self.board[halfHeight + 1][width - col - 1] = PlayerEnum.WHITE

            for col in range(1, halfWidth, 2):
                self.board[halfHeight][col] = PlayerEnum.WHITE
                self.board[halfHeight + 1][col] = PlayerEnum.WHITE

                self.board[halfHeight][width - col - 1] = PlayerEnum.BLACK
                self.board[halfHeight + 1][width - col - 1] = PlayerEnum.BLACK
        else:
            for col in range(0, halfWidth, 2):
                self.board[halfHeight][col] = PlayerEnum.BLACK
                self.board[halfHeight][width - col - 1] = PlayerEnum.WHITE
            for col in range(1, halfWidth, 2):
                self.board[halfHeight][col] = PlayerEnum.WHITE
                self.board[halfHeight][width - col - 1] = PlayerEnum.BLACK

    def inside_board(self, r: int, c: int):
        return r >= 0 and r < self.height and c >= 0 and c < self.width

    def can_move_in_diagonal(self, r: int, c: int):
        return (r + c) % 2 == 0
    def get_pieces(self, player: PlayerEnum):
        return np.argwhere(self.board == player)

    def get_adjacent_aproach(self, r: int, c: int):
        if self.can_move_in_diagonal(r, c):
            dr = [1, -1, 0, 1, -1, 0, 1, -1]
            dc = [0, 0, 1, 1, 1, -1, -1, -1]
        else:
            dr = [1, -1, 0,  0]
            dc = [0,  0, 1, -1]

        for i, j in zip(dr, dc):
            r2 = r  + i
            c2 = c  + j
            r3 = r2 + i
            c3 = c2 + j
            if self.inside_board(r2, c2) and self.inside_board(r3, c3):
                yield (r2, c2, r3, c3)

    def get_adjacent_withdrawal(self, r: int, c: int):
        if self.can_move_in_diagonal(r, c):
            dr = [1, -1, 0, 1, -1, 0, 1, -1]
            dc = [0, 0, 1, 1, 1, -1, -1, -1]
        else:
            dr = [1, -1, 0,  0]
            dc = [0,  0, 1, -1]

        for i, j in zip(dr, dc):
            r2 = r + i
            c2 = c + j
            r3 = r - i
            c3 = c - j
            if self.inside_board(r2, c2) and self.inside_board(r3, c3):
                yield (r2, c2, r3, c3)

    def get_adjacent_free(self, r: int, c: int):
        if self.can_move_in_diagonal(r, c):
            dr = [1, -1, 0, 1, -1, 0, 1, -1]
            dc = [0, 0, 1, 1, 1, -1, -1, -1]
        else:
            dr = [1, -1, 0,  0]
            dc = [0,  0, 1, -1]

        for i, j in zip(dr, dc):
            r2 = r + i
            c2 = c + j
            if self.inside_board(r2, c2):
                yield (r2, c2)

    def moves(self, player: PlayerEnum):
        moves = []
        pieces = self.get_pieces(player)
        for [r, c] in pieces:
            for r2, c2, r3, c3 in self.get_adjacent_aproach(r, c):
                if self.board[r2][c2] == PlayerEnum.EMPTY and self.board[r3][c3] == opponent_player(player):
                    moves.append(Move(r, c, r2, c2, TypeOfMove.APPROACH))
                    
            for r2, c2, r3, c3 in self.get_adjacent_withdrawal(r, c):
                if self.board[r2][c2] == PlayerEnum.EMPTY and self.board[r3][c3] == opponent_player(player):
                    moves.append(Move(r, c, r2, c2, TypeOfMove.WITHDRAWAL))

        if moves == []:
            for [r, c] in pieces:
                for r2, c2 in self.get_adjacent_free(r, c):
                    if self.board[r2][c2] == PlayerEnum.EMPTY:
                        moves.append(Move(r, c, r2, c2, TypeOfMove.FREE))
                    
        return moves
    
    def get_tile_moves(self, r: int, c: int):
        moves = []
        for r2, c2, r3, c3 in self.get_adjacent_aproach(r, c):
            if self.board[r2][c2] == PlayerEnum.EMPTY and self.board[r3][c3] == opponent_player(self.board[r][c]):
                moves.append(Move(r, c, r2, c2, TypeOfMove.APPROACH))
                
        for r2, c2, r3, c3 in self.get_adjacent_withdrawal(r, c):
            if self.board[r2][c2] == PlayerEnum.EMPTY and self.board[r3][c3] == opponent_player(self.board[r][c]):
                moves.append(Move(r, c, r2, c2, TypeOfMove.WITHDRAWAL))
                    
        return moves

    def set_place(self, r: int, c: int, player: PlayerEnum):
        self.board[r][c] = player

    def get_place(self, r: int, c: int):
        return self.board[r][c]

    def draw(self):
        print(self.board)

if __name__ == '__main__':
    # b = Board()
    c = Board(9, 6)
    c.moves(PlayerEnum.BLACK)

