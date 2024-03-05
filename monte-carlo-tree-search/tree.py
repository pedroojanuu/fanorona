import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from node import MonteCarloNode
from state import State
import pickle

class MonteCarloTree:
    def __init__(self):
        self.root = MonteCarloNode(None)
        self.state = State()
    
    def save_to_disk(self, path):
        with open(path, 'wb') as file:
            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_from_disk(path):
        with open(path,  "rb") as f:
            return pickle.load(f)
        
    def one_training_iteration(self):
        node = self.root
        move = None
        state = self.state
        while node.children != []:
            node, move = node.select_child()
            if state.execute_move(move) == None:
                print(move)
                state.draw()
                print(state.get_available_moves())
            state = state.execute_move(move)
        if node.visits > 0:
            node = node.expand(state)
            winner = node.rollout(state)
            node.backpropagate(winner)
        else:
            winner = node.rollout(state)
            node.backpropagate(winner)

    def print_tree(self):
        self.print_tree_aux(self.root, 0)
    
    def print_tree_aux(self, node, depth):
        print(" " * 4*depth, "t:", node.total, "v:", node.visits)
        for child, move in node.children:
            print(" " * depth)
            self.print_tree_aux(child, depth + 1)

    def train(self, iterations):
        for _ in range(iterations):
            self.one_training_iteration()
            self.state = State()
    

if __name__ == '__main__':
    mcts = MonteCarloTree()
    mcts.train(2)
    mcts.print_tree()
