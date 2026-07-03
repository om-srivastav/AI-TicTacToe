def board_to_text(board):

    text = ""

    for i in range(9):

        if board[i] == "":
            text += "-"

        else:
            text += board[i]

    return text