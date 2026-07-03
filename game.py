#This files includes the main game loop and the logic for running the game. 
# It handles user input, updates the game state, and renders the game to the screen.
#And the functions like create_board()

# make_move()
# check_winner()
# check_draw()
# re
# ==================set_game()
# Tic Tac Toe Game Logic
# ==========================================

WINNING_COMBINATIONS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


def create_board():
    return [""] * 9


def check_winner(board):

    for combo in WINNING_COMBINATIONS:

        a, b, c = combo

        if (
            board[a] != ""
            and board[a] == board[b]
            and board[b] == board[c]
        ):
            return board[a]

    return None


def check_draw(board):

    return "" not in board


def make_move(board, index, player):

    if board[index] == "":

        board[index] = player

        return True

    return False


def reset_game():

    return create_board()