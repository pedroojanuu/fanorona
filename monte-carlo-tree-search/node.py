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
    def __init__(self, parentNode, state, cWhite=2, cBlack=10):
        self.total = 0
        self.visits = 0
        self.parentNode = parentNode
        self.player = PlayerEnum.WHITE
        self.children = []
        self.state = state
        self.cWhite = cWhite
        self.cBlack = cBlack
        self.game_finished = (state.check_winner() != PlayerEnum.EMPTY)
        self.expanded = False

    def add_child(self, child, move):
        self.children.append((child, move))

    # Upper Confidence Bound 1
    def ucb1(self):
        if self.visits == 0:
            return float("inf")
        if self.parentNode.player == PlayerEnum.WHITE:
            return self.total / self.visits + self.cWhite * (math.log(self.parentNode.visits) / self.visits) ** 0.5
        else:
            return self.total / self.visits + self.cBlack * (math.log(self.parentNode.visits) / self.visits) ** 0.5
        
    def select_child(self):
        if self.children == []:
            raise Exception("No children to select from")
        return random.choice(all_max(self.children, key=lambda x: x[0].ucb1()))
    
    def expand(self):
        self.expanded = True
        moves = self.state.get_available_moves()

        for move in moves:
            new_state = deepcopy(self.state)
            new_state.execute_move(move)
            self.add_child(MonteCarloNode(self, new_state, self.cWhite, self.cBlack), move)

        return random.choice(self.children)[0]
    
    def rollout(self):
        state = deepcopy(self.state)
        while state.check_winner() == PlayerEnum.EMPTY:
            # state.draw()
            state.execute_move(random.choice(state.get_available_moves()))
        return state.check_winner()
    
    def delete_state(self):
        self.state = None
    
    def backpropagate(self, winner):
        self.visits += 1
        if winner == PlayerEnum.WHITE and self.player == PlayerEnum.WHITE:
            self.total += 1
        if self.parentNode is not None:
            self.parentNode.backpropagate(winner)
        