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

    def set_root_value(self, value):
        self.root.total = value

    def get_root_value(self):
        return self.root.total
    
    def save_to_disk(self, path):
        with open(path, 'wb') as file:
            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_from_disk(path):
        with open(path,  "rb") as f:
            return pickle.load(f)
    

if __name__ == '__main__':
    mcts = MonteCarloTree()
    mcts.set_root_value(15)
    mcts.save_to_disk("mcts_test")

    mcts2 = MonteCarloTree.load_from_disk("mcts_test")

    print(mcts2.get_root_value())
