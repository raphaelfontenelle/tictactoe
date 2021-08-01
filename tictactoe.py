"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

MAX = 1
MIN = -1


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for i in board:
        for j in i:
            if j != EMPTY:
                count += 1

    if count % 2 == 1:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row, cell = action
    new_board = copy.deepcopy(board)

    if new_board[row][cell] != EMPTY:
        raise Exception("Invalid action.")
    else:
        new_board[row][cell] = player(board)
    return new_board

def get_columns(board):
    columns = []
    for i in range(3):
        columns.append([row[i] for row in board])
    return columns

def get_diagonals(board):
    return [[board[0][0], board[1][1], board[2][2]],
            [board[0][2], board[1][1], board[2][0]]]

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    rows = board + get_columns(board) + get_diagonals(board)
    for row in rows:
        if row[0] is not None and three_in_a_row(row):
            return row[0]

    # Return None if there is no winner
    return None

def three_in_a_row(row):
    return row.count(row[0]) == 3

def all_cells_filled(board):
    for i in board:
        for j in i:
            if j == EMPTY:
                return False
    return True

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or all_cells_filled(board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    value = winner(board)
    if value == X:
        return MAX
    elif value == O:
        return MIN
    else:
        return 0

def max_value(board, a, b):
    """
    Returns max utility value for a given state.
    """
    value = MIN

    # If game is over, return utility
    if terminal(board):
        return utility(board)

    # Search lower nodes and return max utility (v)
    for action in actions(board):
        value = max(value, min_value(result(board, action), a, b))
        alpha = max(value, a)  # Update alpha if current utility is higher

        # Stop if maximizer's best guaranteed utility (alpha) equals/exceeds minimizer's at current node
        if b <= a:
            break

    return value

def min_value(board, a, b):
    """
    Returns min utility value for a given state.
    """
    value = MAX

    # If game is over, return utility
    if terminal(board):
        return utility(board)

    # Search lower nodes and return min utility (v)
    for action in actions(board):
        value = min(value, max_value(result(board, action), a, b))
        b = min(value, b)  # Update beta if current utility is lower

        # Stop if minimizer's best guaranteed utility (beta) equals/is lower than maximizer's at current node
        if b <= a:
            break

    return value

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    turn = player(board)
    move = None
    a = MIN
    b = MAX

    if turn == X:

        value = MIN
        for action in actions(board):
            new_v = min_value(result(board, action), a, b)
            a = max(new_v, a)


            if new_v > value:
                move = action
                value = new_v

            if b <= a:
                break

    else:

        value = MAX
        for action in actions(board):
            new_v = max_value(result(board, action), a, b)
            b = min(new_v, b)  # Update beta if current utility is lower

            if new_v < value:
                move = action
                value = new_v

            if b <= a:
                break

    return move
