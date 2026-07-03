import time
import streamlit as st

from game import (
    create_board,
    make_move,
    check_winner,
    check_draw,
)

from agents import ask_gemini

from constants import *

from styles import CUSTOM_CSS

# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(

    page_title=TITLE,

    page_icon=PAGE_ICON,

    layout="wide",

)

st.markdown(

    CUSTOM_CSS,

    unsafe_allow_html=True,

)

# -------------------------------
# SESSION STATE
# -------------------------------

if "board" not in st.session_state:

    st.session_state.board = create_board()

if "turn" not in st.session_state:

    st.session_state.turn = PLAYER_X

if "winner" not in st.session_state:

    st.session_state.winner = None

if "game_over" not in st.session_state:

    st.session_state.game_over = False

if "mode" not in st.session_state:

    st.session_state.mode = "Human vs AI"

if "thinking" not in st.session_state:

    st.session_state.thinking = False
if "player_score" not in st.session_state:
    st.session_state.player_score = 0

if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0

if "draw_score" not in st.session_state:
    st.session_state.draw_score = 0
if "score_updated" not in st.session_state:
    st.session_state.score_updated = False


# -------------------------------
# RESET
# -------------------------------

def reset_game_state():

    st.session_state.board = create_board()

    st.session_state.turn = PLAYER_X

    st.session_state.winner = None

    st.session_state.game_over = False

    st.session_state.thinking = False

    st.session_state.score_updated = False

# -------------------------------
# TITLE
# -------------------------------

st.markdown("""
<div style="
background:linear-gradient(90deg,#6C63FF,#2563EB);
padding:22px;
border-radius:20px;
text-align:center;
margin-bottom:20px;
">

<h1 style="margin:0;color:white;">
🤖 AI Tic Tac Toe
</h1>

<h3 style="margin-top:8px;color:white;">
Challenge Google's Gemini AI
</h3>

<p style="margin-top:12px;font-size:18px;color:white;">
⚡ Powered by <b>Gemini 2.5 Flash</b> • Python • Streamlit
</p>

</div>
""", unsafe_allow_html=True)

st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👤 You", st.session_state.player_score)

with col2:
    st.metric("🤖 Gemini", st.session_state.ai_score)

with col3:
    st.metric("🤝 Draw", st.session_state.draw_score)

st.divider()



# -------------------------------
# HUMAN MOVE
# -------------------------------

def human_move(index):

    if st.session_state.game_over:
        return

    if st.session_state.board[index] != "":
        return

    make_move(
    st.session_state.board,
    index,
    st.session_state.turn,
)
    winner = check_winner(
        st.session_state.board
    )

    if winner:

        st.session_state.winner = winner

        st.session_state.game_over = True

        return

    if check_draw(
        st.session_state.board
    ):

        st.session_state.winner = "Draw"

        st.session_state.game_over = True

        return

    if st.session_state.mode == "Human vs AI":
     st.session_state.turn = PLAYER_O

# -------------------------------
# AI MOVE
# -------------------------------

def ai_move():

    if st.session_state.game_over:
        return

    st.session_state.thinking = True

    with st.spinner("🤖 Gemini is planning the best move..."):

        time.sleep(1)

        move = ask_gemini(
            st.session_state.board
        )

    st.session_state.thinking = False

    if move is None:

        empty = []

        for i in range(9):

            if st.session_state.board[i] == "":

                empty.append(i)

        if len(empty) == 0:
            return

        move = empty[0]

    make_move(

        st.session_state.board,

        move,

        PLAYER_O,

    )

    winner = check_winner(
        st.session_state.board
    )

    if winner:

        st.session_state.winner = winner

        st.session_state.game_over = True

        return

    if check_draw(
        st.session_state.board
    ):

        st.session_state.winner = "Draw"

        st.session_state.game_over = True

        return

    st.session_state.turn = PLAYER_X

# -------------------------------
# BOARD UI
# -------------------------------

st.subheader("🎯 Battle Arena")

for row in range(3):

    cols = st.columns(3)

    for col in range(3):

        index = row * 3 + col

        value = st.session_state.board[index]

        if value == "":
            value = "⬜"

        with cols[col]:

            if st.button(
                value,
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

                # --------------------
                # HUMAN vs AI
                # --------------------

                if st.session_state.mode == "Human vs AI":

                    human_move(index)

                    if not st.session_state.game_over:

                        ai_move()

                    st.rerun()

                # --------------------
                # HUMAN vs HUMAN
                # --------------------

                else:

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

                            if st.session_state.turn == PLAYER_X:

                                st.session_state.turn = PLAYER_O

                            else:

                                st.session_state.turn = PLAYER_X

                        st.rerun()

# -------------------------------
# RESULT
# -------------------------------
if st.session_state.game_over:

    st.subheader("🏆 Game Over")

    if st.session_state.mode == "Human vs AI":

        if st.session_state.winner == PLAYER_X:

            st.balloons()

            st.success("🎉 You Won!")

        elif st.session_state.winner == PLAYER_O:

            st.error("🤖 Gemini Won!")

        else:

            st.info("🤝 Match Draw!")

    else:

        if st.session_state.winner == "Draw":

            st.info("🤝 Match Draw!")

        else:

            st.success(f"🏆 Player {st.session_state.winner} Won!")

# -------------------------------
# RESET
# -------------------------------

st.divider()

if st.button(

    "🔄 Reset Game",

    use_container_width=True,

):

    reset_game_state()

    st.rerun()

# -------------------------------
# FOOTER
# -------------------------------

st.markdown("---")

st.caption("🚀 Built with ❤️ by Om Srivastav")

st.caption("Python • Streamlit • Gemini AI")

# -------------------------------
# SIDEBAR
# -------------------------------

with st.sidebar:

    st.header("⚙ Game Settings")

    selected_mode = st.selectbox(
        "🎮 Select Game Mode",
        [
            "Human vs AI",
            "Human vs Human",
        ],
        index=0 if st.session_state.mode == "Human vs AI" else 1,
    )

    if selected_mode != st.session_state.mode:

        st.session_state.mode = selected_mode

        reset_game_state()

        st.rerun()

    st.divider()

    st.metric(
        "Current Turn",
        st.session_state.turn,
    )

    st.metric(
        "Empty Cells",
        st.session_state.board.count(""),
    )

    st.divider()

    st.success("AI Model")
    st.write("✅ Gemini 2.5 Flash")

    st.success("Framework")
    st.write("✅ Streamlit")

    st.success("Language")
    st.write("✅ Python")