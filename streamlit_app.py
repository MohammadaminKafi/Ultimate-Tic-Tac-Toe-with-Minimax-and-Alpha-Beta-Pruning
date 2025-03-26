import streamlit as st
import time

# Import your existing modules (same as in the original project)
from src.tables import uttt_table
from src.ai import minimax_alphaBetaPrunning

# 1) -------------- STREAMLIT PAGE CONFIG --------------
st.set_page_config(page_title="Ultimate Tic-Tac-Toe", layout="centered")

# 2) -------------- INITIALIZE SESSION STATE -----------
# We store the game state and user settings in Streamlit's session_state
if 'board' not in st.session_state:
    st.session_state.board = uttt_table()  # The main Ultimate Tic-Tac-Toe board
if 'player_turn' not in st.session_state:
    st.session_state.player_turn = 'X'     # 'X' always goes first
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# Default: both players set to "Human"; AI depths
if 'player1_type' not in st.session_state:
    st.session_state.player1_type = "Human"
if 'player2_type' not in st.session_state:
    st.session_state.player2_type = "Human"
if 'ai_depth_player1' not in st.session_state:
    st.session_state.ai_depth_player1 = 3
if 'ai_depth_player2' not in st.session_state:
    st.session_state.ai_depth_player2 = 3


# 3) -------------- HELPER FUNCTIONS --------------------

def handle_human_move(i, j):
    """
    Convert the clicked cell (i, j) into:
      - subtable_x, subtable_y
      - cell_x, cell_y
    and attempt the move.
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
        current_board.make_move(
            subtable_x,
            subtable_y,
            cell_x,
            cell_y,
            turn
        )
        # Switch player
        st.session_state.player_turn = 'O' if turn == 'X' else 'X'
    except Exception as e:
        st.warning(f"Illegal Move: {str(e)}")


def handle_ai_move():
    """
    Have the AI (Minimax + Alpha-Beta) choose and execute a move for the current player.
    """
    if st.session_state.game_over:
        return

    current_board = st.session_state.board
    turn = st.session_state.player_turn

    # Decide which depth to use, based on the current player
    if turn == 'X':
        depth = st.session_state.ai_depth_player1
    else:
        depth = st.session_state.ai_depth_player2

    # Run your existing Minimax alpha-beta function
    elapsed_time, best_move, alpha, beta = minimax_alphaBetaPrunning(
        current_board, turn, depth
    )

    # best_move is typically [subtable_x, subtable_y, cell_x, cell_y]
    sub_x, sub_y, cell_x, cell_y = best_move

    # Convert that to the same "pos" style logic
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
    Clear out all session state for a fresh start.
    """
    st.session_state.board = uttt_table()
    st.session_state.player_turn = 'X'
    st.session_state.game_over = False


# 4) ------------- BUILD THE SIDEBAR UI ----------------
st.sidebar.header("Game Settings")

# Player 1 type
player1_type = st.sidebar.selectbox(
    "Player 1 (X)",
    ("Human", "AI"),
    index=0,
    key='player1_type'
)

# Player 2 type
player2_type = st.sidebar.selectbox(
    "Player 2 (O)",
    ("Human", "AI"),
    index=0,
    key='player2_type'
)

# AI Depth Sliders
st.sidebar.subheader("AI Depth Settings")
st.session_state.ai_depth_player1 = st.sidebar.slider(
    "AI Depth for Player X",
    min_value=1, max_value=10,
    value=st.session_state.ai_depth_player1,
    step=1,
    key='ai_depth_player1'
)
st.session_state.ai_depth_player2 = st.sidebar.slider(
    "AI Depth for Player O",
    min_value=1, max_value=10,
    value=st.session_state.ai_depth_player2,
    step=1,
    key='ai_depth_player2'
)

# Restart Button
if st.sidebar.button("Restart Game"):
    restart_game()
    st.experimental_rerun()

st.title("Ultimate Tic-Tac-Toe (Streamlit Version)")

# 5) ------------- RENDER THE BOARD ---------------------
# We will create a 9x9 "grid" of buttons or placeholders
# Each small cell belongs to a sub-board.
#
# The sub-boards are 3x3 of 3x3 cells = total 9x9 cells.

current_board = st.session_state.board

# Draw row by row
for i in range(9):
    cols = st.columns(9)  # 9 columns in the row
    for j in range(9):
        subtable_x = i // 3
        subtable_y = j // 3
        cell_x = i % 3
        cell_y = j % 3

        cell_value = current_board.subtable[subtable_x][subtable_y].table[cell_x][cell_y]

        # Make a label for the cell
        if cell_value == 0:
            label = " "  # Empty
        else:
            label = str(cell_value)

        # Highlight subtable if needed
        subtable_required = current_board.subtable_to_be_played
        highlight = False
        if subtable_required != [None, None]:
            # highlight the required subtable
            if subtable_x == subtable_required[0] and subtable_y == subtable_required[1]:
                highlight = True

        # We can use st.button or st.write with Markdown (for coloring).
        # For simplicity, we just show a button. If it's clicked and empty => handle move.
        button_clicked = cols[j].button(
            label,
            key=f"cell_{i}_{j}",
            help=f"Subtable ({subtable_x},{subtable_y}), Cell ({cell_x},{cell_y})",
            # You can attempt some styling or just rely on default
        )

        if button_clicked:
            # If this cell is empty and it's not game over, let the human move
            if not st.session_state.game_over and cell_value == 0:
                handle_human_move(i, j)
                st.experimental_rerun()

# After the board is rendered, let’s see if we need an AI move.
# If it’s AI’s turn, handle it automatically.
if not st.session_state.game_over:
    turn = st.session_state.player_turn
    if (turn == 'X' and st.session_state.player1_type == "AI") or \
       (turn == 'O' and st.session_state.player2_type == "AI"):
        handle_ai_move()
        st.experimental_rerun()

# Check if the game ended after a move
check_game_over()
