from moves.motion_move import MotionMove
from board import PlayerEnum, opponent_player


class ApproachMove(MotionMove):
    def __init__(self, row_origin, col_origin, row_destination, col_destination):
        super().__init__(row_origin, col_origin, row_destination, col_destination)

    def __str__(self):
        return super().__str__ + " Approach"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ApproachMove):
            return super().__eq__(other)
        return False

    @super.execute_decorator
    def execute(self, state):
        state = super().execute(state)
        direction = (
            self.row_destination - self.row_origin,
            self.col_destination - self.col_origin,
        )
        row_to_kill = self.row_destination
        col_to_kill = self.col_destination
        while True:
            row_to_kill += direction[0]
            col_to_kill += direction[1]
            if state.board.inside_board(
                row_to_kill, col_to_kill
            ) and state.get_board_matrix()[row_to_kill][col_to_kill] == opponent_player(
                state.player
            ):
                state.get_board_matrix()[row_to_kill][col_to_kill] = PlayerEnum.EMPTY
            else:
                break
        return state
