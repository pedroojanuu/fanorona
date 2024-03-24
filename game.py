import pygame
from state import State
from player import Player
from enum import Enum
from typing import Callable
import random

from heuristics.groups_heuristic import GroupsHeuristic
from heuristics.center_control_heuristic import CenterControlHeuristic
from heuristics.win_heuristic import WinHeuristic
from heuristics.adjacent_pieces_heuristic import AdjacentPiecesHeuristic
from heuristics.nr_pieces_heuristic import NrPiecesHeuristic
from heuristics.heuristics_list import HeuristicsList

from monte_carlo_tree_search.tree import MonteCarloTree


class WindowState(Enum):
    BOARD_SIZE_SEL = 0
    WHITE_MODE_SEL = 1
    BLACK_MODE_SEL = 2
    PLAYING = 3
    GAME_OVER = 4

class PlayerModes(Enum):
    HUMAN = 0
    MINIMAX_WIN = 1
    MINIMAX_NR_PIECES = 2
    MINIMAX_ADJACENT_PIECES = 3
    MINIMAX_GROUPS = 4
    MINIMAX_CENTER_CONTROL = 5
    MCTS_QUICK = 6
    MCTS_BETTER = 7


class Game:
    def __init__(self):
        pygame.init()
        self.canvas = pygame.display.set_mode((350, 420))
        self.canvas.fill((184, 59, 50)) # Background
        self.font = pygame.font.Font('freesansbold.ttf', 15)
        pygame.display.set_caption("Fanorona")
        pygame.display.update()

        self.frame_rate = 30
        self.frame_time_counter = 0

        self.window_state = WindowState.BOARD_SIZE_SEL
        self.selected_piece = None

        self.width = None
        self.height = None

        self.game_state = None
        self.winner = Player.EMPTY
        self.white_mode = None
        self.black_mode = None
        self.available_moves = None

        self.white_alg = None
        self.black_alg = None

    def size_sel(self):
        for i in range(5, 11):
            for j in range(5, 11):
                text = self.font.render(f"{i}*{j}", True, (0,0,0), (255,255,255))
                textRect = text.get_rect()
                textRect.center = ((i-4)*50, (j-4)*60)
                self.canvas.blit(text, textRect)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = ((x+25) // 50) + 4
                row = ((y+25) // 60) + 4
                
                if 5 <= col <= 10 and 5 <= row <= 10:
                    self.width = col
                    self.height = row
                    self.canvas = pygame.display.set_mode((self.width*70, self.height*70 + 15))
                    self.game_state = State(self.width, self.height)
                    self.available_moves = self.game_state.get_available_moves()
                    self.window_state = WindowState.WHITE_MODE_SEL
                    return

        pygame.display.update()
    
    def mode_sel(self):
        # TODO

        # temp
        self.window_state = WindowState.PLAYING
        self.white_mode = PlayerModes.HUMAN
        self.black_mode = PlayerModes.HUMAN
        # temp

        if self.white_mode == PlayerModes.MCTS_QUICK:
            self.white_alg = MonteCarloTree(self.game_state.board.width, self.game_state.board.height)
            self.white_alg.state = self.game_state

        return

    def board(self):
        self.canvas.fill((184, 59, 50)) # Background

        # Static elements
        for i in range(self.width):
            pygame.draw.line(self.canvas, (255,255,255), (70*i+35, 35), (70*i+35, 70*self.height-35), 2)
        for i in range(self.height):
            pygame.draw.line(self.canvas, (255,255,255), (35, 70*i+35), (70*self.width-35, 70*i+35), 2)
        for i in range(self.width-1):
            for j in range(self.height-1):
                if (i+j)%2 == 0:
                    pygame.draw.line(self.canvas, (255,255,255), (70*i+35, 70*j+35), (70*i+105, 70*j+105), 2)
                else:
                    pygame.draw.line(self.canvas, (255,255,255), (70*i+105, 70*j+35), (70*i+35, 70*j+105), 2)

        for row in range(self.height):
            for col in range(self.width):
                if self.game_state.board.board[row][col] == Player.WHITE:
                    pygame.draw.circle(self.canvas, (255,255,255), (70*col+35, 70*row+35), 30)
                elif self.game_state.board.board[row][col] == Player.BLACK:
                    pygame.draw.circle(self.canvas, (0,0,0), (70*col+35, 70*row+35), 30)
        
        if self.selected_piece != None:
            pygame.draw.circle(self.canvas, (235,235,52), (70*self.selected_piece[1]+35, 70*self.selected_piece[0]+35), 30, 3)
        
        if self.game_state.player == Player.BLACK:
            text = self.font.render("Vez das pretas", True, (0,0,0), (184,59,50))
        elif self.game_state.player == Player.WHITE:
            text = self.font.render("Vez das brancas", True, (255,255,255), (184,59,50))
        textRect = text.get_rect()
        textRect.center = (100, self.height*70+7)
        self.canvas.blit(text, textRect)

        if (self.white_mode == PlayerModes.HUMAN and self.game_state.player == Player.WHITE) or (self.black_mode == PlayerModes.HUMAN and self.game_state.player == Player.BLACK):
            for move in self.available_moves:
                if self.selected_piece == (move.row_origin, move.col_origin):
                    pygame.draw.circle(self.canvas, (0,255,0), (70*move.col_destination+35, 70*move.row_destination+35), 30, 3)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // 70
                    row = y // 70
                    if self.game_state.board.board[row][col] == self.game_state.player:
                        self.selected_piece = (row, col)
                    elif self.game_state.board.board[row][col] == Player.EMPTY:
                        for move in self.available_moves:
                            if self.selected_piece == (move.row_origin, move.col_origin) and (row, col) == (move.row_destination, move.col_destination):
                                self.game_state.execute_move(move)
                                self.available_moves = self.game_state.get_available_moves()
                                self.selected_piece = None
                                pygame.display.update()
                                return
        elif self.game_state.player == Player.WHITE:
            if self.white_mode == PlayerModes.MCTS_QUICK:
                self.white_alg.state = self.game_state

        pygame.display.update()
    
    def game_over(self):
        self.canvas.fill((184, 59, 50)) # Background

        if self.winner == Player.BLACK:
            text = self.font.render("Pretas vencem!", True, (0,0,0), (184,59,50))
        elif self.winner == Player.WHITE:
            text = self.font.render("Brancas vencem!", True, (255,255,255), (184,59,50))
        textRect = text.get_rect()
        textRect.center = (self.width*35, self.height*35)
        self.canvas.blit(text, textRect)

        text = self.font.render("Obrigado por jogar Fanorona!", True, (0,0,0), (184,59,50))
        textRect = text.get_rect()
        textRect.center = (self.width*35, self.height*35+30)
        self.canvas.blit(text, textRect)

        text = self.font.render("Félix Martins, Pedro Lima e Pedro Januário", True, (0,0,0), (184,59,50))
        textRect = text.get_rect()
        textRect.center = (self.width*35, self.height*35+50)
        self.canvas.blit(text, textRect)

        text = self.font.render("Pressione ESC ou feche a janela para sair", True, (0,0,0), (184,59,50))
        textRect = text.get_rect()
        textRect.center = (self.width*35, self.height*35+90)
        self.canvas.blit(text, textRect)

        pygame.display.update()

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return
            if self.window_state == WindowState.PLAYING:
                self.winner = self.game_state.check_winner()
                if self.winner != Player.EMPTY:
                    self.window_state = WindowState.GAME_OVER
                    continue
                self.board()
            elif self.window_state == WindowState.BOARD_SIZE_SEL:
                self.size_sel()
            elif self.window_state == WindowState.WHITE_MODE_SEL or self.window_state == WindowState.BLACK_MODE_SEL:
                self.mode_sel()
            elif self.window_state == WindowState.GAME_OVER:
                self.game_over()

if __name__ == '__main__':
    game = Game()
    game.play()
