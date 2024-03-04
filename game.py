from heuristics.adjacent_pieces_heuristic import AdjacentPiecesHeuristic
from heuristics.heuristics_list import HeuristicsList
from state import State
from board import PlayerEnum

from board import Board, opponent_player, PlayerEnum
class Game:
    def __init__(self):
        self.state = State()

def play_simulation(initial_state: State):
    initial_state.draw()

    for i in range(20):
        # print("Available moves: ", initial_state.board.get_available_moves(initial_state.player))
        move_to_exe = initial_state.get_available_moves()[0]
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
    g = Game()
    play_simulation(g.state)
