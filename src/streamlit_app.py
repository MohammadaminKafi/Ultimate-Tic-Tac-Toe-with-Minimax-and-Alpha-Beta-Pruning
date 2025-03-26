import streamlit as st
import time
import random

# -- Workaround for older Streamlit versions that lack st.experimental_rerun() --
def rerun():
    """Force a fresh rerun by changing a query param."""
    st.experimental_set_query_params(rerun=str(random.randint(0, 9999999)))
    st.stop()

# Import your existing modules (same as in the original project)
from tables import uttt_table
from ai import minimax_alphaBetaPrunning

# 1) -------------- STREAMLIT PAGE CONFIG --------------
st.set_page_config(page_title="Ultimate Tic-Tac-Toe", layout="centered")

# 2) -------------- INITIALIZE SESSION STATE -----------
# We store the board, current turn, and game_over in session_state (no widget keys).
if 'board' not in st.session_state:
    st.session_state.board = uttt_table()  # The main Ultimate Tic-Tac-Toe board
if 'player_turn' not in st.session_state:
    st.session_state.player_turn = 'X'     # 'X' always goes first
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# 3) -------------- HELPER FUNCTIONS --------------------

def handle_human_move(i, j):
    """
    Convert the clicked cell (i, j) into:
      - subtable_x, subtable_y
      - cell_x, cell_y
    and attempt the move on st.session_state.board.
    """
    if st.session_state.game_over:
        return

    subtable_x = i // 3  # which subtable row
    subtable_y = j // 3  # which subtable col
    cell_x = i % 3       # which cell inside subtable row
    cell_y = j % 3       # which cell inside subtable col

    current_board = st.session_state.board
    turn = st.session_state.player_turn

    try:
        current_board.make_move(subtable_x, subtable_y, cell_x, cell_y, turn)
        # Switch player
        st.session_state.player_turn = 'O' if turn == 'X' else 'X'
    except Exception as e:
        st.warning(f"Illegal Move: {str(e)}")


def handle_ai_move():
    """
    Have the AI (Minimax + Alpha-Beta) choose and execute a move 
    for the current player, given the appropriate depth.
    """
    if st.session_state.game_over:
        return

    current_board = st.session_state.board
    turn = st.session_state.player_turn

    # Decide which depth to use, based on the current player
    # (Read directly from st.session_state, which is set by the slider widget)
    if turn == 'X':
        depth = st.session_state.ai_depth_player1
    else:
        depth = st.session_state.ai_depth_player2

    # Run your existing Minimax alpha-beta function
    elapsed_time, best_move, alpha, beta = minimax_alphaBetaPrunning(
        current_board, turn, depth
    )
    sub_x, sub_y, cell_x, cell_y = best_move

    # Convert that to row/col for handle_human_move
    handle_human_move(sub_x * 3 + cell_x, sub_y * 3 + cell_y)


def check_game_over():
    """
    Check if the global board is over. If so, display a message.
    """
    board = st.session_state.board
    if board.game_over:
        st.session_state.game_over = True
        if board.winner in ['X', 'O']:
            st.success(f"Game Over: Player {board.winner} wins!")
        else:
            st.info("Game Over: It's a draw!")


def restart_game():
    """
    Clear out all relevant session state for a fresh start.
    """
    st.session_state.board = uttt_table()
    st.session_state.player_turn = 'X'
    st.session_state.game_over = False


# 4) ------------- BUILD THE SIDEBAR UI ----------------
st.sidebar.header("Game Settings")

# Player type selectboxes — let these define session_state keys, no manual assignment
st.sidebar.selectbox(
    "Player 1 (X)",
    ("Human", "AI"),
    index=0,
    key="player1_type"
)

st.sidebar.selectbox(
    "Player 2 (O)",
    ("Human", "AI"),
    index=0,
    key="player2_type"
)

# AI Depth Sliders — each slider sets session_state internally.
# We'll just read from it. We do *not* do st.session_state[...] = st.sidebar.slider(...)
st.sidebar.subheader("AI Depth Settings")
st.sidebar.slider(
    "AI Depth for Player X",
    min_value=1,
    max_value=10,
    value=3,
    step=1,
    key="ai_depth_player1"
)
st.sidebar.slider(
    "AI Depth for Player O",
    min_value=1,
    max_value=10,
    value=3,
    step=1,
    key="ai_depth_player2"
)

# Restart Button
if st.sidebar.button("Restart Game"):
    restart_game()
    rerun()  # triggers a full rerun immediately

# 5) ------------- MAIN LAYOUT ---------------------
st.title("Ultimate Tic-Tac-Toe (Streamlit Version)")

current_board = st.session_state.board

# Render a 9x9 grid of cells. Each small cell is subtable_x,y, cell_x,y.
for i in range(9):
    cols = st.columns(9)
    for j in range(9):
        subtable_x = i // 3
        subtable_y = j // 3
        cell_x = i % 3
        cell_y = j % 3

        cell_value = current_board.subtable[subtable_x][subtable_y].table[cell_x][cell_y]
        label = str(cell_value) if cell_value != 0 else " "

        clicked = cols[j].button(
            label,
            key=f"cell_{i}_{j}",
            help=f"Subtable ({subtable_x},{subtable_y}), Cell ({cell_x},{cell_y})"
        )

        if clicked:
            # If the user clicked this cell, handle the move if it's empty
            if not st.session_state.game_over and cell_value == 0:
                handle_human_move(i, j)
                rerun()  # rerun after the move to update the board/AI

# After the user (or AI) might have moved, check if the game is over
check_game_over()

# If not over and it's AI's turn, make the AI move automatically
if not st.session_state.game_over:
    turn = st.session_state.player_turn
    if (turn == 'X' and st.session_state.player1_type == "AI") or \
       (turn == 'O' and st.session_state.player2_type == "AI"):
        handle_ai_move()
        rerun()  # rerun after AI move to refresh board
