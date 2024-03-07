# import pygame
import numpy as np
import math
from move import Move, TypeOfMove
from typing import List
from adjacent_positions import ADJACENT_4, ADJACENT_ALL
from player import Player

class Board:
    def __init__(self, width: int = 9, height: int = 5):
        self.width = width
        self.height = height
        self.board = np.zeros((self.height, self.width), dtype=Player)
        self.board.fill(Player.EMPTY)

        halfHeight = (self.height - 1) // 2
        halfWidth = (self.width - 1) // 2
        for row in range(halfHeight):
            for col in range(self.width):
                self.board[row][col] = Player.BLACK
                self.board[self.height - 1 - row][col] = Player.WHITE

        if self.height % 2 == 0:
            for col in range(0, halfWidth, 2):
                self.board[halfHeight][col] = Player.BLACK
                self.board[halfHeight + 1][col] = Player.BLACK

                self.board[halfHeight][width - col - 1] = Player.WHITE
                self.board[halfHeight + 1][width - col - 1] = Player.WHITE

            for col in range(1, halfWidth, 2):
                self.board[halfHeight][col] = Player.WHITE
                self.board[halfHeight + 1][col] = Player.WHITE

                self.board[halfHeight][width - col - 1] = Player.BLACK
                self.board[halfHeight + 1][width - col - 1] = Player.BLACK
        else:
            for col in range(0, halfWidth, 2):
                self.board[halfHeight][col] = Player.BLACK
                self.board[halfHeight][width - col - 1] = Player.WHITE
            for col in range(1, halfWidth, 2):
                self.board[halfHeight][col] = Player.WHITE
                self.board[halfHeight][width - col - 1] = Player.BLACK

    def inside_board(self, r: int, c: int):
        return r >= 0 and r < self.height and c >= 0 and c < self.width

    def can_move_in_diagonal(self, r: int, c: int):
        return (r + c) % 2 == 0
    def get_pieces(self, player: Player):
        return np.argwhere(self.board == player)

    def get_adjacent_aproach(self, r: int, c: int):
        diff = ADJACENT_ALL if self.can_move_in_diagonal(r, c) else ADJACENT_4
        # if self.can_move_in_diagonal(r, c):
            
        #     dr = [1, -1, 0, 1, -1, 0, 1, -1]
        #     dc = [0, 0, 1, 1, 1, -1, -1, -1]
        # else:
        #     dr = [1, -1, 0,  0]
        #     dc = [0,  0, 1, -1]

        for i, j in diff:
            r2 = r  + i
            c2 = c  + j
            r3 = r2 + i
            c3 = c2 + j
            if self.inside_board(r2, c2) and self.inside_board(r3, c3):
                yield (r2, c2, r3, c3)

    def get_adjacent_withdrawal(self, r: int, c: int):
        diff = ADJACENT_ALL if self.can_move_in_diagonal(r, c) else ADJACENT_4
        # if self.can_move_in_diagonal(r, c):
        #     dr = [1, -1, 0, 1, -1, 0, 1, -1]
        #     dc = [0, 0, 1, 1, 1, -1, -1, -1]
        # else:
        #     dr = [1, -1, 0,  0]
        #     dc = [0,  0, 1, -1]

        for i, j in diff:
            r2 = r + i
            c2 = c + j
            r3 = r - i
            c3 = c - j
            if self.inside_board(r2, c2) and self.inside_board(r3, c3):
                yield (r2, c2, r3, c3)

    def get_adjacent_free(self, r: int, c: int):
        diff = ADJACENT_ALL if self.can_move_in_diagonal(r, c) else ADJACENT_4
        # if self.can_move_in_diagonal(r, c):
        #     dr = [1, -1, 0, 1, -1, 0, 1, -1]
        #     dc = [0, 0, 1, 1, 1, -1, -1, -1]
        # else:
        #     dr = [1, -1, 0,  0]
        #     dc = [0,  0, 1, -1]

        for i, j in diff:
            r2 = r + i
            c2 = c + j
            if self.inside_board(r2, c2):
                yield (r2, c2)

    def get_all_moves(self, player: Player):
        moves = []
        pieces = self.get_pieces(player)
        for [r, c] in pieces:
            for r2, c2, r3, c3 in self.get_adjacent_aproach(r, c):
                if self.board[r2][c2] == Player.EMPTY and self.board[r3][c3] == Player.opponent_player(player):
                    moves.append(Move(r, c, r2, c2, TypeOfMove.APPROACH))
                    
            for r2, c2, r3, c3 in self.get_adjacent_withdrawal(r, c):
                if self.board[r2][c2] == Player.EMPTY and self.board[r3][c3] == Player.opponent_player(player):
                    moves.append(Move(r, c, r2, c2, TypeOfMove.WITHDRAWAL))

        if moves == []:
            for [r, c] in pieces:
                for r2, c2 in self.get_adjacent_free(r, c):
                    if self.board[r2][c2] == Player.EMPTY:
                        moves.append(Move(r, c, r2, c2, TypeOfMove.FREE))
                    
        return moves
    
    def get_tile_moves(self, r: int, c: int):
        moves = []
        for r2, c2, r3, c3 in self.get_adjacent_aproach(r, c):
            if self.board[r2][c2] == Player.EMPTY and self.board[r3][c3] == Player.opponent_player(self.board[r][c]):
                moves.append(Move(r, c, r2, c2, TypeOfMove.APPROACH))
                
        for r2, c2, r3, c3 in self.get_adjacent_withdrawal(r, c):
            if self.board[r2][c2] == Player.EMPTY and self.board[r3][c3] == Player.opponent_player(self.board[r][c]):
                moves.append(Move(r, c, r2, c2, TypeOfMove.WITHDRAWAL))
                    
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

