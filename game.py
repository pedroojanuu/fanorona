import random
from typing import Callable

from heuristics.adjacent_pieces_heuristic import AdjacentPiecesHeuristic
from heuristics.heuristics_list import HeuristicsList
from state import State
from player import Player

class Game:
    def __init__(self, width: int = 9, height: int = 5):
        self.state = State(width, height)

    def run_ais(
        self,
        ai_white: Callable[["Game"], bool],
        ai_black: Callable[["Game"], bool],
        log_states: bool = False,
    ) -> Player:
        """
        Run the AI players in the game until it is over.

        Parameters:
        - ai_white: A function that represents the AI player for the white side. It takes a "Game" object as input and returns a boolean representing whether it has no moves.
        - ai_black: A function that represents the AI player for the black side. It takes a "Game" object as input and returns a boolean representing whether it has no moves.
        - log_states: A boolean flag indicating whether to log the game states during the AI player's moves. Default is False.

        Returns:
        - The winner of the game.
        """
        winner = None
        while not self.state.game_over() and winner is None:
            if log_states:
                self.state.draw()
            if self.state.is_white_turn():
                if ai_white(self):
                    winner = Player.BLACK
            else:
                if ai_black(self):
                    winner = Player.WHITE

        if log_states:
            self.state.draw()

        if winner is None:
            winner = self.state.check_winner()

        if log_states:
            print(f"Winner: {winner}")
        return winner


def play_simulation(initial_state: State):
    initial_state.draw()

    for i in range(50):
        # print("Available moves: ", initial_state.board.get_available_moves(initial_state.player))
        move_to_exe = random.choice(initial_state.get_available_moves())
        print()
        print("Move to execute: ", move_to_exe)

        print()
        print("-" * 50)
        print()

        initial_state.execute_move(move_to_exe)
        initial_state.draw()
        if initial_state.check_winner() != Player.EMPTY:
            print("Winner: ", initial_state.check_winner())
            break


if __name__ == "__main__":
    g = Game(10, 10)
    play_simulation(g.state)
