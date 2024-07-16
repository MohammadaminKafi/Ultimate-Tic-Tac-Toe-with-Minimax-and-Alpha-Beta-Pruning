# class for the table of an ultimate tic-tac-toe game
class uttt_table:
    def __init__(self):
        self.subtable = [[ttt_table() for i in range(3)] for j in range(3)]
        self.subtable_winner = ttt_table()
        self.subtable_to_be_played = [None, None] # location of the subtable to be played, [x, y]
        self.winner = 0
        self.game_over = False
        self.moves_log = []

    # method to print the table
    def print_table(self):
        print(16 * "* ")
        for i in range(3):
            for j in range(3):
                print("* ", end=" ")
                for k in range(3):
                    for l in range(3):
                        if self.subtable[i][k].table[j][l] == 0:
                            print(" ", end=" ")
                        else:
                            print(self.subtable[i][k].table[j][l], end=" ")
                    print(" * ", end=" ")
                if j != 2:
                    print("\n", end="")
            print("\n" + 16 * "* ")

    # method to check if the game is over
    def check_game_over(self):
        if self.subtable_winner.game_over == True:
            self.game_over = True
            self.winner = self.subtable_winner.winner

    # method to make a move
    def make_move(self, subtable_x, subtable_y, x, y, symbol): # x, y are the coordinates of the move in the subtable
        #print(f"subtable to be played: {self.subtable_to_be_played}, subtable played: {[subtable_x, subtable_y]}, move: {[x, y]}, symbol: {symbol}")
        # check if the subtable is playable
        if self.subtable_to_be_played == [None, None]:
            pass
        elif self.subtable_to_be_played != [subtable_x, subtable_y] and self.subtable[subtable_to_be_played[0]][subtable_to_be_played[1]].game_over == False:
            raise Exception(f"Illegal subtable to be played: must play in subtable {self.subtable_to_be_played} but played in subtable {[subtable_x, subtable_y]}")
            return
        if self.subtable[subtable_x][subtable_y].game_over == True:
            raise Exception(f"Illegal subtable to be played: subtable {self.subtable_to_be_played} is already over")
            return
        
        # make the move
        try:
            self.subtable[subtable_x][subtable_y].make_move(x, y, symbol) # move
        except Exception as e:
            raise Exception(f"Illegal move in subtable {[subtable_x, subtable_y]}: {e}")
            return
        self.moves_log.append([symbol, [subtable_x, subtable_y, x, y]]) # log the move
        if self.subtable[x][y].game_over == True:
            self.subtable_to_be_played = [None, None]
        else:
            self.subtable_to_be_played = [x, y] # update the subtable to be played
        # if subtable is over, update the subtable winner
        if self.subtable[subtable_x][subtable_y].game_over == True:
            self.subtable_winner.make_move(subtable_x, subtable_y, self.subtable[subtable_x][subtable_y].winner)

        # check if the game is over
        self.check_game_over()







# class for the table of tic-tac-toe game
class ttt_table:
    def __init__(self):
        self.table = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.winner = 0
        self.game_over = False
        self.moves = 0

    # method to print the table
    def print_table(self):
        print("----------")
        for i in range(3):
            for j in range(3):
                if self.table[i][j] == 0:
                    print(" ", end=" ")
                else:
                    print(self.table[i][j], end=" ")
                if j != 2:
                    print("|", end=" ")
            print("\n----------")

    # method to check if the game is over
    def check_game_over(self):
        if self.moves == 9:
            self.game_over = True
        elif self.winner != 0:
            self.game_over = True

    # method to check if the game is won
    def check_winner(self):
        # check rows
        for i in range(3):
            if self.table[i][0] == self.table[i][1] == self.table[i][2] != 0:
                self.winner = self.table[i][0]
                break
        # check columns
        for i in range(3):
            if self.table[0][i] == self.table[1][i] == self.table[2][i] != 0:
                self.winner = self.table[0][i]
                break
        # check diagonals
        if self.table[0][0] == self.table[1][1] == self.table[2][2] != 0:
            self.winner = self.table[0][0]
        elif self.table[0][2] == self.table[1][1] == self.table[2][0] != 0:
            self.winner = self.table[0][2]

    # method to make a move
    def make_move(self, x, y, symbol):
        if self.table[x][y] == 0:
            self.table[x][y] = symbol
            self.moves += 1
            self.check_winner()
            self.check_game_over()
        else:
            raise Exception(f"Illegal move: [{x}, {y}] is already occupied")
            return

    # method to reset the table
    def reset_table(self):
        self.table = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


if __name__ == "__main__":
    ttt = uttt_table()
    ttt.print_table()
    ttt.make_move(0, 0, 1, 1, 'x')
    ttt.print_table()
    ttt.make_move(1, 1, 0, 0, 'o')
    ttt.print_table()
    ttt.make_move(0, 0, 0, 0, 'x')
    ttt.print_table()
    ttt.make_move(0, 0, 2, 2, 'o')
    ttt.print_table()
    ttt.make_move(2, 2, 0, 0, 'x')
    ttt.print_table()
    ttt.make_move(0, 0, 1, 0, 'o')
    ttt.print_table()
    ttt.make_move(1, 0, 0, 0, 'x')
    ttt.print_table()
    ttt.make_move(0, 0, 1, 2, 'o')
    ttt.print_table()
    ttt.make_move(1, 2, 0, 0, 'x')
    ttt.print_table()
    ttt.make_move(0, 0, 2, 0, 'o')
    ttt.print_table()
    ttt.make_move(2, 0, 0, 0, 'x')
    ttt.print_table()
    ttt.make_move(0, 0, 2, 1, 'o')
    ttt.print_table()
    ttt.make_move(2, 1, 0, 0, 'x')
    ttt.print_table()
    print(f"winner: {ttt.winner}")
    print(f"game over: {ttt.game_over}")
    ttt.subtable_winner.print_table()
