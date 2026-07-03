from agents import ask_gemini

board = [
    "X", "", "",
    "", "O", "",
    "", "", "X"
]

move = ask_gemini(board)

print("AI Move :", move)