from board import Board, PlayerEnum, opponent_player
from move import Move, TypeOfMove
import numpy as np

class State:
    def __init__(self):
        self.board = Board()
        self.player = PlayerEnum.WHITE
        self.move_log = []

    def get_board_matrix(self):
        return self.board.board
    
    def change_player(self):
        self.player = opponent_player(self.player)
    
    def execute_move(self, move: Move):
        self.get_board_matrix()[move.row_destination][move.col_destination] = self.get_board_matrix()[move.row_origin][move.col_origin] 
        self.get_board_matrix()[move.row_origin][move.col_origin] = PlayerEnum.EMPTY

        direction = (move.row_destination - move.row_origin, move.col_destination - move.col_origin)

        row_dest = move.row_destination
        col_dest = move.col_destination
        match (move.type):
            case TypeOfMove.APPROACH:
                while True:
                    row_dest += direction[0]
                    col_dest += direction[1]
                    if self.board.inside_board(row_dest, col_dest) and self.get_board_matrix()[row_dest][col_dest] == opponent_player(self.get_board_matrix()[move.row_origin][move.col_origin]):
                        self.get_board_matrix()[row_dest][col_dest] = PlayerEnum.EMPTY
                    else:
                        break
            case TypeOfMove.WITHDRAWAL:
                row_dest -= direction[0]
                col_dest -= direction[1]
                if self.board.inside_board(row_dest, col_dest) and self.get_board_matrix()[row_dest][col_dest] == opponent_player(self.get_board_matrix()[move.row_origin][move.col_origin]):
                    self.get_board_matrix()[row_dest][col_dest] = PlayerEnum.EMPTY

        self.move_log.append(move)

        if(self.board.get_tile_moves(move.row_destination, move.col_destination) == []):
            self.change_player()
    
    def check_winner(self):
        if np.count_nonzero(self.get_board_matrix() == 1) == 0:
            return PlayerEnum.WHITE
        if np.count_nonzero(self.get_board_matrix() == 2) == 0:
            return PlayerEnum.BLACK
        return PlayerEnum.EMPTY
    
    def draw(self):
        print("Player: ", self.player)
        self.board.draw()
        print("Move Log: ", self.move_log)

if __name__ == '__main__':
    s = State()
    s.draw()
    s.execute_move(Move(3, 4, 2, 4, TypeOfMove.APPROACH))
    s.draw()
