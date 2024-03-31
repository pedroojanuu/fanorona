from player import Player
from copy import deepcopy
import random
import math
import numpy as np

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
        self.children = np.array([])
        self.state = state
        self.cWhite = cWhite
        self.cBlack = cBlack
        self.game_finished = (state.check_winner() != Player.EMPTY)
        self.expanded = False
        if(state.player == Player.WHITE):
            self.player = Player.WHITE
        else:
            self.player = Player.BLACK

    def add_child(self, child, move):
        self.children.append((child, move))

    def ucb1(self):
        if self.visits == 0:
            return float("inf")
        if self.parentNode.player == Player.WHITE:
            return self.total / self.visits + self.cWhite * (math.log(self.parentNode.visits) / self.visits) ** 0.5
        else:
            return self.total / self.visits + self.cBlack * (math.log(self.parentNode.visits) / self.visits) ** 0.5
        
    def select_child(self):
        if self.children.size == 0:
            raise Exception("No children to select from")
        return max(self.children, key=lambda x: x[0].ucb1())

    def expand(self):
        self.expanded = True
        moves = self.state.get_available_moves()
        if len(moves) == 0:
            self.state = self.state.execute_move(None)
            self.Player = Player.opponent_player(self.player)
            return self

        self.children = np.empty(len(moves), dtype=object)

        for i in range(len(moves)):
            move = moves[i]
            new_state = self.state.execute_move(move)
            self.children[i] = (MonteCarloNode(self, new_state, self.cWhite, self.cBlack), move)

        return random.choice(self.children)[0]
    
    def rollout(self):
        state = self.state
        while state.check_winner() == Player.EMPTY:
            available_moves = state.get_available_moves()
            if(available_moves == []):
                move = None
            else:
                move = random.choice(available_moves)
            state = state.execute_move(move)
        return state.check_winner()
    
    def delete_state(self):
        self.state = None
    
    def backpropagate(self, winner):
        self.visits += 1
        if winner == Player.WHITE and self.player == Player.WHITE:
            self.total += 1
        elif winner == Player.BLACK and self.player == Player.BLACK:
            self.total += 1
        if self.parentNode is not None:
            self.parentNode.backpropagate(winner)

    def one_training_iteration(self):
        node = self

        while node.children.size != 0 and not node.game_finished:
            node, move = node.select_child()
        
        if node.game_finished:
            node.backpropagate(node.state.check_winner())
        elif not node.expanded:
            new_node = node.expand()
            node.delete_state()
            winner = new_node.rollout()
            new_node.backpropagate(winner)
        else:
            winner = node.rollout()
            node.backpropagate(winner)
