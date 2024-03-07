import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from state import State
from player import Player
from moves.move import Move
from moves.withdrawal_move import WithdrawalMove
from moves.free_move import FreeMove
from moves.approach_move import ApproachMove
from moves.pass_move import PassMove

def test(func):
    def wrapper(*args, **kwargs):
        print("="*50)
        print("Testing ", func.__name__)
        result = func(*args, **kwargs)
        print("Test finished")
        print("="*50)
        return result
    return wrapper

@test
def test_withdrawal_move():
    before = State()
    before.get_board_matrix().fill(Player.EMPTY)
    before.get_board_matrix()[1][0] = Player.WHITE
    before.get_board_matrix()[2][0] = Player.BLACK
    before.player = Player.WHITE

    move = WithdrawalMove(1, 0, 0, 0)
    print(move)

    after = before.execute_move(move)

    print("State before:")
    before.draw()
    print("-"*50)
    print("State after")
    after.draw()

@test
def test_free_move():
    before = State()
    before.get_board_matrix().fill(Player.EMPTY)
    before.get_board_matrix()[1][0] = Player.WHITE
    before.get_board_matrix()[4][0] = Player.BLACK
    before.player = Player.WHITE
    move = FreeMove(1, 0, 2, 0)
    print(move)
    after = before.execute_move(move)
    print("State before:")
    before.draw()
    print("-"*50)
    print("State after")
    after.draw()

@test
def test_approach_move():
    before = State()
    before.get_board_matrix().fill(Player.EMPTY)
    before.get_board_matrix()[1][0] = Player.WHITE
    before.get_board_matrix()[3:6][0:2] = Player.BLACK
    before.player = Player.WHITE

    move = ApproachMove(1, 0, 2, 0)
    print(move)

    after = before.execute_move(move)

    print("State before:")
    before.draw()
    print("-"*50)
    print("State after")
    after.draw()

@test
def test_multiple_captures():
    before = State()
    before.get_board_matrix().fill(Player.EMPTY)
    before.get_board_matrix()[1][0] = Player.WHITE
    before.get_board_matrix()[3:6][0:2] = Player.BLACK
    before.get_board_matrix()[2][2:5] = Player.BLACK
    before.player = Player.WHITE

    move = ApproachMove(1, 0, 2, 0)
    print(move)

    after = before.execute_move(move)

    before.draw()
    print("-"*50)
    after.draw()
    print("Next available moves:")
    print(after.get_available_moves())
    return after

@test
def test_pass(state):
    move = PassMove()
    print(move)
    after = state.execute_move(move)
    state.draw()
    print("-"*50)
    after.draw()

@test
def test_capture_more(state):
    move = ApproachMove(2, 0, 2, 1)
    print(move)
    after = state.execute_move(move)
    state.draw()
    print("-"*50)
    after.draw()
    print("Next available moves:")
    print(after.get_available_moves())

if __name__ == '__main__':
    test_withdrawal_move()
    test_free_move()
    test_approach_move()
    state = test_multiple_captures()
    test_pass(state)
    test_capture_more(state)

