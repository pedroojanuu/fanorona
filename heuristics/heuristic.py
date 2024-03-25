from abc import ABC, abstractmethod

class Heuristic(ABC):
    @abstractmethod
    def evaluate_board(self, state, player_to_win):
        pass
