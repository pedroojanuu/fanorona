from board import Board, PlayerEnum, opponent_player
from move import Move, TypeOfMove
import numpy as np

class State:
    def __init__(self, width=9, height=5):
        self.board = Board(width, height)
        self.player = PlayerEnum.WHITE
        self.move_log = []

    def get_board_matrix(self):
        return self.board.board
    
    def change_player(self):
        self.player = opponent_player(self.player)

    def in_move_log(self, move: Move):
        if self.move_log == []:
            return False
        return move.get_destination() == self.move_log[0].get_origin() or all(map(lambda x: x.get_destination() == move.get_destination(), self.move_log))

    def get_available_moves(self):
        if self.move_log == []:
            return self.board.get_all_moves(self.player)
        else:
            all_tile_moves = self.board.get_tile_moves(self.move_log[-1].row_destination, self.move_log[-1].col_destination)
            return list(filter(lambda x: not self.in_move_log(x), all_tile_moves))
            
    
    def execute_move(self, move: Move):
        if move not in self.board.get_all_moves(self.player) and not self.in_move_log(move):
            print("Invalid move")
            return
        self.get_board_matrix()[move.row_destination][move.col_destination] = self.get_board_matrix()[move.row_origin][move.col_origin] 
        self.get_board_matrix()[move.row_origin][move.col_origin] = PlayerEnum.EMPTY

        direction = (move.row_destination - move.row_origin, move.col_destination - move.col_origin)

        row_dest = move.row_destination
        col_dest = move.col_destination
        if move.type == TypeOfMove.APPROACH:
                row_to_kill = move.row_destination
                col_to_kill = move.col_destination
                while True:
                    row_to_kill += direction[0]
                    col_to_kill += direction[1]
                    if self.board.inside_board(row_to_kill, col_to_kill) and self.get_board_matrix()[row_to_kill][col_to_kill] == opponent_player(self.player):
                        self.get_board_matrix()[row_to_kill][col_to_kill] = PlayerEnum.EMPTY
                    else:
                        break
        elif move.type == TypeOfMove.WITHDRAWAL:
                while True:
                    row_to_kill = move.row_origin
                    col_to_kill = move.col_origin
                    row_to_kill -= direction[0]
                    col_to_kill -= direction[1]
                    if self.board.inside_board(row_to_kill, col_to_kill) and self.get_board_matrix()[row_to_kill][col_to_kill] == opponent_player(self.player):
                        self.get_board_matrix()[row_to_kill][col_to_kill] = PlayerEnum.EMPTY
                    else:
                        break

        self.move_log.append(move)

        if self.get_available_moves() == []:
            self.change_player()
            self.move_log.clear()
    
    def check_winner(self):
        if np.count_nonzero(self.get_board_matrix() == PlayerEnum.WHITE) == 0:
            return PlayerEnum.BLACK
        if np.count_nonzero(self.get_board_matrix() == PlayerEnum.BLACK) == 0:
            return PlayerEnum.WHITE
        return PlayerEnum.EMPTY
    
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
