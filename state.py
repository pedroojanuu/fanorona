from board import Board, PlayerEnum, opponent_player
from move import Move, TypeOfMove

class State:
    def __init__(self):
        self.board = board.Board()
        self.player = board.PlayerEnum.WHITE
        self.list_of_moves_in_play = []
    
    def change_player(self):
        self.player = opponent_player(self.player)

    def moves(self, player: PlayerEnum):
        moves = []
        pieces = np.argwhere(self.board == player)
        for [r, c] in pieces:
            for r2, c2, r3, c3 in self.board.get_adjacent_aproach(r, c):
                if self.board[r2][c2] == PlayerEnum.EMPTY and self.board[r3][c3] == opponent_player(player):
                    if move not in self.list_of_moves_in_play:
                        moves.append((r, c, r2, c2))
            for r2, c2, r3, c3 in self.board.get_adjacent_withdrawal(r, c):
                if self.board[r2][c2] == PlayerEnum.EMPTY and self.board[r3][c3] == opponent_player(player):
                    if move not in self.list_of_moves_in_play:
                        moves.append((r, c, r2, c2))
        return moves
    
    def execute_move(self, move: Move):
        r, c = origin
        r2, c2 = destination
        self.board[r2][c2] = self.board[r][c]
        self.board[r][c] = PlayerEnum.EMPTY

        direction = (r2 - r, c2 - c)
        match (move.type):
            case TypeOfMove.APPROACH:
                while True:
                    r2 += direction[0]
                    c2 += direction[1]
                    if(self.board.board[r2][c2] == opponent_player(self.board.board[r][c])):
                        self.board[r2][c2] = PlayerEnum.EMPTY
                    else:
                        break
                self.board[r3][c3] = PlayerEnum.EMPTY
            case TypeOfMove.WITHDRAWAL:
                r3, c3 = (r - r2) + r
                self.board[r3][c3] = PlayerEnum.EMPTY
            case TypeOfMove.FREE:
                pass

        self.list_of_moves_in_play.append((r, c, r2, c2))
    
    def check_winner(self):
        if np.count_nonzero(self.board == 1) == 0:
            return PlayerEnum.WHITE
        if np.count_nonzero(self.board == 2) == 0:
            return PlayerEnum.BLACK
        return PlayerEnum.EMPTY


