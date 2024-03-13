from import_from_parent import import_from_parent
import_from_parent()

from board import PlayerEnum
from copy import deepcopy
import random
import math

def all_max(iterable, key):
    max_value = float("-inf")
    max_items = []
    for item in iterable:
        value = key(item) if key is not None else item
        if value > max_value:
            max_value = value
            max_items = [item]
        elif value == max_value:
            max_items.append(item)
    return max_items


class MonteCarloNode:
    def __init__(self, parentNode, state):
        self.total = 0
        self.visits = 0
        self.parentNode = parentNode
        self.player = PlayerEnum.WHITE
        self.children = []
        self.state = state

    def add_child(self, child, move):
        self.children.append((child, move))

    # Upper Confidence Bound 1
    def ucb1(self, c=2):
        if self.visits == 0:
            return float("inf")
        return self.total / self.visits + c * (math.log(self.visits) / self.parentNode.visits) ** 0.5

    def select_child(self):
        if self.children == []:
            return None
        if PlayerEnum.WHITE == self.player:
            return random.choice(all_max(self.children, key=lambda x: x[0].ucb1(2)))
        else:
            return random.choice(all_max(self.children, key=lambda x: x[0].ucb1(10)))
    
    def expand(self):
        state = deepcopy(state)
        moves = state.get_available_moves()

        for move in moves:
            self.add_child(MonteCarloNode(self), move)
        return random.choice(self.children)[0]
    
    def rollout(self, state):
        while state.check_winner() == PlayerEnum.EMPTY:
            state.execute_move(random.choice(state.get_available_moves()))
        return state.check_winner()
    
    def backpropagate(self, winner):
        self.visits += 1
        if winner == PlayerEnum.WHITE and self.player == PlayerEnum.WHITE:
            self.total += 1
        if self.parentNode is not None:
            self.parentNode.backpropagate(winner)
        