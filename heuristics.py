from state import State, PlayerEnum
from board import Board, opponent_player
import numpy as np
from enum import Enum



# class MobilityHeuristic(Heuristic):
#     def evaluate_board(self, state, player_to_win):
#         return len(state.board.moves(player_to_win)) - len(state.board.moves(opponent_player(player_to_win)))

# class HeuristicList(Heuristic):
#     def __init__(self, heuristics, weights):
#         self.heuristics = heuristics

#     def evaluate_board(self, state, player_to_win):
#         return sum(self.heuristics.evaluate_board(state, player_to_win) * self.weights)


# class HeuristicDecorator(Heuristic):
#     def __init__(self, heuristic, weight):
#         self.heuristic = heuristic
#         self.weight = weight

#     def evaluate_board(self, state, player_to_win):
#         return self.weight * self.heuristic.evaluate_board(state, player_to_win)


