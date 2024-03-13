from abc import abstractmethod

class Heuristic:
    @abstractmethod
    def evaluate_board(self, state, player_to_win):
        pass
