from time import sleep
import pygame
from board import Board, PlayerEnum, opponent_player

class Game:
    def __init__(self):
        pygame.init()
        self.canvas = pygame.display.set_mode((350, 400))
        self.canvas.fill((184, 59, 50)) # Background
        pygame.display.set_caption("Fanorona")
        pygame.display.update()

        self.selected_tile = None
        
        # TODO: Mode selection

        # TODO: Board size selection
        # for i in range(5, 10):
        #     pygame.draw.rect(self.canvas, (255,255,255), (70*i, 350, 70, 50))
        #     font = pygame.font.Font('Montserrat-Black.otf', 36)
        #     text = font.render(str(i), True, (0,0,0))
        #     self.canvas.blit(text, (70*i+10, 360))
        # pygame.display.update()

        # while True:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        #             exit()
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             x, y = pygame.mouse.get_pos()
        #             print(x, y)
        
        # TEMP
        self.width = 5
        self.height = 5
        # TEMP

        self.canvas = pygame.display.set_mode((self.width*70, self.height*70 + 15))

        self.board = Board(width=self.width, height=self.height)
        self.player = PlayerEnum.BLACK

        self.exit = False
    
    def change_player(self):
        self.player = opponent_player(self.player)
    
    def draw(self):
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
                if self.board.board[row][col] == PlayerEnum.WHITE:
                    pygame.draw.circle(self.canvas, (255,255,255), (70*col+35, 70*row+35), 30)
                elif self.board.board[row][col] == PlayerEnum.BLACK:
                    pygame.draw.circle(self.canvas, (0,0,0), (70*col+35, 70*row+35), 30)
        
        if self.selected_tile != None:
            pygame.draw.circle(self.canvas, (235,235,52), (70*self.selected_tile[1]+35, 70*self.selected_tile[0]+35), 30, 3)
        
        # TODO: Write player turn in bottom

        pygame.display.update()

    def play(self):
        while not self.exit:
            # TODO: Move selection/execution/board update
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.exit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // 70
                    row = y // 70
                    if self.board.board[row][col] != PlayerEnum.EMPTY:
                        self.selected_tile = (row, col)

            # TODO: Check winner

            self.draw()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.play()
