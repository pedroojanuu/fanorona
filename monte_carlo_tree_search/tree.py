if __name__ == '__main__':
    from import_from_parent import import_from_parent
    import_from_parent()

from monte_carlo_tree_search.node import MonteCarloNode
from state import State
from player import Player
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
        while time.time() - start < timeout and not all([child.visits != 0 for child, _ in self.currNode.children]):
            self.currNode.one_training_iteration()

    def train_until(self, total_iterations):
        while self.currNode.visits < total_iterations:
            self.currNode.one_training_iteration()
        
    def get_best_move(self):
        best_move = None
        best_score = float("-inf")
        found = False
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
        if not self.currNode.expanded:
            self.currNode.expand()
            
        for child, move in self.currNode.children:
            if move == move_to_exe:
                print("--------------- Update move: ", move_to_exe)
                self.currNode = child
                self.state = self.state.execute_move(move_to_exe)
                return
            
        print("Player: ", self.state.player)
        print("Children: ", self.currNode.children)
        self.currNode.state.draw()
        raise Exception("Move not found: ", move_to_exe, " in children: ", self.currNode.children)
    
    def reset_game(self):
        self.state = State(self.boardWidth, self.boardHeight)
        self.currNode = self.root
    

def play_simulation(state: State, mcts: MonteCarloTree, no_rollouts=100):
    state.draw()

    while True:
        if state.player == Player.WHITE:
            mcts.train_until(no_rollouts)
            move_to_exe = mcts.get_best_move()
            if(move_to_exe not in state.get_available_moves()):
                mcts.currNode.parentNode.state.draw()
                raise Exception("Invalid move: ", move_to_exe, " in ", state.get_available_moves())
            print("Best move: ", move_to_exe)
        else:
            print("Available moves: ", state.get_available_moves())
            move_to_exe = random.choice(state.get_available_moves())
        print()
        print("Move to execute: ", move_to_exe)

        print()
        print('-'*50)
        print()

        state = state.execute_move(move_to_exe)
        state.draw()

        mcts.update_move(move_to_exe)
        mcts.state.draw()
        mcts.currNode.state.draw()
        
        if state.check_winner() != Player.EMPTY:
            print("Winner: ", state.check_winner())
            break

if __name__ == '__main__':
    start = time.time()

    mcts = MonteCarloTree(5, 5, 2, 10)
    # mcts.train_time(5)
    mcts.print_tree()
    play_simulation(State(5, 5), mcts)

    print("Time: ", time.time() - start)


