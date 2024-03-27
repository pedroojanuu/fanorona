import pygame
import numpy as np
from state import State
from player import Player
from enum import Enum
from time import sleep

import minimax
from heuristics.heuristic import Heuristic
from heuristics.nr_pieces_heuristic import NrPiecesHeuristic
from heuristics.adjacent_pieces_heuristic import AdjacentPiecesHeuristic
from heuristics.heuristics_list import HeuristicsList
from heuristics.win_heuristic import WinHeuristic
from heuristics.groups_heuristic import GroupsHeuristic
from heuristics.center_control_heuristic import CenterControlHeuristic
from heuristics.approximate_enemy_heuristic import ApproximateEnemyHeuristic

from monte_carlo_tree_search.tree import MonteCarloTree
from monte_carlo_tree_search.tree_heuristics import MonteCarloTreeHeuristic

WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
BG_RED_COLOR = (184, 59, 50)

MIN_SIZE, MAX_SIZE = 5, 10


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
    MINIMAX_APPROXIMATE_ENEMY = 6
    MCTS_QUICK = 7
    MCTS_BETTER = 8
    MCTS_HEURISTICS = 9

    def __str__(self):
        arr = [
            "Humano",
            "Minimax (Vitória)",
            "Minimax (Nr. Peças)",
            "Minimax (Peças Adjacentes)",
            "Minimax (Grupos)",
            "Minimax (Aproximação ao Inimigo)",
            "Minimax (Controlo do Centro)",
            "MCTS (Rápido)",
            "MCTS (Melhor)",
            "MCTS (Heurísticas)",
        ]
        return arr[self.value]


class Text:
    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        color: tuple[int, int, int],
        font: pygame.font.Font,
        canvas: pygame.Surface,
    ):
        self.text = font.render(text, True, color)
        self.textRect = text.get_rect(center=(x, y))

    def draw(self, canvas: pygame.Surface):
        canvas.blit(self.text, self.textRect)


class Button:
    RECT_PADDING = 10
    RECT_BORDER_RADIUS = 4

    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        canvas: pygame.Surface,
        font: pygame.font.Font,
        textColor: tuple[int, int, int],
        bgColor: tuple[int, int, int],
        action=None,
        width=None,
        height=None,
    ):
        self.text = font.render(text, True, textColor)
        self.canvas = canvas
        self.textRect = self.text.get_rect(center=(x, y))
        self.bgColor = bgColor

        if width is None:
            width = self.textRect.width

        if height is None:
            height = self.textRect.height
        
        paddingWidth = width - self.textRect.width + self.RECT_PADDING
        paddingHeight = height - self.textRect.height + self.RECT_PADDING

        self.paddingRect = self.textRect.inflate(paddingWidth, paddingHeight)
        self.action = action

    def draw(self):
        if self.bgColor is not None:
            pygame.draw.rect(
                self.canvas, self.bgColor, self.paddingRect, 0, self.RECT_BORDER_RADIUS
            )
        self.canvas.blit(self.text, self.textRect)

    def mouse_collision(self, x, y):
        return self.paddingRect.collidepoint(x, y)


