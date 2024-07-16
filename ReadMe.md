# Ultimate Tic-Tac-Toe with Minimax and Alpha-Beta Pruning

This project is a Python implementation of the Ultimate Tic-Tac-Toe game using Pygame, featuring an AI that employs the Minimax algorithm with Alpha-Beta Pruning.

## Concept

**Ultimate Tic-Tac-Toe** is a 3x3 grid of 3x3 tic-tac-toe boards. Players take turns playing on the smaller boards, aiming to win three in a row on the larger board. The cell a player picks on a smaller board dictates which smaller board the opponent must play on next. The game ends when a player wins three smaller boards in a row, or all smaller boards are full without a winner.

## Code Structure

### `main.py`
The main entry point for the game. It handles:
- Game initialization and Pygame setup
- Handling player clicks and moves
- Drawing the game board and updating the display
- Logging game moves for later visualization
- AI move calculations using the Minimax algorithm with Alpha-Beta Pruning

### `heuristics.py`
Defines the heuristic function used by the AI to evaluate board states. The heuristic function assigns a numerical value to a given board state, which helps the AI determine the most advantageous moves. Key metrics used in the heuristic include:

- **Number of Subtables Won/Lost**: Counts how many subtables have been won or lost by each player.
- **Total Number of Subtables Played**: Tracks the number of subtables that have been played.
- **Subtable to Be Played Is Over**: Checks if the subtable to be played is already over.
- **Number of Potential Wins/Losses in Subtables**: Evaluates the potential for winning or losing in the subtables.
- **Potential Win/Loss in the Table**: Assesses the potential for winning or losing in the entire board.
- **Value of Each Cell**: Assigns values to cells based on their positions (center, corners, edges).

These metrics are weighted and combined to form the heuristic value, which the AI uses to make decisions. For example:
- **Subtables Won/Lost**: Winning subtables increases the score significantly, while losing decreases it.
- **Potential Wins/Losses**: Having multiple potential wins in subtables or the main table positively impacts the score.
- **Cell Values**: Central cells are given higher values, as controlling the center is typically advantageous.

The heuristic function ensures that the AI not only aims to win but also considers various strategic factors to maximize its chances of success.

### Other Key Files

- **`ai.py`**: Implements the Minimax algorithm with Alpha-Beta Pruning to determine the best moves for the AI.
- **`node.py`**: Contains classes that represent the game state and nodes for the Minimax algorithm.
- **`tables.py`**: Manages the game board, including sub-board logic and move validation.

### `logs` Directory
Stores game logs that can be replayed or visualized later to analyze gameplay or debug the AI.
