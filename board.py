import pygame
import numpy as np
import math
import enum
from typing import List

class PlayerEnum(enum.Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

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

    def inside_board(self, r: int, c: int):
        return r >= 0 and r < self.height and c >= 0 and c < self.width

    def get_adjacent_aproach(self, r: int, c: int):
        dr = [1, -1, 0, 1, -1, 0, 1, -1]
        dc = [0, 0, 1, 1, 1, -1, -1, -1]

        for i, j in zip(dr, dc):
            r2 = r  + i
            c2 = c  + j
            r3 = r2 + i
            c3 = c2 + j
            if self.inside_board(r2, c2) and self.inside_board(r3, c3):
                yield (r2, c2, r3, c3)

    def get_adjacent_withdrawal(self, r: int, c: int):
        dr = [1, -1, 0, 1, -1, 0, 1, -1]
        dc = [0, 0, 1, 1, 1, -1, -1, -1]

        for i, j in zip(dr, dc):
            r2 = r + i
            c2 = c + j
            r3 = r - i
            c3 = c - j
            if self.inside_board(r2, c2) and self.inside_board(r3, c3):
                yield (r2, c2, r3, c3)

    # def draw(self, screen):
    #     for x in range(self.width):
    #         for y in range(self.height):
    #             pygame.draw.rect(screen, (255, 255, 255), (x*50, y*50, 50, 50), 1)
    #             if self.board[x][y] == 1:
    #                 pygame.draw.circle(screen, (255, 0, 0), (x*50 + 25, y*50 + 25), 20)


if __name__ == '__main__':
    # b = Board()
    c = Board(9, 6)
    c.moves(PlayerEnum.BLACK)

