from utils import board_to_text
from prompts import SYSTEM_PROMPT

import os
from dotenv import load_dotenv
import google.generativeai as genai

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)

# -----------------------------
# Load Gemini Model
# -----------------------------
model = genai.GenerativeModel("gemini-2.5-flash")


# -----------------------------
# Ask Gemini for Best Move
# -----------------------------
def ask_gemini(board):

    prompt = f"""
{SYSTEM_PROMPT}

Current Board:

{board_to_text(board)}
"""

    try:

        response = model.generate_content(prompt)

        move = response.text.strip()

        # Sometimes Gemini returns spaces/newlines
        move = move.replace("\n", "").replace(" ", "")

        move = int(move)

        # Check valid range
        if move < 0 or move > 8:
            return None

        # Check empty position
        if board[move] != "":
            return None

        return move

    except Exception as e:

        print("Gemini Error:", e)

        return None