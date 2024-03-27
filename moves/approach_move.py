from moves.move import Move
from moves.motion_move import MotionMove
from player import Player


class ApproachMove(MotionMove):
    def __init__(self, row_origin, col_origin, row_destination, col_destination):
        super().__init__(row_origin, col_origin, row_destination, col_destination)

    def __str__(self):
        return super().__str__() + " Approach"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ApproachMove):
            return super().__eq__(other)
        return False

    def allows_multiple_moves(self) -> bool:
        return True

    def get_directions(self) -> tuple[int, int]:
        return (self.row_destination - self.row_origin, self.col_destination - self.col_origin)

    def get_first_to_kill(self) -> tuple[int, int]:
        rdir, cdir = self.get_directions()
        return self.row_destination + rdir, self.col_destination + cdir

    @Move.execute_decorator
    def execute(self, state):
        state = super().execute(state)
        rdir, cdir = (
            self.row_destination - self.row_origin,
            self.col_destination - self.col_origin,
        )

        row_to_kill = self.row_destination
        col_to_kill = self.col_destination
        opponent = Player.opponent_player(state.player)
        while True:
            row_to_kill += rdir
            col_to_kill += cdir
            if (
                state.board.inside_board(row_to_kill, col_to_kill)
                and state.get_board_matrix()[row_to_kill][col_to_kill] == opponent
            ):
                state.get_board_matrix()[row_to_kill][col_to_kill] = Player.EMPTY
                state.decrement_pieces_count(opponent)
            else:
                break

        state.count = 0
        return state
