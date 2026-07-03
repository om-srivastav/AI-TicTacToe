import time
import streamlit as st

from game import (
    create_board,
    make_move,
    check_winner,
    check_draw,
    reset_game,
)

from agents import ask_gemini
from constants import *
from styles import CUSTOM_CSS

# ----------------------------
# Page Config
# ----------------------------

st.set_page_config(
    page_title=TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------------------
# Session State
# ----------------------------

if "board" not in st.session_state:
    st.session_state.board = create_board()

if "turn" not in st.session_state:
    st.session_state.turn = PLAYER_X

if "winner" not in st.session_state:
    st.session_state.winner = None

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "thinking" not in st.session_state:
    st.session_state.thinking = False

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "mode" not in st.session_state:
    st.session_state.mode = "Human vs AI"

# ----------------------------
# Reset
# ----------------------------

def reset():

    st.session_state.board = reset_game()

    st.session_state.turn = PLAYER_X

    st.session_state.winner = None

    st.session_state.game_over = False

    st.session_state.thinking = False

    st.session_state.game_started = False

# ----------------------------
# AI Turn
# ----------------------------

def ai_turn():

    st.session_state.thinking = True

    with st.spinner("🤖 Gemini is thinking..."):

        move = ask_gemini(st.session_state.board)

        st.write("🤖 AI Selected:", move)

        time.sleep(1)

    st.session_state.thinking = False

    if move is None:
        return

    make_move(
        st.session_state.board,
        move,
        PLAYER_O
    )

    winner = check_winner(st.session_state.board)

    if winner:
        st.session_state.winner = winner
        st.session_state.game_over = True
        return

    if check_draw(st.session_state.board):
        st.session_state.winner = "Draw"
        st.session_state.game_over = True
        return

    st.session_state.turn = PLAYER_X
# ----------------------------
# Sidebar
# ----------------------------

with st.sidebar:

    st.title("⚙ Settings")

    st.session_state.mode = st.selectbox(

        "Game Mode",

        [

            "Human vs AI",

            "Human vs Human",

        ]

    )

    st.divider()

    st.metric(
        "Current Turn",
        st.session_state.turn
    )

    st.metric(
        "Empty Cells",
        st.session_state.board.count("")
    )

# ----------------------------
# Main UI
# ----------------------------

st.title(TITLE)

st.caption(
    "Powered by Gemini AI"
)

st.divider()

if not st.session_state.game_started:

    if st.button(
        "🎮 Start Game",
        use_container_width=True
    ):

        st.session_state.game_started = True

        st.rerun()

if st.session_state.game_started:

    st.success("Game Started!")

    st.write(
        f"### Mode : {st.session_state.mode}"
    )

    if not st.session_state.game_over:

        st.info(
            f"Current Turn : {st.session_state.turn}"
        )

    st.divider()

    st.subheader("Game Board")
        # ----------------------------
    # Board
    # ----------------------------

    for row in range(3):

        cols = st.columns(3)

        for col in range(3):

            index = row * 3 + col

            symbol = st.session_state.board[index]

            if symbol == "":
                symbol = "⬜"

            with cols[col]:

                if st.button(
                    symbol,
                    key=f"cell_{index}",
                    use_container_width=True,
                    disabled=(
                        st.session_state.game_over
                        or (
                            st.session_state.mode == "Human vs AI"
                            and st.session_state.turn == PLAYER_O
                        )
                    ),
                ):

                    if make_move(
                        st.session_state.board,
                        index,
                        st.session_state.turn,
                    ):

                        winner = check_winner(
                            st.session_state.board
                        )

                        if winner:

                            st.session_state.winner = winner

                            st.session_state.game_over = True

                        elif check_draw(
                            st.session_state.board
                        ):

                            st.session_state.winner = "Draw"

                            st.session_state.game_over = True

                        else:

                            if (
                                st.session_state.mode
                                == "Human vs AI"
                            ):

                                st.session_state.turn = PLAYER_O

                            else:

                                if (
                                    st.session_state.turn
                                    == PLAYER_X
                                ):
                                    st.session_state.turn = PLAYER_O
                                else:
                                    st.session_state.turn = PLAYER_X

                        st.rerun()

    # ----------------------------
    # AI Move
    # ----------------------------

    if (
        st.session_state.mode == "Human vs AI"
        and st.session_state.turn == PLAYER_O
        and not st.session_state.game_over
    ):

        ai_turn()

        st.rerun()

    st.divider()

    # ----------------------------
    # Result
    # ----------------------------

    if st.session_state.game_over:

        if st.session_state.winner == "Draw":

            st.warning("🤝 Match Draw!")

        else:

            st.success(
                f"🏆 Winner : {st.session_state.winner}"
            )

    # ----------------------------
    # Reset
    # ----------------------------

    if st.button(
        "🔄 Reset Game",
        use_container_width=True,
    ):

        reset()

        st.rerun()