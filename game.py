from heuristics.adjacent_pieces_heuristic import AdjacentPiecesHeuristic
from heuristics.heuristics_list import HeuristicsList
from state import State
from player import Player
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
        if initial_state.check_winner() != Player.EMPTY:
            print("Winner: ", initial_state.check_winner())
            break

    def run(self, ai_white, ai_black):
        while not self.state.game_over():
            if self.state.is_white_turn():
                ai_white(self.state)
            else:
                ai_black(self.state)

        print("Winner: ", self.state.check_winner())


if __name__ == '__main__':
    g = Game(10, 10)
    play_simulation(g.state)
