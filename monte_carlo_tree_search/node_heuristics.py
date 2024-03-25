from node import MonteCarloNode
from player import Player
from copy import deepcopy

import random
import numpy as np

class MonteCarloNodeHeuristic(MonteCarloNode):
    def __init__(self, heuristic, parentNode, state, cWhite, cBlack):
        super().__init__(parentNode, state, cWhite, cBlack)
        self.heuristic = heuristic

    def expand(self):
        self.expanded = True
        moves = self.state.get_available_moves()
        self.children = np.empty(len(moves), dtype=object)

        for i in range(len(moves)):
            move = moves[i]
            new_state = deepcopy(self.state)
            new_state.execute_move(move)
            self.children[i] = (MonteCarloNodeHeuristic(self.heuristic, self, new_state, self.cWhite, self.cBlack), move)

        return random.choice(self.children)[0]

    def rollout(self):
        valWhite = self.heuristic.evaluate_board(self.state, Player.WHITE)
        valBlack = self.heuristic.evaluate_board(self.state, Player.BLACK)
        return (valWhite, valBlack)
    
    def backpropagate(self, valWhite, valBlack):
        self.visits += 1
        if self.player == Player.WHITE:
            self.total += valWhite - valBlack
        elif self.player == Player.BLACK:
            self.total += valBlack - valWhite
        
        if self.parentNode is not None:
            self.parentNode.backpropagate(valWhite, valBlack)

    def one_training_iteration(self):
        node = self

        while node.children.size != 0 and not node.game_finished:
            node, move = node.select_child()
        
        if not node.expanded and not node.game_finished:
            new_node = node.expand()
            node.delete_state()
            valWhite, valBlack = new_node.rollout()
            new_node.backpropagate(valWhite, valBlack)
        else:
            valWhite, valBlack = node.rollout()
            node.backpropagate(valWhite, valBlack)
