from heuristics.AdjacentPiecesHeuristic import AdjacentPiecesHeuristic
from heuristics.HeuristicList import HeuristicList

from board import Board, opponent_player, PlayerEnum
class Game:
    def __init__(self):
        self.board = Board()
        self.player = PlayerEnum.BLACK
    
    def change_player(self):
        self.player = opponent_player(self.player)

    def play(self):
        pass

