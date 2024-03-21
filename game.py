from time import sleep
import pygame
from state import State
from player import Player
from enum import Enum

class WindowState(Enum):
    BOARD_SIZE_SEL = 0
    WHITE_MODE_SEL = 1
    BLACK_MODE_SEL = 2
    PLAYING = 3
    GAME_OVER = 4

class Game:
    def __init__(self):
        pygame.init()
        self.canvas = pygame.display.set_mode((350, 420))
        self.canvas.fill((184, 59, 50)) # Background
        self.font = pygame.font.Font('freesansbold.ttf', 15)
        pygame.display.set_caption("Fanorona")
        pygame.display.update()

        self.window_state = WindowState.GAME_OVER # MUDAR PARA BOARD_SIZE_SEL !!!!

        self.selected_tile = None
                
        self.width = None
        self.height = None

        self.state = None
        self.winner = Player.WHITE # MUDAR PARA EMPTY!!!!!

        # TEMP
        self.width = 5
        self.height = 5
        self.canvas = pygame.display.set_mode((self.width*70, self.height*70 + 15))
    
    def size_sel(self):
        for i in range(5, 11):
            for j in range(5, 11):
                text = self.font.render(f"{i}*{j}", True, (0,0,0), (255,255,255))
                textRect = text.get_rect()
                textRect.center = ((i-4)*50, (j-4)*60)
                self.canvas.blit(text, textRect)
        
        # TODO: process input

        self.canvas = pygame.display.set_mode((self.width*70, self.height*70 + 15))
        self.state = State(self.width, self.height)

        pygame.display.update()
    
    def mode_sel(self):
        # TODO
        return

    def board(self):
        # self.canvas.fill((184, 59, 50)) # Background

        # Static elements
        for i in range(self.width):
            pygame.board.line(self.canvas, (255,255,255), (70*i+35, 35), (70*i+35, 70*self.height-35), 2)
        for i in range(self.height):
            pygame.board.line(self.canvas, (255,255,255), (35, 70*i+35), (70*self.width-35, 70*i+35), 2)
        for i in range(self.width-1):
            for j in range(self.height-1):
                if (i+j)%2 == 0:
                    pygame.board.line(self.canvas, (255,255,255), (70*i+35, 70*j+35), (70*i+105, 70*j+105), 2)
                else:
                    pygame.board.line(self.canvas, (255,255,255), (70*i+105, 70*j+35), (70*i+35, 70*j+105), 2)

        for row in range(self.height):
            for col in range(self.width):
                if self.state.board.board[row][col] == Player.WHITE:
                    pygame.board.circle(self.canvas, (255,255,255), (70*col+35, 70*row+35), 30)
                elif self.state.board.board[row][col] == Player.BLACK:
                    pygame.board.circle(self.canvas, (0,0,0), (70*col+35, 70*row+35), 30)
        
        if self.selected_tile != None:
            pygame.board.circle(self.canvas, (235,235,52), (70*self.selected_tile[1]+35, 70*self.selected_tile[0]+35), 30, 3)
        
        if self.state.player == Player.BLACK:
            text = self.font.render("Vez das pretas", True, (0,0,0), (184,59,50))
        elif self.state.player == Player.WHITE:
            text = self.font.render("Vez das brancas", True, (255,255,255), (184,59,50))
        textRect = text.get_rect()
        textRect.center = (50, self.height*70+7)
        self.canvas.blit(text, textRect)

        # TODO: Move selection/execution/board update
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // 70
                row = y // 70
                if self.state.board.board[row][col] == self.state.player:
                    self.selected_tile = (row, col)
                else:
                    self.selected_tile = None

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
                self.winner = self.state.check_winner
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
