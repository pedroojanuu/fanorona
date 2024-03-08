from board import Board
from move import Move, TypeOfMove
from player import Player
import numpy as np

class State:
    def __init__(self, width: int = 9, height: int = 5):
        self.board = Board(width, height)
        self.player = Player.WHITE
        self.move_log = []

    def get_board_matrix(self):
        return self.board.board
    
    def change_player(self):
        self.player = Player.opponent_player(self.player)

    def in_move_log(self, move: Move):
        if self.move_log == []:
            return False
        return move.get_destination() == self.move_log[0].get_origin() or any(map(lambda x: x.get_destination() == move.get_destination(), self.move_log))

    def have_the_same_direction(self, move1: Move, move2: Move):
        delta_row_move_1 = move1.row_destination - move1.row_origin
        delta_col_move_1 = move1.col_destination - move1.col_origin
        delta_row_move_2 = move2.row_destination - move2.row_origin
        delta_col_move_2 = move2.col_destination - move2.col_origin
        return delta_row_move_1 == delta_row_move_2 and delta_col_move_1 == delta_col_move_2

    def get_available_moves(self):
        if self.move_log == []:
            return self.board.get_all_moves(self.player)
        else:
            all_tile_moves = self.board.get_tile_moves(self.move_log[-1].row_destination, self.move_log[-1].col_destination)
            return list(filter(lambda x: not self.in_move_log(x) and not self.have_the_same_direction(x, self.move_log[-1]), all_tile_moves))
            
    
    def execute_move(self, move: Move):
        if move not in self.board.get_all_moves(self.player) and not self.in_move_log(move):
            print("Invalid move")
            return
        self.get_board_matrix()[move.row_destination][move.col_destination] = self.get_board_matrix()[move.row_origin][move.col_origin] 
        self.get_board_matrix()[move.row_origin][move.col_origin] = Player.EMPTY

        direction = (move.row_destination - move.row_origin, move.col_destination - move.col_origin)

        row_dest = move.row_destination
        col_dest = move.col_destination
        match (move.type):
            case TypeOfMove.APPROACH:
                row_to_kill = move.row_destination
                col_to_kill = move.col_destination
                while True:
                    row_to_kill += direction[0]
                    col_to_kill += direction[1]
                    if self.board.inside_board(row_to_kill, col_to_kill) and self.get_board_matrix()[row_to_kill][col_to_kill] == Player.opponent_player(self.player):
                        self.get_board_matrix()[row_to_kill][col_to_kill] = Player.EMPTY
                    else:
                        break
            case TypeOfMove.WITHDRAWAL:
                while True:
                    row_to_kill = move.row_origin
                    col_to_kill = move.col_origin
                    row_to_kill -= direction[0]
                    col_to_kill -= direction[1]
                    if self.board.inside_board(row_to_kill, col_to_kill) and self.get_board_matrix()[row_to_kill][col_to_kill] == Player.opponent_player(self.player):
                        self.get_board_matrix()[row_to_kill][col_to_kill] = Player.EMPTY
                    else:
                        break

        self.move_log.append(move)

        if self.get_available_moves() == []:
            self.change_player()
            self.move_log.clear()
    
    def check_winner(self):
        if np.count_nonzero(self.get_board_matrix() == Player.BLACK) == 0:
            return Player.WHITE
        if np.count_nonzero(self.get_board_matrix() == Player.WHITE) == 0:
            return Player.BLACK
        return Player.EMPTY

    def draw(self):
        print("Next Player: ", self.player)
        self.board.draw()
        print("Move Log: ", self.move_log)

if __name__ == '__main__':
    s = State()
    s.draw()

    print()
    start_move = Move(2, 3, 2, 4, TypeOfMove.WITHDRAWAL)
    print("Move to execute: ", start_move)

    print()
    print('-'*50)
    print()

    s.execute_move(start_move)
    s.draw()
