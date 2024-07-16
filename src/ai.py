import time
import copy
from node import Node
from tables import uttt_table
import heuristics

# function for a minimax algorithm with alpha-beta prunning to play ultimate tic-tac-toe
# inputs are the current board, the current player and the depth of the search
# outputs are the move, the score of the move, the number of nodes visited and the time taken
def minimax_alphaBetaPrunning(board, player, depth):
    start_time = time.time()

    # copy the board to avoid changing the original board
    original_board = copy.deepcopy(board)
    
    root = Node(None, None, original_board, -1000000, 1000000)
    best_move(root, player, depth)
    #print(f"best move is {root.best_move} with value {root.alpha if player == 'X' else root.beta}")

    elapsed_time = time.time() - start_time
    return elapsed_time, root.best_move, root.alpha, root.beta

# function to return best move for a given board and player and depth, recursively
def best_move(root, player, depth):
    # X is maximizing
    # O is minimizing

    # branching factor equals 81
    if root.board.subtable_to_be_played == [None, None] or root.board.subtable[root.board.subtable_to_be_played[0]][root.board.subtable_to_be_played[1]].game_over == True:
        for i in range(3):
            for j in range(3):
                if root.board.subtable[i][j].game_over == False:
                    for k in range(3):
                        for l in range(3):
                            if root.board.subtable[i][j].table[k][l] == 0:
                                new_board = copy.deepcopy(root.board)
                                new_board.make_move(i, j, k, l, player)
                                new_node = Node(len(root.children), root, new_board, root.alpha, root.beta)
                                root.add_child(new_node)
                                #print(f"On depth n - {depth}, created node {len(root.children)} for player {player} at {[i, j, k, l]}")
                                if depth - 1 != 0 and new_board.game_over == False:
                                    best_move(new_node, 'X' if player == 'O' else 'O', depth - 1)
                                    if player == 'X':
                                        pre_alpha = root.alpha
                                        root.alpha = max(root.alpha, new_node.alpha, new_node.beta)
                                        if pre_alpha != root.alpha:
                                            root.best_move = [i, j, k, l]
                                    else:
                                        pre_beta = root.beta
                                        root.beta = min(root.beta, new_node.alpha, new_node.beta)
                                        if pre_beta != root.beta:
                                            root.best_move = [i, j, k, l]
                                else:
                                    value = heuristics.uttt_heuristic(new_board)
                                    if player == 'X':
                                        pre_alpha = root.alpha
                                        root.alpha = max(root.alpha, value)
                                        if pre_alpha != root.alpha:
                                            root.best_move = [i, j, k, l]
                                    else:
                                        pre_beta = root.beta
                                        root.beta = min(root.beta, value)
                                        if pre_beta != root.beta:
                                            root.best_move = [i, j, k, l]
                                
                                if root.alpha >= root.beta:
                                    #print(f"Prunned at node {root.index} with alpha {root.alpha} and beta {root.beta}")
                                    return
                                
    # branching factor equals 9
    else:
        for k in range(3):
            for l in range(3):
                if root.board.subtable[root.board.subtable_to_be_played[0]][root.board.subtable_to_be_played[1]].table[k][l] == 0:
                    new_board = copy.deepcopy(root.board)
                    new_board.make_move(root.board.subtable_to_be_played[0], root.board.subtable_to_be_played[1], k, l, player)
                    new_node = Node(len(root.children), root, new_board, root.alpha, root.beta)
                    root.add_child(new_node)
                    #print(f"On depth n - {depth}, created node {len(root.children)} for player {player} at {[root.board.subtable_to_be_played[0], root.board.subtable_to_be_played[1], k, l]}")
                    if depth - 1 != 0 and new_board.game_over == False:
                        best_move(new_node, 'X' if player == 'O' else 'O', depth - 1)
                        if player == 'X':
                            pre_alpha = root.alpha
                            root.alpha = max(root.alpha, new_node.alpha, new_node.beta)
                            if pre_alpha != root.alpha:
                                root.best_move = [root.board.subtable_to_be_played[0], root.board.subtable_to_be_played[1], k, l]
                        else:
                            pre_beta = root.beta
                            root.beta = min(root.beta, new_node.alpha, new_node.beta)
                            if pre_beta != root.beta:
                                root.best_move = [root.board.subtable_to_be_played[0], root.board.subtable_to_be_played[1], k, l]
                    else:
                        value = heuristics.uttt_heuristic(new_board)
                        if player == 'X':
                            pre_alpha = root.alpha
                            root.alpha = max(root.alpha, value)
                            if pre_alpha != root.alpha:
                                root.best_move = [root.board.subtable_to_be_played[0], root.board.subtable_to_be_played[1], k, l]
                        else:
                            pre_beta = root.beta
                            root.beta = min(root.beta, value)
                            if pre_beta != root.beta:
                                root.best_move = [root.board.subtable_to_be_played[0], root.board.subtable_to_be_played[1], k, l]
                    
                    if root.alpha >= root.beta:
                        #print(f"Prunned at node {root.index} with alpha {root.alpha} and beta {root.beta}")
                        return

    return


if __name__ == "__main__":
    uttt = uttt_table()
    uttt.print_table()
    # make some moves
    uttt.make_move(0, 0, 0, 0, 'X')
    uttt.make_move(0, 0, 1, 1, 'O')
    uttt.make_move(1, 1, 2, 2, 'X')
    uttt.make_move(2, 2, 0, 2, 'O')
    uttt.make_move(0, 2, 0, 0, 'X')
    uttt.make_move(0, 0, 1, 0, 'O')
    uttt.make_move(1, 0, 2, 0, 'X')

    print(minimax_alphaBetaPrunning(uttt, 'O', 5))

    