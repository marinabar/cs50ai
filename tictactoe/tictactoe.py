"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    if board == initial_state():
        return X
    Xboard_count = board[0].count(X) + board[1].count(X) + board[2].count(X) + board[0].count(O) + board[1].count(O) + board[2].count(O)
    if Xboard_count % 2 == 1:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = ()
    act1 = list(action)
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                act1.append((i, j))

    action = tuple(act1)

    return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("this action is not a valid action")

    dcopb = copy.deepcopy(board)
    dcopb[action[0]][action[1]] = player(board)

    return dcopb


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for x in range(3):
        if board[x][0] == board[x][1] == board[x][2] != EMPTY:
            return board[x][0]
    for y in range(3):
        if board[0][y] == board[1][y] == board[2][y] != EMPTY:
            return board[0][y]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[2][0] == board[1][1] == board[0][2] != EMPTY:
        return board[2][0]
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X:
        return True
    elif winner(board) == O:
        return True

    for x in range(3):
        for y in range(3):
            if board[x][y] is None:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        v = -math.inf
        for one in actions(board):
            temp = MinValue(result(board, one))
            if temp > v:
                v = temp
                best = one
    else:
        v = math.inf
        for one in actions(board):
            temp = MaxValue(result(board, one))
            if temp < v:
                v = temp
                best = one
    return best
    

def MaxValue(board):

    if terminal(board):
        return utility(board)

    v = -math.inf
    for one in actions(board):
        value = MinValue(result(board, one))
        v = max(v, value)
        if v == 1:
            break
    return v


def MinValue(board):

    if terminal(board):
        return utility(board)

    v = math.inf

    for one in actions(board):
        value = MaxValue(result(board, one))
        v = min(v, value)
        if v == -1:
            break
    return v
