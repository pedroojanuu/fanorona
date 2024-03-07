import random
import math
from heuristics.nr_pieces_heuristic import NrPiecesHeuristic
from state import State
from player import Player
from game import Game

def execute_random_move(game: Game):
    move = random.choice(game.state.get_available_moves())
    game.state = game.state.execute_move(move)


def minimax(state, depth, alpha, beta, player_to_win, evaluate_func):
    if depth == 0 or state.check_winner() != Player.EMPTY:
        return evaluate_func(state, player_to_win)
        # evaluate_func gives the score from the perspective of player 1
        # if we are player 2, we need to invert the score

    if player_to_win == state.player:  # MAX
        max_eval = -math.inf
        for mv in state.get_available_moves():
            nstate = state.execute_move(mv)
            eval = minimax(nstate, depth - 1, alpha, beta, player_to_win, evaluate_func)
            max_eval = max(max_eval, eval)

            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval

    else:  # MIN
        min_eval = math.inf
        for mv in state.get_available_moves():
            nstate = state.execute_move(mv)
            eval = minimax(nstate, depth - 1, alpha, beta, player_to_win, evaluate_func)
            min_eval = min(min_eval, eval)

            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def execute_minimax_move(evaluate_func, depth):
    def execute_minimax_move_aux(game):
        best_state = None

        alpha = best_eval = -math.inf
        beta = math.inf
        for mv in game.state.get_available_moves():
            nstate = game.state.execute_move(mv)
            nstate_eval = minimax(nstate, depth - 1, alpha, beta, game.state.player, evaluate_func)

            if nstate_eval > best_eval:
                alpha = best_eval = nstate_eval
                best_state = nstate

        game.state = best_state

    return execute_minimax_move_aux


if __name__ == "__main__":
    for _ in range(1):
        game = Game()
        game.run_ais(execute_random_move, execute_random_move, log_states=True)
    # execute_minimax_move(NrPiecesHeuristic().evaluate_board, 2)
