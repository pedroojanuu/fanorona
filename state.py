import numpy as np

from board import Board
from player import Player
from moves.move import Move
from moves.pass_move import PassMove
from moves.approach_move import ApproachMove, test_approach_move

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

    def is_white_turn(self):
        return self.player == Player.WHITE

    def in_move_log(self, move: Move):
        if self.move_log == []:
            return False
        return move.get_destination() == self.move_log[0].get_origin() or any(map(lambda x: x.get_destination() == move.get_destination(), self.move_log))

    def get_available_moves(self):
        if self.move_log == []:
            return self.board.get_all_moves(self.player)
        else:
            all_tile_moves = self.board.get_tile_moves(self.move_log[-1].row_destination, self.move_log[-1].col_destination)
            result = list(filter(lambda x: not self.in_move_log(x), all_tile_moves))

            if result != []:    # if there are available consecutive moves (captures), then allow the player to pass
                result.append(PassMove())
            return result

    def execute_move(self, move: Move) -> "State":
        if move not in self.board.get_all_moves(self.player) and not self.in_move_log(move):
            print("Invalid move")
            return None
        nstate = move.execute(self)
        # if no possible next move, change player
        if nstate.get_available_moves() == []:
            nstate.finish_turn()
        return nstate

    # def execute_move(self, move: Move):
    #     if move not in self.board.get_all_moves(self.player) and not self.in_move_log(move):
    #         print("Invalid move")
    #         return
    #     self.get_board_matrix()[move.row_destination][move.col_destination] = self.get_board_matrix()[move.row_origin][move.col_origin]
    #     self.get_board_matrix()[move.row_origin][move.col_origin] = PlayerEnum.EMPTY
    #     direction = (move.row_destination - move.row_origin, move.col_destination - move.col_origin)

    #     row_dest = move.row_destination
    #     col_dest = move.col_destination
    #     match (move.type):
    #         case TypeOfMove.APPROACH:
    #             row_to_kill = move.row_destination
    #             col_to_kill = move.col_destination
    #             while True:
    #                 row_to_kill += direction[0]
    #                 col_to_kill += direction[1]
    #                 if self.board.inside_board(row_to_kill, col_to_kill) and self.get_board_matrix()[row_to_kill][col_to_kill] == opponent_player(self.player):
    #                     self.get_board_matrix()[row_to_kill][col_to_kill] = Player.EMPTY
    #                 else:
    #                     break
    #         case TypeOfMove.WITHDRAWAL:
    #             while True:
    #                 row_to_kill = move.row_origin
    #                 col_to_kill = move.col_origin
    #                 row_to_kill -= direction[0]
    #                 col_to_kill -= direction[1]
    #                 if self.board.inside_board(row_to_kill, col_to_kill) and self.get_board_matrix()[row_to_kill][col_to_kill] == opponent_player(self.player):
    #                     self.get_board_matrix()[row_to_kill][col_to_kill] = Player.EMPTY
    #                 else:
    #                     break

    #     self.move_log.append(move)

    #     if self.get_available_moves() == []:
    #         self.change_player()
    #         self.move_log.clear()
    
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



def test_approach_move():
    before = State()
    before.get_board_matrix()[1][0] = Player.WHITE
    before.get_board_matrix()[2][0] = Player.BLACK
    before.player = Player.WHITE

    move = ApproachMove(1, 0, 0, 0)
    print(move)

    after = move.execute(before)

    print("State before:")
    print(before)
    print("State after")
    print(after)


if __name__ == '__main__':
    s = State()
    # s.draw()

    # print()
    # start_move = WithdrawalMove(2, 3, 2, 4)
    # print("Move to execute: ", start_move)

    # print()
    # print('-'*50)
    # print()

    # s.execute_move(start_move)
    s.draw()
    
    test_approach_move()

