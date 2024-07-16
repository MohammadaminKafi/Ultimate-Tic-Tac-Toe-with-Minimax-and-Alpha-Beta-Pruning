import copy
import heuristics

# code for simulating tree structure
class Node:
    def __init__(self, index, parent, board, alpha, beta):
        self.index = index
        self.parent = parent
        self.board = board
        self.alpha = alpha
        self.beta = beta
        self.children = []
        self.score = 0
        self.visits = 0
        self.best_move = None
    
    def add_child(self, child_index):
        self.children.append(child_index)

    def build_all_children_to_depth(self, player_turn, depth):
        if depth == 0:
            return
        if self.board.game_over == True:
            return
        if self.board.subtable_to_be_played == [None, None] or self.board.subtable[self.board.subtable_to_be_played[0]][self.board.subtable_to_be_played[1]].game_over == True:
            for i in range(3):
                for j in range(3):
                    if self.board.subtable[i][j].game_over == False:
                        for k in range(3):
                            for l in range(3):
                                if self.board.subtable[i][j].table[k][l] == 0:
                                    new_board = copy.deepcopy(self.board)
                                    new_board.make_move(i, j, k, l, player_turn)
                                    new_node = Node(len(self.children), self, new_board, self.alpha, self.beta)
                                    self.add_child(new_node)
                                    #print(f"On depth n - {depth}, created node {len(self.children)} for player {player_turn} at {[i, j, k, l]}")
                                    #print(f"Heuristic value for this node is {heuristics.uttt_heuristic(new_board)}")
                                    new_node.build_all_children_to_depth('X' if player_turn == 'O' else 'O', depth - 1)
        else:
            i = self.board.subtable_to_be_played[0]
            j = self.board.subtable_to_be_played[1]
            for k in range(3):
                for l in range(3):
                    if self.board.subtable[i][j].table[k][l] == 0:
                        new_board = copy.deepcopy(self.board)
                        new_board.make_move(i, j, k, l, player_turn)
                        new_node = Node(len(self.children), self, new_board, self.alpha, self.beta)
                        self.add_child(new_node)
                        #print(f"On depth n - {depth}, created node {len(self.children)} for player {player_turn} at {[i, j, k, l]}")
                        #print(f"Heuristic value for this node is {heuristics.uttt_heuristic(new_board)}")
                        new_node.build_all_children_to_depth('X' if player_turn == 'O' else 'O', depth - 1)