import numpy as np
from typing import Callable
import time

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
        self.white_pieces_count = self.board.num_pieces
        self.black_pieces_count = self.board.num_pieces

    def decrement_pieces_count(self, player):
        if player == Player.WHITE:
            self.white_pieces_count -= 1
        else:
            self.black_pieces_count -= 1
    def get_num_pieces(self, player):
        if player == Player.WHITE:
            return self.white_pieces_count
        return self.black_pieces_count

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

    def execute_move(self, move: Move | None) -> "State":
        """
        Executes a move and returns the new state.
        Assumes the move is valid
        """
        if move is None:
            self.finish_turn()
            return self

        nstate: State = move.execute(self)
        nstate.add_to_log(move)
        # if no possible next move (no more captures), change player
        if not move.allows_multiple_moves() or nstate.get_available_moves() == []:
            nstate.finish_turn()
        return nstate

    def check_winner(self):
        if self.get_num_pieces(Player.WHITE) == 0:
            return Player.BLACK
        if self.get_num_pieces(Player.BLACK) == 0:
            return Player.WHITE
        return Player.EMPTY

    def game_over(self):
        return self.check_winner() != Player.EMPTY or self.count >= DRAW_COUNTER_THRESHOLD

    def draw(self):
        print("Next Player: ", self.player)
        self.board.draw()
        print("Move Log: ", self.move_log)

    def run_ais(
        self,
        ai_white: Callable[["State"], bool],
        ai_black: Callable[["State"], bool],
        log_states: bool = False,
        log_number_of_moves: bool = False,
    ) -> Player:
        """
        Run the AI players in the game until it is over.

        Parameters:
        - ai_white: A function that represents the AI player for the white side. It takes a "State" object as input and returns the new state after executing its move.
        - ai_black: A function that represents the AI player for the black side. It takes a "State" object as input and returns the new state after executing its move.
        - log_states: A boolean flag indicating whether to log the game states during the AI player's moves. Default is False.

        Returns:
        - The winner of the game.
        """
        time_white, time_black = 0, 0
        number_of_moves = 0
        while not self.game_over():
            number_of_moves += 1
            if log_states:
                print()
                print(self.get_available_moves())
                self.draw()
            if self.is_white_turn():
                start = time.time()
                self = ai_white(self)
                end = time.time()
                time_white += end - start
            else:
                start = time.time()
                self = ai_black(self)
                end = time.time()
                time_black += end - start

        if self.count == DRAW_COUNTER_THRESHOLD and log_states:
            # if X moves have passed without a capture, the game is a draw (in our simulations)
            print(f"Draw by {DRAW_COUNTER_THRESHOLD} moves rule (no captures)")

        if log_states:
            self.draw()

        winner = self.check_winner()

        if log_states:
            print(f"Winner: {winner}")

        if log_number_of_moves:
            print(f"Number of moves: {number_of_moves}")

        return winner, time_white, time_black
