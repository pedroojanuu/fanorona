from state import State
from typing import Callable
from player import Player

class GameSimulator:
    def __init__(self, width: int = 9, height: int = 5):
        self.state = State(width, height)

    def run_ais(
        self,
        ai_white: Callable[["GameState"], bool],
        ai_black: Callable[["GameState"], bool],
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

