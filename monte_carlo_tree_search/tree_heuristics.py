if __name__ == '__main__':
    from import_from_parent import import_from_parent
    import_from_parent()

from monte_carlo_tree_search.tree import MonteCarloTree, play_simulation
from monte_carlo_tree_search.node_heuristics import MonteCarloNodeHeuristic
from state import State
from player import Player
import time

from heuristics.heuristics_list import HeuristicsList
from heuristics.win_heuristic import WinHeuristic
from heuristics.nr_pieces_heuristic import NrPiecesHeuristic
from heuristics.adjacent_pieces_heuristic import AdjacentPiecesHeuristic
from heuristics.groups_heuristic import GroupsHeuristic
from heuristics.center_control_heuristic import CenterControlHeuristic
import numpy as np

class MonteCarloTreeHeuristic(MonteCarloTree):
    def __init__(self, heuristic, boardWidth, boardHeight, cWhite=2, cBlack=2):
        super().__init__(boardWidth, boardHeight, cWhite, cBlack)
        self.root = MonteCarloNodeHeuristic(heuristic, None, State(boardWidth, boardHeight), cWhite, cBlack)
        self.currNode = self.root
        self.heuristic = heuristic
    
    @classmethod
    def from_player(self, heuristic, boardWidth, boardHeight, player):
        if player == Player.WHITE:
            return MonteCarloTreeHeuristic(heuristic, boardWidth, boardHeight, 2, 10)
        else:
            return MonteCarloTreeHeuristic(heuristic, boardWidth, boardHeight, 10, 2)

    def train_until(self, total_iterations):
        while self.currNode.visits < total_iterations:
            self.currNode.one_training_iteration()

    def reset_game(self):
        self.state = State(self.boardWidth, self.boardHeight)
        self.root = MonteCarloNodeHeuristic(self.heuristic, None, State(self.boardWidth, self.boardHeight), self.cWhite, self.cBlack)
        self.currNode = self.root

if __name__ == '__main__':
    start = time.time()

    h = HeuristicsList(
        heuristics=np.array([
            WinHeuristic(),
            NrPiecesHeuristic(),
            GroupsHeuristic(),
            CenterControlHeuristic(),
        ]),
        weights=np.array([100000, 50, 10, 5]),
    )

    mctsh = MonteCarloTreeHeuristic(heuristic=h, boardWidth=10, boardHeight=10, cWhite=2, cBlack=10)
    # mcts.train_time(5)
    play_simulation(State(10, 10), mctsh, 1000)

    print("Time: ", time.time() - start)




