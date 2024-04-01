import random
import math
from moves.move import Move
from player import Player
from state import State
from typing import Callable

EPS = 1e-9

def get_random_move(state: State) -> Move | None:
    moves = state.get_available_moves()
    if moves == []:  # No moves available
        return None
    return random.choice(moves)

def execute_random_move(state: State) -> State:
    move = get_random_move(state)
    state = state.execute_move(move)
    return state


def minimax(state: State, depth, alpha, beta, player_to_win, evaluate_func: Callable[[State, Player], float]):
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


def get_minimax_move(evaluate_func, depth: int) -> Move | None:
    def get_minimax_move_aux(state: State) -> Move:
        best_moves = []

        alpha = best_eval = -math.inf
        beta = math.inf
        for mv in state.get_available_moves():
            nstate = state.execute_move(mv)
            nstate_eval = minimax(
                nstate, depth - 1, alpha, beta, state.player, evaluate_func
            )

            if nstate_eval > best_eval:
                alpha = best_eval = nstate_eval
                best_moves.clear()
                best_moves.append(mv)

            if best_eval - EPS <= nstate_eval <= best_eval + EPS:   # float equality
                best_moves.append(mv)

        if best_moves != []:
            return random.choice(best_moves)
        return None

    return get_minimax_move_aux

def execute_minimax_move(evaluate_func, depth: int) -> State:
    def execute_minimax_move_aux(state: State):
        move = get_minimax_move(evaluate_func, depth)(state)
        return state.execute_move(move)
    return execute_minimax_move_aux
