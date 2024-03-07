from moves.motion_move import MotionMove
from board import PlayerEnum, opponent_player

class WithdrawalMove(MotionMove):
    def __init__(self, row_origin, col_origin, row_destination, col_destination):
        super().__init__(row_origin, col_origin, row_destination, col_destination)

    def __str__(self):
        return super().__str__ + " Free"

    def __eq__(self, other: object):
        if isinstance(other, WithdrawalMove):
            return super().__eq__(other)
        return False

    @super.execute_decorator
    def execute(self, state):
        state = super().execute(state)
        direction = (self.row_origin - self.row_destination, self.col_origin - self.col_destination)
        while True:
            row_to_kill = self.row_origin
            col_to_kill = self.col_origin
            row_to_kill -= direction[0]
            col_to_kill -= direction[1]
            if state.board.inside_board(row_to_kill, col_to_kill) and state.get_board_matrix()[row_to_kill][col_to_kill] == opponent_player(self.player):
                state.get_board_matrix()[row_to_kill][col_to_kill] = PlayerEnum.EMPTY
            else:
                break
        return state
