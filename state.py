import numpy as np
from typing import Callable

from board import Board
from player import Player
from moves.move import Move
from moves.pass_move import PassMove

DRAW_COUNTER_THRESHOLD = 20

class State:
    def __init__(self, width: int = 9, height: int = 5):
        self.board = Board(width, height)
        self.player = Player.WHITE
        self.move_log = []
        self.count = 0

    def get_board_matrix(self):
        return self.board.board

    def change_player(self):
        self.player = Player.opponent_player(self.player)

    def finish_turn(self):
        self.change_player()
        self.move_log.clear()

    def add_to_log(self, move):
        self.move_log.append(move)

    def is_white_turn(self):
        return self.player == Player.WHITE

    def in_move_log(self, move: Move):
        if self.move_log == []:
            return False
        if not move.allows_multiple_moves():
            return False
        return move.get_destination() == self.move_log[0].get_origin() or any(map(lambda x: x.get_destination() == move.get_destination(), self.move_log))

    def get_available_moves(self):
        """
        Depending on the move log, will return normal moves or consecutive moves (only captures and pass)
        """
        if self.move_log == []:
            return self.board.get_all_moves(self.player)

        all_tile_moves = self.board.get_tile_moves(self.move_log[-1].row_destination, self.move_log[-1].col_destination)
        result = list(filter(lambda x: not self.in_move_log(x), all_tile_moves))
        if result != []:    # if there are available consecutive moves (captures), then allow the player to pass
            result.append(PassMove())
        return result

    def execute_move(self, move: Move) -> "State":
        """
        Executes a move and returns the new state.
        Assumes the move is valid
        """
        nstate: State = move.execute(self)
        nstate.add_to_log(move)
        # if no possible next move (no more captures), change player
        if not move.allows_multiple_moves() or nstate.get_available_moves() == []:
            nstate.finish_turn()
        return nstate

    def check_winner(self):
        if np.count_nonzero(self.get_board_matrix() == Player.BLACK) == 0:
            return Player.WHITE
        if np.count_nonzero(self.get_board_matrix() == Player.WHITE) == 0:
            return Player.BLACK
        return Player.EMPTY

    def game_over(self):
        return self.check_winner() != Player.EMPTY

    def draw(self):
        print("Next Player: ", self.player)
        self.board.draw()
        print("Move Log: ", self.move_log)

    def run_ais(
        self,
        ai_white: Callable[["State"], bool],
        ai_black: Callable[["State"], bool],
        log_states: bool = False,
    ) -> Player:
        """
        Run the AI players in the game until it is over.

        Parameters:
        - ai_white: A function that represents the AI player for the white side. It takes a "Game" object as input and returns a boolean representing whether it has no moves.
        - ai_black: A function that represents the AI player for the black side. It takes a "Game" object as input and returns a boolean representing whether it has no moves.
        - log_states: A boolean flag indicating whether to log the game states during the AI player's moves. Default is False.

        Returns:
        - The winner of the game.
        """
        winner = None

        while not self.game_over() and winner is None and self.count < DRAW_COUNTER_THRESHOLD:
            print(self.get_available_moves())
            if log_states:
                self.draw()
            if self.is_white_turn():
                self = ai_white(self)
            else:
                self = ai_black(self)

        if self.count == DRAW_COUNTER_THRESHOLD:
            # if X moves have passed without a capture, the game is a draw
            print(f"Draw by {DRAW_COUNTER_THRESHOLD} moves rule (no captures)")

        if log_states:
            self.draw()

        if winner is None:
            winner = self.check_winner()

        if log_states:
            print(f"Winner: {winner}")
        return winner
