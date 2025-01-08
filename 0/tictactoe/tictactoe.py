"""
Tic Tac Toe Player
"""

import math

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
    """
    Returns player who has the next turn on a board.
    """
    x_num = 0
    o_num = 0 
    for i in range(3):
        for j in range(3):
            if (board[i][j] == O):
                o_num += 1
            elif (board[i][j] == X):
                x_num += 1
    if (x_num <= o_num):
        return X
    else:
        return O
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = set()
    
    for i in range(3):
        for j in range(3):
            if (board[i][j] == EMPTY):
                action.add((i, j))
    return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    Nboard = initial_state()
    for i in range(3):
        for j in range(3):
            Nboard[i][j] = board[i][j]
    if (action not in actions(Nboard)):
        raise ValueError("Usnsupport action")
    else:
        Nboard[action[0]][action[1]] = player(Nboard)

    return Nboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # column
    for i in range(3):
        if (board[i][0] != EMPTY and board[i][0] == board[i][1] and board[i][1] == board[i][2]):
            return board[i][0]
    # row
    for i in range(3):
        if (board[0][i] != EMPTY and board[0][i] == board[1][i] and board[1][i] == board[2][i]):
            return board[0][i]
        
    # diag
    if (board[0][0] != EMPTY and board[0][0] == board[1][1] and board[1][1] == board[2][2]):
        return board[0][0]
    if (board[0][2] != EMPTY and board[0][2] == board[1][1] and board[1][1] == board[2][0]):
        return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    sign = True
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                sign = False
    return (winner(board) != None) or sign
        

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    now = winner(board)
    if (now == X):
        return 1
    elif (now == O):
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    def minFunc(board, pivot):
        if terminal(board):
            return utility(board)
        v = float('inf')
        for action in actions(board):
            if v < pivot:
                break
            v = min(v, maxFunc(result(board, action),v))
        return v

    def maxFunc(board, pivot):
        if terminal(board):
            return utility(board)
        v = float('-inf')
        for action in actions(board):
            if v > pivot:
                break 
            v = max(v, minFunc(result(board, action), v))
        return v

    # Determine the optimal action for the current player
    current_player = player(board)  # Get the current player
    best_action = None

    if current_player == "X":  # Maximizing player
        now = float('-inf')
        for action in actions(board):
            action_value = minFunc(result(board, action), now)
            if action_value > now:
                now = action_value
                best_action = action
    else:  # Minimizing player
        now = float('inf')
        for action in actions(board):
            action_value = maxFunc(result(board, action), now)
            if action_value < now:
                now = action_value
                best_action = action

    return best_action

