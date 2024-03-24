import numpy as np

from board import Board
from player import Player
from moves.move import Move
from moves.pass_move import PassMove

class State:
    def __init__(self, width: int = 9, height: int = 5):
        self.board = Board(width, height)
        self.player = Player.WHITE
        self.move_log = []

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
        if self.get_available_moves() == []:    # if no moves, forfeit game
            return Player.opponent_player(self.player)
        return Player.EMPTY

    def game_over(self):
        return self.check_winner() != Player.EMPTY

    def draw(self):
        print("Next Player: ", self.player)
        self.board.draw()
        print("Move Log: ", self.move_log)
