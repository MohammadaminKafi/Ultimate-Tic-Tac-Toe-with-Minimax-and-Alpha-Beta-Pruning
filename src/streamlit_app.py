import streamlit as st
import time

# Import your existing modules (same as in the original project)
from tables import uttt_table
from ai import minimax_alphaBetaPrunning

# 1) -------------- STREAMLIT PAGE CONFIG --------------
st.set_page_config(page_title="Ultimate Tic-Tac-Toe", layout="centered")

# 2) -------------- INITIALIZE SESSION STATE -----------
# We store the board and basic turn/game info in session_state (no widgets).
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

    subtable_x = i // 3  # Which subtable row
    subtable_y = j // 3  # Which subtable col
    cell_x = i % 3       # Which cell inside subtable row
    cell_y = j % 3       # Which cell inside subtable col

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
    Clear out all relevant session state for a fresh start.
    """
    st.session_state.board = uttt_table()
    st.session_state.player_turn = 'X'
    st.session_state.game_over = False


# 4) ------------- BUILD THE SIDEBAR UI ----------------
st.sidebar.header("Game Settings")

# Player type selectboxes — we let these define session_state keys directly:
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

# AI Depth Sliders — again, each slider sets a session_state key and default:
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
    st.experimental_rerun()

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

        # Create a label for the cell
        label = str(cell_value) if cell_value != 0 else " "

        # Make a clickable button if the cell is empty
        clicked = cols[j].button(
            label,
            key=f"cell_{i}_{j}",
            help=f"Subtable ({subtable_x},{subtable_y}), Cell ({cell_x},{cell_y})"
        )

        if clicked:
            if not st.session_state.game_over and cell_value == 0:
                handle_human_move(i, j)
                st.experimental_rerun()

# After the user potentially made a move, check if the game is over:
check_game_over()

# If not over and it's AI's turn, automatically make the AI move:
if not st.session_state.game_over:
    turn = st.session_state.player_turn
    if (turn == 'X' and st.session_state.player1_type == "AI") or \
       (turn == 'O' and st.session_state.player2_type == "AI"):
        handle_ai_move()
        st.experimental_rerun()
