from moves.motion_move import MotionMove

class FreeMove(MotionMove):
    def __init__(self, row_origin, col_origin, row_destination, col_destination):
        super().__init__(row_origin, col_origin, row_destination, col_destination)
    
    def __str__(self):
        return super().__str__ + " Free"

    def __eq__(self, other: object):
        if isinstance(other, FreeMove):
            return super().__eq__(other)
        return False

    @super.execute_decorator
    def execute(self, state):
        return super().execute(state)
