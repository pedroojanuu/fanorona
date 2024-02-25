import pygame
import numpy as np
import math
import enum
from typing import List

class PlayerEnum(enum.Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

class Game:
    def __init__(self):
        self.board = Board()
        self.player = PlayerEnum.BLACK
    
    def change_player(self):
        self.player = opponent_player(self.player)

    def play(self):
        pass

def opponent_player(player):
    if player == PlayerEnum.BLACK:
        return PlayerEnum.WHITE
    return PlayerEnum.BLACK

class Board:
    def __init__(self, width: int = 9, height: int = 5):
        self.width = width
        self.height = height
        self.board = np.zeros((self.height, self.width), dtype=PlayerEnum)

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

        print(self.board)


    def get_adjacent(self, r: int, c: int):
        # # #
        # X #
        # # #
        dr = [1, 1, 0, 0, -1, -1]
        dc = [0, 1, 1, -1, 0, -1]



    def moves(self, player: PlayerEnum):
        moves = []
        pieces = np.argwhere(self.board == player)
        for [r, c] in pieces:
            for r2, c2, r3, c3 in get_adjacent(r, c):
                if self.board[r2][c2] == PlayerEnum.EMPTY and self.board[r3][c3] == opponent_player(player):
                    moves.append((r, c, r2, c2))

            
        
        # Capturing moves
        if moves:
            return []

        # Non-capturing moves
        
        return []

    # def draw(self, screen):
    #     for x in range(self.width):
    #         for y in range(self.height):
    #             pygame.draw.rect(screen, (255, 255, 255), (x*50, y*50, 50, 50), 1)
    #             if self.board[x][y] == 1:
    #                 pygame.draw.circle(screen, (255, 0, 0), (x*50 + 25, y*50 + 25), 20)




    def check_winner(self):
        if np.count_nonzero(self.board == 1) == 0:
            return PlayerEnum.WHITE
        if np.count_nonzero(self.board == 2) == 0:
            return PlayerEnum.BLACK
        return PlayerEnum.EMPTY


if __name__ == '__main__':
    # b = Board()
    c = Board(9, 6)
    c.moves(PlayerEnum.BLACK)

