from board import Board, PlayerEnum, opponent_player
from move import Move, TypeOfMove

class State:
    def __init__(self):
        self.board = Board()
        self.player = PlayerEnum.WHITE
        self.move_log = []
    
    def change_player(self):
        self.player = opponent_player(self.player)
    
    def execute_move(self, move: Move):
        self.board.board[move.row_destination][move.col_destination] = self.board.board[move.row_origin][move.col_origin] 
        self.board.board[move.row_origin][move.col_origin] = PlayerEnum.EMPTY

        direction = (move.row_destination - move.row_origin, move.col_destination - move.col_origin)

        row_dest = move.row_destination
        col_dest = move.col_destination
        match (move.type):
            case TypeOfMove.APPROACH:
                while True:
                    row_dest += direction[0]
                    col_dest += direction[1]
                    if self.board.inside_board(row_dest, col_dest) and self.board.board[row_dest][col_dest] == opponent_player(self.board.board[move.row_origin][move.col_origin]):
                        self.board.board[row_dest][col_dest] = PlayerEnum.EMPTY
                    else:
                        break
            case TypeOfMove.WITHDRAWAL:
                row_dest -= direction[0]
                col_dest -= direction[1]
                if self.board.inside_board(row_dest, col_dest) and self.board.board[row_dest][col_dest] == opponent_player(self.board.board[move.row_origin][move.col_origin]):
                    self.board.board[row_dest][col_dest] = PlayerEnum.EMPTY

        self.move_log.append(move)
    
    # def check_winner(self):
    #     if np.count_nonzero(self.board == 1) == 0:
    #         return PlayerEnum.WHITE
    #     if np.count_nonzero(self.board == 2) == 0:
    #         return PlayerEnum.BLACK
    #     return PlayerEnum.EMPTY
    
    def draw(self):
        print("Player: ", self.player)
        self.board.draw()
        print("Move Log: ", self.move_log)

if __name__ == '__main__':
    # b = Board()
    s = State()
    s.draw()
    s.execute_move(Move(3, 4, 2, 4, TypeOfMove.APPROACH))
    s.draw()
    print(s.board.moves(PlayerEnum.WHITE))