class Game:
    DEFAULT_WIDTH = 7
    DEFAULT_HEIGHT = 7

    @staticmethod
    def get_canvas_width(width):
        return width * 70

    @staticmethod
    def get_canvas_height(height):
        return height * 70 + 15

    def get_default_canvas_width(self):
        return self.get_canvas_width(self.DEFAULT_WIDTH)
    def get_default_canvas_height(self):
        return self.get_canvas_height(self.DEFAULT_HEIGHT)

    def __init__(self):
        pygame.init()
        self.change_canvas_size(self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT)
        self.canvas.fill(BG_RED_COLOR)  # Background
        self.font = pygame.font.Font("freesansbold.ttf", 15)
        pygame.display.set_caption("Fanorona")
        pygame.display.update()

        self.frame_rate = 30
        self.frame_time_counter = 0

        self.window_state = WindowState.BOARD_SIZE_SEL
        self.selected_piece = None

        self.width = None
        self.height = None

        self.game_state: State = None
        self.winner: Player = Player.EMPTY
        self.white_mode = None
        self.black_mode = None
        self.available_moves = None

        self.white_alg = None
        self.black_alg = None

        self.size_sel_title = self.font.render(
            "Selecione o tamanho do tabuleiro", True, WHITE_COLOR
        )
        self.size_sel_title_rect = self.size_sel_title.get_rect(center=(self.get_default_canvas_width() // 2, 15))

        self.size_sel_buttons: list[Button] = []
        for col in range(MIN_SIZE, MAX_SIZE + 1):
            for row in range(MIN_SIZE, MAX_SIZE + 1):
                self.size_sel_buttons.append(
                    Button(
                        (col - 4) * self.DEFAULT_WIDTH * 10,
                        (row - 4) * self.DEFAULT_HEIGHT * 10,
                        f"{col}*{row}",
                        self.canvas,
                        self.font,
                        BLACK_COLOR,
                        WHITE_COLOR,
                        self.size_sel_button_action(col, row),
                    )
                )
        self.mode_sel_buttons = [
            Button(
                x=self.DEFAULT_WIDTH * 35,
                y=(i + 2) * 40,
                text=str(mode),
                canvas=self.canvas,
                font=self.font,
                textColor=BLACK_COLOR,
                bgColor=WHITE_COLOR,
                action=self.mode_sel_button_action(mode),
                width=self.DEFAULT_WIDTH * 35,
                height=None,
            )
            for i, mode in enumerate(PlayerModes)
        ]

        self.widthStr = None
        self.whiteTypeStr = None

        self.back_buttons = [
            self.create_back_button(self.back_to_board_size_sel(from_game_over=False)),
            self.create_back_button(self.back_to_white_mode_sel),
            self.create_back_button(self.back_to_black_mode_sel),
            self.create_back_button(self.back_to_board_size_sel(from_game_over=True)),
        ]
    def back_to_white_mode_sel(self):
        self.white_mode = None
        self.window_state = WindowState.WHITE_MODE_SEL

    def back_to_black_mode_sel(self):
        self.black_mode = None
        self.change_canvas_size(self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT)
        self.window_state = WindowState.BLACK_MODE_SEL

    def back_to_board_size_sel(self, from_game_over):
        def func():
            if from_game_over:
                self.winner = Player.EMPTY
                self.selected_piece = None
                self.back_to_black_mode_sel()
                self.back_to_white_mode_sel()
                self.back_to_board_size_sel(from_game_over=False)()
            self.width = None
            self.height = None
            self.window_state = WindowState.BOARD_SIZE_SEL
        return func

    def create_back_button(self, action) -> Button:
        return Button(
            30,
            15,
            "Voltar",
            self.canvas,
            self.font,
            BLACK_COLOR,
            WHITE_COLOR,
            action=action,
        )
    def get_back_button(self) -> Button | None:
        match self.window_state:
            case WindowState.WHITE_MODE_SEL:
                return self.back_buttons[0]
            case WindowState.BLACK_MODE_SEL:
                return self.back_buttons[1]
            case WindowState.PLAYING:
                return self.back_buttons[2]
            case WindowState.GAME_OVER:
                return self.back_buttons[3]
        return None

    def mode_sel_button_action(self, mode):
        def func():
            if self.window_state == WindowState.WHITE_MODE_SEL:
                self.white_mode = PlayerModes(mode)
                self.whiteTypeStr = str(mode)
            elif self.window_state == WindowState.BLACK_MODE_SEL:
                self.black_mode = PlayerModes(mode)
                self.game_state = State(self.width, self.height)
                self.available_moves = self.game_state.get_available_moves()
                self.selected_piece = None
        return func

    def change_canvas_size(self, width, height):
        self.canvas = pygame.display.set_mode((width * 70, height * 70 + 15))

    def size_sel_button_action(self, col, row):
        def func():
            self.width = col
            self.height = row
            self.window_state = WindowState.WHITE_MODE_SEL
            self.widthStr = f"{self.width}*{self.height}"

        return func

    def check_exit_event(self, event):
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            exit()

    def size_sel(self):
        self.canvas.fill(BG_RED_COLOR)  # Background
        self.canvas.blit(self.size_sel_title, self.size_sel_title_rect)

        back_button = self.get_back_button()
        if back_button is not None:
            back_button.draw()

        for button in self.size_sel_buttons:
            button.draw()

        for event in pygame.event.get():
            self.check_exit_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for button in self.size_sel_buttons:
                    if button.mouse_collision(x, y):
                        button.action()
                        return

                if back_button is not None and back_button.mouse_collision(x, y):
                    back_button.action()
                    return

        pygame.display.update()

    def get_mode_sel_text(self):
        center = (self.DEFAULT_WIDTH * 35, 15)
        text = None

        if self.window_state == WindowState.WHITE_MODE_SEL:
            text = self.font.render(
                f"Tamanho: {self.widthStr}. Selecione o modo da equipa branca",
                True,
                WHITE_COLOR,
            )
        elif self.window_state == WindowState.BLACK_MODE_SEL:
            text = self.font.render(
                f"Tamanho: {self.widthStr}. Branco: {self.whiteTypeStr}. Selecione o modo da equipa preta",
                True,
                BLACK_COLOR,
            )

        textRect = text.get_rect(center=center)
        return text, textRect

    def mode_sel(self):
        self.canvas.fill(BG_RED_COLOR)  # Background

        text, textRect = self.get_mode_sel_text()
        self.canvas.blit(text, textRect)

        back_button = self.get_back_button()
        if back_button is not None:
            back_button.draw()
        for button in self.mode_sel_buttons:
            button.draw()

        pygame.display.update()

        for event in pygame.event.get():
            self.check_exit_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for button in self.mode_sel_buttons:
                    if button.mouse_collision(x, y):
                        button.action()

                if back_button is not None and back_button.mouse_collision(x, y):
                    back_button.action()
                    return

        if self.white_mode is not None and self.window_state == WindowState.WHITE_MODE_SEL:
            if self.white_mode == PlayerModes.MINIMAX_WIN:
                self.white_alg = minimax.get_minimax_move(
                    WinHeuristic().evaluate_board, 4
                )
            elif self.white_mode == PlayerModes.MINIMAX_NR_PIECES:
                self.white_alg = minimax.get_minimax_move(
                    NrPiecesHeuristic().evaluate_board, 4
                )
            elif self.white_mode == PlayerModes.MINIMAX_ADJACENT_PIECES:
                self.white_alg = minimax.get_minimax_move(
                    AdjacentPiecesHeuristic().evaluate_board, 4
                )
            elif self.white_mode == PlayerModes.MINIMAX_GROUPS:
                self.white_alg = minimax.get_minimax_move(
                    GroupsHeuristic().evaluate_board, 4
                )
            elif self.white_mode == PlayerModes.MINIMAX_CENTER_CONTROL:
                self.white_alg = minimax.get_minimax_move(
                    CenterControlHeuristic().evaluate_board, 4
                )
            elif self.white_mode == PlayerModes.MINIMAX_APPROXIMATE_ENEMY:
                self.white_alg = minimax.get_minimax_move(
                    ApproximateEnemyHeuristic().evaluate_board, 4
                )
            elif (
                self.white_mode == PlayerModes.MCTS_QUICK
                or self.white_mode == PlayerModes.MCTS_BETTER
            ):
                self.white_alg = MonteCarloTree.from_player(
                    self.width, self.height, Player.WHITE
                )
            elif self.white_mode == PlayerModes.MCTS_HEURISTICS:
                h = HeuristicsList(
                    heuristics=np.array(
                        [
                            WinHeuristic(),
                            NrPiecesHeuristic(),
                            GroupsHeuristic(),
                            CenterControlHeuristic(),
                        ]
                    ),
                    weights=np.array([100000, 50, 10, 5]),
                )
                self.white_alg = MonteCarloTreeHeuristic.from_player(
                    h, self.width, self.height, Player.WHITE
                )
            self.window_state = WindowState.BLACK_MODE_SEL
        elif (
            self.black_mode is not None and self.window_state == WindowState.BLACK_MODE_SEL
        ):
            if self.black_mode == PlayerModes.MINIMAX_WIN:
                self.black_alg = minimax.get_minimax_move(
                    WinHeuristic().evaluate_board, 4
                )
            elif self.black_mode == PlayerModes.MINIMAX_NR_PIECES:
                self.black_alg = minimax.get_minimax_move(
                    NrPiecesHeuristic().evaluate_board, 4
                )
            elif self.black_mode == PlayerModes.MINIMAX_ADJACENT_PIECES:
                self.black_alg = minimax.get_minimax_move(
                    AdjacentPiecesHeuristic().evaluate_board, 4
                )
            elif self.black_mode == PlayerModes.MINIMAX_GROUPS:
                self.black_alg = minimax.get_minimax_move(
                    GroupsHeuristic().evaluate_board, 4
                )
            elif self.black_mode == PlayerModes.MINIMAX_CENTER_CONTROL:
                self.black_alg = minimax.get_minimax_move(
                    CenterControlHeuristic().evaluate_board, 4
                )
            elif self.black_mode == PlayerModes.MINIMAX_APPROXIMATE_ENEMY:
                self.black_alg = minimax.get_minimax_move(
                    ApproximateEnemyHeuristic().evaluate_board, 4
                )
            elif (
                self.black_mode == PlayerModes.MCTS_QUICK
                or self.black_mode == PlayerModes.MCTS_BETTER
            ):
                self.black_alg = MonteCarloTree.from_player(
                    self.width, self.height, Player.BLACK
                )
            elif self.black_mode == PlayerModes.MCTS_HEURISTICS:
                h = HeuristicsList(
                    heuristics=np.array(
                        [
                            WinHeuristic(),
                            NrPiecesHeuristic(),
                            GroupsHeuristic(),
                            CenterControlHeuristic(),
                        ]
                    ),
                    weights=np.array([100000, 50, 10, 5]),
                )
                self.black_alg = MonteCarloTreeHeuristic.from_player(
                    h, self.width, self.height, Player.BLACK
                )
            self.window_state = WindowState.PLAYING
            self.change_canvas_size(self.width, self.height)

        return

    def board(self):
        self.canvas.fill(BG_RED_COLOR)  # Background
        back_button = self.get_back_button()

        # Static elements
        for i in range(self.width):
            pygame.draw.line(
                self.canvas,
                WHITE_COLOR,
                (70 * i + 35, 35),
                (70 * i + 35, 70 * self.height - 35),
                2,
            )
        for i in range(self.height):
            pygame.draw.line(
                self.canvas,
                WHITE_COLOR,
                (35, 70 * i + 35),
                (70 * self.width - 35, 70 * i + 35),
                2,
            )
        for i in range(self.width - 1):
            for j in range(self.height - 1):
                if (i + j) % 2 == 0:
                    pygame.draw.line(
                        self.canvas,
                        WHITE_COLOR,
                        (70 * i + 35, 70 * j + 35),
                        (70 * i + 105, 70 * j + 105),
                        2,
                    )
                else:
                    pygame.draw.line(
                        self.canvas,
                        WHITE_COLOR,
                        (70 * i + 105, 70 * j + 35),
                        (70 * i + 35, 70 * j + 105),
                        2,
                    )

        for row in range(self.height):
            for col in range(self.width):
                if self.game_state.get_board_matrix()[row][col] == Player.WHITE:
                    pygame.draw.circle(
                        self.canvas, WHITE_COLOR, (70 * col + 35, 70 * row + 35), 30
                    )
                elif self.game_state.board.board[row][col] == Player.BLACK:
                    pygame.draw.circle(
                        self.canvas, BLACK_COLOR, (70 * col + 35, 70 * row + 35), 30
                    )

        if self.selected_piece != None:
            pygame.draw.circle(
                self.canvas,
                (235, 235, 52),
                (70 * self.selected_piece[1] + 35, 70 * self.selected_piece[0] + 35),
                30,
                3,
            )

        if self.game_state.player == Player.BLACK:
            text = self.font.render("Vez das pretas", True, BLACK_COLOR)
        elif self.game_state.player == Player.WHITE:
            text = self.font.render("Vez das brancas", True, WHITE_COLOR)
        textRect = text.get_rect(center = (100, self.height * 70 + 7))
        self.canvas.blit(text, textRect)

        if back_button is not None:
            back_button.draw()

        if (
            self.white_mode == PlayerModes.HUMAN
            and self.game_state.player == Player.WHITE
        ) or (
            self.black_mode == PlayerModes.HUMAN
            and self.game_state.player == Player.BLACK
        ):
            self.available_moves = self.game_state.get_available_moves()
            for move in self.available_moves:
                if str(move) != "Pass" and self.selected_piece == (
                    move.row_origin,
                    move.col_origin,
                ):
                    pygame.draw.circle(
                        self.canvas,
                        (0, 255, 0),
                        (
                            70 * move.col_destination + 35,
                            70 * move.row_destination + 35,
                        ),
                        30,
                        3,
                    )

            for event in pygame.event.get():
                self.check_exit_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if back_button is not None and back_button.mouse_collision(x, y):
                        back_button.action()
                        return
                    col = x // 70
                    row = y // 70
                    if self.game_state.board.board[row][col] == self.game_state.player:
                        self.selected_piece = (row, col)
                    elif self.game_state.board.board[row][col] == Player.EMPTY:
                        for move in self.available_moves:
                            if self.selected_piece == (
                                move.row_origin,
                                move.col_origin,
                            ) and (row, col) == (
                                move.row_destination,
                                move.col_destination,
                            ):
                                if self.game_state.player == Player.BLACK and (
                                    self.black_mode == PlayerModes.MCTS_QUICK
                                    or self.black_mode == PlayerModes.MCTS_BETTER
                                    or self.black_mode == PlayerModes.MCTS_HEURISTICS
                                ):
                                    self.white_alg.update_move(move)
                                elif self.game_state.player == Player.WHITE and (
                                    self.white_mode == PlayerModes.MCTS_QUICK
                                    or self.white_mode == PlayerModes.MCTS_BETTER
                                    or self.white_mode == PlayerModes.MCTS_HEURISTICS
                                ):
                                    self.black_alg.update_move(move)
                                self.game_state = self.game_state.execute_move(move)
                                self.selected_piece = None
                                pygame.display.update()
                                return
        elif self.game_state.player == Player.WHITE:
            move = None
            if (
                self.white_mode == PlayerModes.MINIMAX_WIN
                or self.white_mode == PlayerModes.MINIMAX_NR_PIECES
                or self.white_mode == PlayerModes.MINIMAX_ADJACENT_PIECES
                or self.white_mode == PlayerModes.MINIMAX_GROUPS
                or self.white_mode == PlayerModes.MINIMAX_CENTER_CONTROL
            ):
                sleep(0.5)
                move = self.white_alg(self.game_state)
                self.game_state = self.game_state.execute_move(move)
            elif self.white_mode == PlayerModes.MCTS_QUICK:
                self.white_alg.train_until(100)
                move = self.white_alg.get_best_move()
                self.game_state = self.game_state.execute_move(move)
                self.white_alg.update_move(move)
            elif self.white_mode == PlayerModes.MCTS_BETTER:
                self.white_alg.train_until(10000)
                move = self.white_alg.get_best_move()
                self.game_state = self.game_state.execute_move(move)
                self.white_alg.update_move(move)
            elif self.white_mode == PlayerModes.MCTS_HEURISTICS:
                self.white_alg.train_time(0.01 * self.width * self.height)
                move = self.white_alg.get_best_move()
                self.game_state = self.game_state.execute_move(move)
                self.white_alg.update_move(move)

            if (
                self.black_mode == PlayerModes.MCTS_QUICK
                or self.black_mode == PlayerModes.MCTS_BETTER
                or self.black_mode == PlayerModes.MCTS_HEURISTICS
            ):
                self.black_alg.update_move(move)
        elif self.game_state.player == Player.BLACK:
            move = None
            if (
                self.black_mode == PlayerModes.MINIMAX_WIN
                or self.black_mode == PlayerModes.MINIMAX_NR_PIECES
                or self.black_mode == PlayerModes.MINIMAX_ADJACENT_PIECES
                or self.black_mode == PlayerModes.MINIMAX_GROUPS
                or self.black_mode == PlayerModes.MINIMAX_CENTER_CONTROL
            ):
                sleep(0.5)
                move = self.black_alg(self.game_state)
                self.game_state = self.game_state.execute_move(move)
            elif self.black_mode == PlayerModes.MCTS_QUICK:
                sleep(0.5)
                self.black_alg.train_until(100)
                move = self.black_alg.get_best_move()
                self.game_state = self.game_state.execute_move(move)
                self.black_alg.update_move(move)
            elif self.black_mode == PlayerModes.MCTS_BETTER:
                self.black_alg.train_until(10000)
                move = self.black_alg.get_best_move()
                self.game_state = self.game_state.execute_move(move)
                self.black_alg.update_move(move)
            elif self.black_mode == PlayerModes.MCTS_HEURISTICS:
                sleep(0.5)
                self.black_alg.train_time(0.01 * self.width * self.height)
                move = self.black_alg.get_best_move()
                self.game_state = self.game_state.execute_move(move)
                self.black_alg.update_move(move)

            if (
                self.white_mode == PlayerModes.MCTS_QUICK
                or self.white_mode == PlayerModes.MCTS_BETTER
                or self.white_mode == PlayerModes.MCTS_HEURISTICS
            ):
                self.white_alg.update_move(move)

        pygame.display.update()

    def game_over(self):
        self.canvas.fill(BG_RED_COLOR)  # Background
        if self.winner == Player.BLACK:
            text = self.font.render("Pretas vencem!", True, BLACK_COLOR)
            color = BLACK_COLOR
        elif self.winner == Player.WHITE:
            text = self.font.render("Brancas vencem!", True, WHITE_COLOR)
            color = WHITE_COLOR
        else:
            text = self.font.render("Empate!", True, BLACK_COLOR)
            color = BLACK_COLOR

        textRect = text.get_rect(center = (self.width * 35, self.height * 35))
        self.canvas.blit(text, textRect)

        text = self.font.render("Obrigado por jogar Fanorona!", True, color)
        textRect = text.get_rect(center = (self.width * 35, self.height * 35 + 30))
        self.canvas.blit(text, textRect)

        text = self.font.render("Félix Martins, Pedro Lima e Pedro Januário", True, color)
        textRect = text.get_rect(center = (self.width * 35, self.height * 35 + 50))
        self.canvas.blit(text, textRect)

        text = self.font.render("Pressione ESC ou feche a janela para sair", True, color)
        textRect = text.get_rect(center = (self.width * 35, self.height * 35 + 90))
        self.canvas.blit(text, textRect)


        back_button = self.get_back_button()
        if back_button is not None:
            back_button.draw()

        pygame.display.update()

        for event in pygame.event.get():
            self.check_exit_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if back_button is not None and back_button.mouse_collision(x, y):
                    back_button.action()
                    return



    def play(self):
        while True:
            if self.window_state == WindowState.PLAYING:
                self.winner = self.game_state.check_winner()
                if self.winner != Player.EMPTY:
                    self.window_state = WindowState.GAME_OVER
                    continue
                self.board()
            elif self.window_state == WindowState.BOARD_SIZE_SEL:
                self.size_sel()
            elif (
                self.window_state == WindowState.WHITE_MODE_SEL
                or self.window_state == WindowState.BLACK_MODE_SEL
            ):
                self.mode_sel()
            elif self.window_state == WindowState.GAME_OVER:
                self.game_over()


if __name__ == "__main__":
    game = Game()
    game.play()
