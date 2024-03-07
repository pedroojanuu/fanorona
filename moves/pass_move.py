from moves.move import Move

class PassMove(Move):
    def __init__(self):
        super().__init__()

    def __str__():
        return "Pass"

    def __eq__(self, other: object):
        return isinstance(other, PassMove)

    @Move.execute_decorator
    def execute(self, state):
        state.finish_turn()
        return state
