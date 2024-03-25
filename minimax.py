import random
import math
from heuristics.nr_pieces_heuristic import NrPiecesHeuristic
from heuristics.adjacent_pieces_heuristic import AdjacentPiecesHeuristic
from heuristics.heuristics_list import HeuristicsList
from heuristics.win_heuristic import WinHeuristic
from heuristics.groups_heuristic import GroupsHeuristic
from heuristics.center_control_heuristic import CenterControlHeuristic
from player import Player
from state import State


def execute_random_move(state: State) -> State:
    moves = state.get_available_moves()
    if moves == []:  # No moves available
        return state
    move = random.choice(moves)
    state = state.execute_move(move)
    return state


def minimax(state: State, depth, alpha, beta, player_to_win, evaluate_func):
    if depth == 0 or state.check_winner() != Player.EMPTY:
        return evaluate_func(state, player_to_win)

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


def execute_minimax_move(evaluate_func, depth: int) -> State:
    def execute_minimax_move_aux(state: State):
        best_state = None

        alpha = best_eval = -math.inf
        beta = math.inf
        for mv in state.get_available_moves():
            nstate = state.execute_move(mv)
            nstate_eval = minimax(
                nstate, depth - 1, alpha, beta, state.player, evaluate_func
            )

            if nstate_eval > best_eval:
                alpha = best_eval = nstate_eval
                best_state = nstate

        return best_state

    return execute_minimax_move_aux

