import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from board import PlayerEnum

class MonteCarloNode:
    def __init__(self, parentNode):
        self.total = 0
        self.visits = 0
        self.parentNode = parentNode
        self.player = PlayerEnum.WHITE
        self.children = []