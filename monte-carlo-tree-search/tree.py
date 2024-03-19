from import_from_parent import import_from_parent
import_from_parent()

from node import MonteCarloNode
from state import State
from board import PlayerEnum
import pickle
import time
import random

class MonteCarloTree:
    def __init__(self, boardWidth, boardHeight, cWhite=2, cBlack=2):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.state = State(boardWidth, boardHeight)
        self.root = MonteCarloNode(None, State(boardWidth, boardHeight), cWhite, cBlack)
        self.currNode = self.root
    
    def save_to_disk(self, path):
        with open(path, 'wb') as file:
            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_from_disk(path):
        with open(path,  "rb") as f:
            return pickle.load(f)

    def print_tree(self):
        self.print_tree_aux(self.root, 0)
    
    def print_tree_aux(self, node, depth):
        print(" " * 4*depth, "t:", node.total, "v:", node.visits)
        for child, move in node.children:
            print(" " * depth)
            self.print_tree_aux(child, depth + 1)

    def train(self, iterations):
        for _ in range(iterations):
            self.currNode.one_training_iteration()

    def train_time(self, timeout):
        start = time.time()
        while time.time() - start < timeout:
            self.currNode.one_training_iteration()

    def train_until(self, total_iterations):
        while self.currNode.visits < total_iterations:
            self.currNode.one_training_iteration()
        
    def get_best_move(self):
        if self.currNode == None or self.currNode.children.size == 0:
        # if self.currNode == None or self.currNode.children == []:
            print("Random move")
            return random.choice(self.state.get_available_moves())
        
        best_move = None
        best_score = float("-inf")
        found = False
        print(self.currNode.children)
        for child, move in self.currNode.children:
            if child.visits == 0 and not found:
                best_move = move
                found = True
            elif child.visits != 0 and child.total / child.visits > best_score:
                best_score = child.total / child.visits
                best_move = move
                found = True
        
        return best_move
    
    def update_move(self, move_to_exe):
        if self.currNode == None or self.currNode.children.size == 0:
        # if self.currNode == None or self.currNode.children == []:
            self.state.execute_move(move_to_exe)
            return
            
        for child, move in self.currNode.children:
            if move == move_to_exe:
                self.currNode = child
                self.state.execute_move(move)
                return
            
        print("Player: ", self.state.player)
        print("Children: ", self.currNode.children)
        raise Exception("Move not found: ", move_to_exe, " in children: ", self.currNode.children)
    
    def reset_game(self):
        self.state = State(self.boardWidth, self.boardHeight)
        self.currNode = self.root
    

def play_simulation(state: State, mcts: MonteCarloTree):
    state.draw()

    for i in range(50):
        # print("Available moves: ", state.board.get_available_moves(state.player))
        if state.player == PlayerEnum.WHITE:
            mcts.train_until(100)
            move_to_exe = mcts.get_best_move()
            # print(mcts.currNode.children)
            print("Best move: ", move_to_exe)
        else:
            print("Available moves: ", state.get_available_moves())
            move_to_exe = random.choice(state.get_available_moves())
        print()
        print("Move to execute: ", move_to_exe)

        print()
        print('-'*50)
        print()

        state.execute_move(move_to_exe)
        state.draw()

        mcts.update_move(move_to_exe)
        mcts.state.draw()
        
        if state.check_winner() != PlayerEnum.EMPTY:
            print("Winner: ", state.check_winner())
            break

if __name__ == '__main__':
    # mcts = MonteCarloTree.load_from_disk("test.mcts")
    #mcts.train(100000)
    # mcts.print_tree()
    #mcts.save_to_disk("test.mcts")
    # mcts = MonteCarloTree.load_from_disk("test.mcts")
    # play_simulation(State(), mcts)
    # mcts.state.draw()
    # for i in range(10):
    #     move = mcts.get_best_move()
    #     mcts.update_move(move)
    #     mcts.state.draw()
    #     print(mcts.state.get_available_moves())
    #     print(mcts.currNode.children)

    start = time.time()

    mcts = MonteCarloTree(9, 5, 2, 10)
    # mcts.train_time(5)
    mcts.print_tree()
    play_simulation(State(9, 5), mcts)

    print("Time: ", time.time() - start)

