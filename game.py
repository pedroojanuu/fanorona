from state import State
from board import PlayerEnum
import random

class Game:
    def __init__(self, width: int = 9, height: int = 5):
        self.state = State(width, height)

def play_simulation(initial_state: State):
    initial_state.draw()

    for i in range(50):
        # print("Available moves: ", initial_state.board.get_available_moves(initial_state.player))
        move_to_exe = random.choice(initial_state.get_available_moves())
        print()
        print("Move to execute: ", move_to_exe)

        print()
        print('-'*50)
        print()

        initial_state.execute_move(move_to_exe)
        initial_state.draw()
        if initial_state.check_winner() != PlayerEnum.EMPTY:
            print("Winner: ", initial_state.check_winner())
            break

if __name__ == '__main__':
    g = Game(10, 10)
    play_simulation(g.state)
