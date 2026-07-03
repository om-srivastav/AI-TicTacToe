from operator import index
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
        PLAYER_X,
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

    ...

# -------------------------------
# AI vs AI ENGINE
# -------------------------------

if (
    st.session_state.mode == "AI vs AI"
    and st.session_state.auto_play
    and not st.session_state.game_over
):

    time.sleep(0.8)

    ai_vs_ai_move()

    st.rerun()
                        # -------------------------------
# RESULT
# -------------------------------

st.divider()

if st.session_state.game_over:

    if not st.session_state.score_updated:

        if st.session_state.winner == PLAYER_X:

            st.session_state.player_score += 1

        elif st.session_state.winner == PLAYER_O:

            st.session_state.ai_score += 1

        else:

            st.session_state.draw_score += 1

        st.session_state.score_updated = True

    if st.session_state.winner == PLAYER_X:

        st.balloons()
        st.success("🎉 You Won!")

    elif st.session_state.winner == PLAYER_O:

        st.error("🤖 Gemini Won!")

    else:

        st.info("🤝 Match Draw!")

else:

    if st.session_state.mode == "Human vs AI":

        if st.session_state.turn == PLAYER_X:

            st.success("🟢 Your Turn")

        else:

           st.warning("🤖 Gemini is Planning...")

    else:

        st.info(
            f"Current Turn : {st.session_state.turn}"
        )

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

    st.session_state.mode = st.selectbox(
    "🎮 Select Game Mode",
    [
        "Human vs AI",
        "Human vs Human",
    ]
)

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