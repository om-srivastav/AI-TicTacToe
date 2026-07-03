import streamlit as st

from game import (
    check_winner,
    check_draw,
    create_board,
    make_move,
    reset_game,
)

from agents import ask_gemini

from constants import *

from styles import CUSTOM_CSS
# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title=TITLE,
    page_icon=PAGE_ICON,
    layout="wide"
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -------------------------
# Session State
# -------------------------
if "board" not in st.session_state:
    st.session_state.board = create_board()

if "turn" not in st.session_state:
    st.session_state.turn = "X"

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "winner" not in st.session_state:
    st.session_state.winner = None

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "mode" not in st.session_state:
    st.session_state.mode = "Human vs AI"

# -------------------------
# Reset Function
# -------------------------
def reset():
    st.session_state.board = reset_game()
    st.session_state.turn = "X"
    st.session_state.game_started = False
    st.session_state.winner = None
    st.session_state.game_over = False


# -------------------------
# UI
# -------------------------
st.title(TITLE)

st.write("Welcome to AI Tic Tac Toe!")

st.success("Environment Ready ✅")
with st.sidebar:

    st.header("⚙ Game Settings")

    st.session_state.mode = st.selectbox(

        "Select Game Mode",

        [

            "Human vs AI",

            "Human vs Human"

        ]

    )

    st.divider()

    st.metric("Current Turn", st.session_state.turn)

    st.metric(
        "Empty Cells",
        st.session_state.board.count("")
    )

# -------------------------
# Start Game
# -------------------------
if not st.session_state.game_started:

    if st.button("🎮 Start Game", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# -------------------------
# Game
# -------------------------
if st.session_state.game_started:

    st.success("Game Started 🎉")
    st.caption(
    f"🎮 Mode : {st.session_state.mode}"
)

    if not st.session_state.game_over:
        st.info(f"Current Turn : {st.session_state.turn}")

    st.divider()

    st.header("🎯 Game Board")

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
                    key=index,
                    use_container_width=True,
                    disabled=st.session_state.game_over
                ):

                    if make_move(
                        st.session_state.board,
                        index,
                        st.session_state.turn
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

                            if st.session_state.turn == "X":
                                st.session_state.turn = "O"
                            else:
                                st.session_state.turn = "X"

                        st.rerun()

    st.divider()

    if st.session_state.game_over:

        if st.session_state.winner == "Draw":

            st.warning("🤝 Match Draw!")

        else:

            st.success(
                f"🏆 Winner : {st.session_state.winner}"
            )

    if st.button(
        "🔄 Reset Game",
        use_container_width=True
    ):
        reset()
        st.rerun()