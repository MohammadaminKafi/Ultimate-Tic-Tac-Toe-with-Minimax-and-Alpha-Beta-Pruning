def uttt_heuristic(board, log_enabled=0):

    if board.game_over == True:
        if board.winner == 'X':
            return 1000000
        elif board.winner == 'O':
            return -1000000

    '''
    metrics are:
    - number of subtables won
    - number of subtables lost
    - total number of subtables played
    - if the subtable to be played is over (kind of if subtable to be played is [None, None])
    - number of potential win in the subtables 
    - number of potential loss in the subtables
    - potential win in the table
    - potential loss in the table
    - value each cell (center = 4, corners = 3, edges = 2)
    '''
    coef_number_of_subtables_won = 13
    coef_number_of_subtables_lost = -12
    coef_total_number_of_subtables_played = 1 / 4
    coef_subtable_to_be_played_is_over = 10
    coef_number_of_potential_win_in_subtables = 5
    coef_number_of_potential_loss_in_subtables = -5
    coef_potential_win_in_table = 13
    coef_potential_loss_in_table = -14
    coef_value_each_cell = 1

    subtables_won_X = 0 # number of subtables won by X, lost by O
    subtables_lost_X = 0 # number of subtables lost by X, won by O
    subtables_over = 0 # number of subtables that are over, won by X or O or draw
    subtable_to_be_played_is_over_X = 0 # if the subtable to be played is over and it is X's turn (1), if it is O's turn (-1), if it is a draw (0)
    potential_win_in_subtables_X = 0 # number of subtables that X can win, O can lose
    potential_loss_in_subtables_X = 0 # number of subtables that X can lose, O can win
    potential_win_in_table_X = 0 # number of ways that X can win the table, O can lose
    potential_loss_in_table_X = 0 # number of ways that X can lose the table, O can win
    total_cell_value_X = 0 # total of value of each cell for X
    total_cell_value_O = 0 # total of value of each cell for O

    # calculating subtables_won_X, subtables_lost_X, subtables_over
    for i in range(3):
        for j in range(3):
            if board.subtable[i][j].game_over == True:
                if board.subtable[i][j].winner == 'X':
                    if i == j == 1:
                        subtables_won_X += 3
                    elif abs(i - j) == 1:
                        subtables_won_X += 1
                    else:
                        subtables_won_X += 2
                elif board.subtable[i][j].winner == 'O':
                    if i == j == 1:
                        subtables_lost_X += 3
                    elif abs(i - j) == 1:
                        subtables_lost_X += 1
                    else:
                        subtables_lost_X += 2
                subtables_over += 1

    # calculating subtable_to_be_played_is_over_X
    if board.subtable_to_be_played == [None, None]:
        # check last move
        if board.moves_log[-1][0] == 'X':
            subtable_to_be_played_is_over_X = -1
        else:
            subtable_to_be_played_is_over_X = 1

    # calculating potential_win_in_subtables_X, potential_loss_in_subtables_X
    for i in range(3):
        for j in range(3):
            if board.subtable[i][j].game_over == False:
                # check if there is 2 of 3 in a row, column or diagonal
                for k in range(3):
                    # check rows
                    if board.subtable[i][j].table[k][0] == board.subtable[i][j].table[k][1] == 'X' and board.subtable[i][j].table[k][2] == 0:
                        potential_win_in_subtables_X += 1
                    elif board.subtable[i][j].table[k][0] == board.subtable[i][j].table[k][2] == 'X' and board.subtable[i][j].table[k][1] == 0:
                        potential_win_in_subtables_X += 1
                    elif board.subtable[i][j].table[k][1] == board.subtable[i][j].table[k][2] == 'X' and board.subtable[i][j].table[k][0] == 0:
                        potential_win_in_subtables_X += 1
                    elif board.subtable[i][j].table[k][0] == board.subtable[i][j].table[k][1] == 'O' and board.subtable[i][j].table[k][2] == 0:
                        potential_loss_in_subtables_X += 1
                    elif board.subtable[i][j].table[k][0] == board.subtable[i][j].table[k][2] == 'O' and board.subtable[i][j].table[k][1] == 0:
                        potential_loss_in_subtables_X += 1
                    elif board.subtable[i][j].table[k][1] == board.subtable[i][j].table[k][2] == 'O' and board.subtable[i][j].table[k][0] == 0:
                        potential_loss_in_subtables_X += 1
                    # check columns
                    if board.subtable[i][j].table[0][k] == board.subtable[i][j].table[1][k] == 'X' and board.subtable[i][j].table[2][k] == 0:
                        potential_win_in_subtables_X += 1
                    elif board.subtable[i][j].table[0][k] == board.subtable[i][j].table[2][k] == 'X' and board.subtable[i][j].table[1][k] == 0:
                        potential_win_in_subtables_X += 1
                    elif board.subtable[i][j].table[1][k] == board.subtable[i][j].table[2][k] == 'X' and board.subtable[i][j].table[0][k] == 0:
                        potential_win_in_subtables_X += 1
                    elif board.subtable[i][j].table[0][k] == board.subtable[i][j].table[1][k] == 'O' and board.subtable[i][j].table[2][k] == 0:
                        potential_loss_in_subtables_X += 1
                    elif board.subtable[i][j].table[0][k] == board.subtable[i][j].table[2][k] == 'O' and board.subtable[i][j].table[1][k] == 0:
                        potential_loss_in_subtables_X += 1
                    elif board.subtable[i][j].table[1][k] == board.subtable[i][j].table[2][k] == 'O' and board.subtable[i][j].table[0][k] == 0:
                        potential_loss_in_subtables_X += 1
                # check diagonals
                if board.subtable[i][j].table[0][0] == board.subtable[i][j].table[1][1] == 'X' and board.subtable[i][j].table[2][2] == 0:
                    potential_win_in_subtables_X += 1
                elif board.subtable[i][j].table[0][0] == board.subtable[i][j].table[2][2] == 'X' and board.subtable[i][j].table[1][1] == 0:
                    potential_win_in_subtables_X += 1
                elif board.subtable[i][j].table[1][1] == board.subtable[i][j].table[2][2] == 'X' and board.subtable[i][j].table[0][0] == 0:
                    potential_win_in_subtables_X += 1
                elif board.subtable[i][j].table[0][0] == board.subtable[i][j].table[1][1] == 'O' and board.subtable[i][j].table[2][2] == 0:
                    potential_loss_in_subtables_X += 1
                elif board.subtable[i][j].table[0][0] == board.subtable[i][j].table[2][2] == 'O' and board.subtable[i][j].table[1][1] == 0:
                    potential_loss_in_subtables_X += 1
                elif board.subtable[i][j].table[1][1] == board.subtable[i][j].table[2][2] == 'O' and board.subtable[i][j].table[0][0] == 0:
                    potential_loss_in_subtables_X += 1
                if board.subtable[i][j].table[0][2] == board.subtable[i][j].table[1][1] == 'X' and board.subtable[i][j].table[2][0] == 0:
                    potential_win_in_subtables_X += 1
                elif board.subtable[i][j].table[0][2] == board.subtable[i][j].table[2][0] == 'X' and board.subtable[i][j].table[1][1] == 0:
                    potential_win_in_subtables_X += 1
                elif board.subtable[i][j].table[1][1] == board.subtable[i][j].table[2][0] == 'X' and board.subtable[i][j].table[0][2] == 0:
                    potential_win_in_subtables_X += 1
                elif board.subtable[i][j].table[0][2] == board.subtable[i][j].table[1][1] == 'O' and board.subtable[i][j].table[2][0] == 0:
                    potential_loss_in_subtables_X += 1
                elif board.subtable[i][j].table[0][2] == board.subtable[i][j].table[2][0] == 'O' and board.subtable[i][j].table[1][1] == 0:
                    potential_loss_in_subtables_X += 1
                elif board.subtable[i][j].table[1][1] == board.subtable[i][j].table[2][0] == 'O' and board.subtable[i][j].table[0][2] == 0:
                    potential_loss_in_subtables_X += 1

    # calculating potential_win_in_table_X, potential_loss_in_table_X
    # check if there is 2 of 3 in a row, column or diagonal
    for k in range(3):
        # check rows
        if board.subtable_winner.table[k][0] == board.subtable_winner.table[k][1] == 'X' and board.subtable_winner.table[k][2] == 0:
            potential_win_in_table_X += 1
        elif board.subtable_winner.table[k][0] == board.subtable_winner.table[k][2] == 'X' and board.subtable_winner.table[k][1] == 0:
            potential_win_in_table_X += 1
        elif board.subtable_winner.table[k][1] == board.subtable_winner.table[k][2] == 'X' and board.subtable_winner.table[k][0] == 0:
            potential_win_in_table_X += 1
        elif board.subtable_winner.table[k][0] == board.subtable_winner.table[k][1] == 'O' and board.subtable_winner.table[k][2] == 0:
            potential_loss_in_table_X += 1
        elif board.subtable_winner.table[k][0] == board.subtable_winner.table[k][2] == 'O' and board.subtable_winner.table[k][1] == 0:
            potential_loss_in_table_X += 1
        elif board.subtable_winner.table[k][1] == board.subtable_winner.table[k][2] == 'O' and board.subtable_winner.table[k][0] == 0:
            potential_loss_in_table_X += 1
        # check columns
        if board.subtable_winner.table[0][k] == board.subtable_winner.table[1][k] == 'X' and board.subtable_winner.table[2][k] == 0:
            potential_win_in_table_X += 1
        elif board.subtable_winner.table[0][k] == board.subtable_winner.table[2][k] == 'X' and board.subtable_winner.table[1][k] == 0:
            potential_win_in_table_X += 1
        elif board.subtable_winner.table[1][k] == board.subtable_winner.table[2][k] == 'X' and board.subtable_winner.table[0][k] == 0:
            potential_win_in_table_X += 1
        elif board.subtable_winner.table[0][k] == board.subtable_winner.table[1][k] == 'O' and board.subtable_winner.table[2][k] == 0:
            potential_loss_in_table_X += 1
        elif board.subtable_winner.table[0][k] == board.subtable_winner.table[2][k] == 'O' and board.subtable_winner.table[1][k] == 0:
            potential_loss_in_table_X += 1
        elif board.subtable_winner.table[1][k] == board.subtable_winner.table[2][k] == 'O' and board.subtable_winner.table[0][k] == 0:
            potential_loss_in_table_X += 1
    # check diagonals
    if board.subtable_winner.table[0][0] == board.subtable_winner.table[1][1] == 'X' and board.subtable_winner.table[2][2] == 0:
        potential_win_in_table_X += 1
    elif board.subtable_winner.table[0][0] == board.subtable_winner.table[2][2] == 'X' and board.subtable_winner.table[1][1] == 0:
        potential_win_in_table_X += 1
    elif board.subtable_winner.table[1][1] == board.subtable_winner.table[2][2] == 'X' and board.subtable_winner.table[0][0] == 0:
        potential_win_in_table_X += 1
    elif board.subtable_winner.table[0][0] == board.subtable_winner.table[1][1] == 'O' and board.subtable_winner.table[2][2] == 0:
        potential_loss_in_table_X += 1
    elif board.subtable_winner.table[0][0] == board.subtable_winner.table[2][2] == 'O' and board.subtable_winner.table[1][1] == 0:
        potential_loss_in_table_X += 1
    elif board.subtable_winner.table[1][1] == board.subtable_winner.table[2][2] == 'O' and board.subtable_winner.table[0][0] == 0:
        potential_loss_in_table_X += 1        
    if board.subtable_winner.table[0][2] == board.subtable_winner.table[1][1] == 'X' and board.subtable_winner.table[2][0] == 0:
        potential_win_in_table_X += 1
    elif board.subtable_winner.table[0][2] == board.subtable_winner.table[2][0] == 'X' and board.subtable_winner.table[1][1] == 0:
        potential_win_in_table_X += 1
    elif board.subtable_winner.table[1][1] == board.subtable_winner.table[2][0] == 'X' and board.subtable_winner.table[0][2] == 0:
        potential_win_in_table_X += 1
    elif board.subtable_winner.table[0][2] == board.subtable_winner.table[1][1] == 'O' and board.subtable_winner.table[2][0] == 0:
        potential_loss_in_table_X += 1
    elif board.subtable_winner.table[0][2] == board.subtable_winner.table[2][0] == 'O' and board.subtable_winner.table[1][1] == 0:
        potential_loss_in_table_X += 1
    elif board.subtable_winner.table[1][1] == board.subtable_winner.table[2][0] == 'O' and board.subtable_winner.table[0][2] == 0:
        potential_loss_in_table_X += 1

    # calculating total_cell_value_X, total_cell_value_O
    # kind of representing #ifdef from C in Python
    if coef_value_each_cell != 0:
        for i in range(3):
            for j in range(3):
                if board.subtable[i][j].game_over == False:
                    for k in range(3):
                        for l in range(3):
                            if board.subtable[i][j].table[k][l] == 'X':
                                if k == l == 1:
                                    total_cell_value_X += (4 if i == j == 1 else 3)
                                elif abs(k - l) == 1:
                                    total_cell_value_X += (2 if i == j == 1 else 1)
                                else:
                                    total_cell_value_X += (3 if i == j == 1 else 2)
                            elif board.subtable[i][j].table[k][l] == 'O':
                                if k == l == 1:
                                    total_cell_value_O += (4 if i == j == 1 else 3)
                                elif abs(k - l) == 1:
                                    total_cell_value_O += (2 if i == j == 1 else 1)
                                else:
                                    total_cell_value_O += (3 if i == j == 1 else 2) 

    # calculating the heuristic
    heuristic_X = coef_number_of_subtables_won * subtables_won_X + \
        coef_number_of_subtables_lost * subtables_lost_X + \
        coef_subtable_to_be_played_is_over * subtable_to_be_played_is_over_X + \
        coef_number_of_potential_win_in_subtables * potential_win_in_subtables_X + \
        coef_number_of_potential_loss_in_subtables * potential_loss_in_subtables_X + \
        coef_potential_win_in_table * potential_win_in_table_X + \
        coef_potential_loss_in_table * potential_loss_in_table_X + \
        coef_value_each_cell * (total_cell_value_X - total_cell_value_O) 

    if log_enabled == 1:
        print(f"won_subtable: {coef_number_of_subtables_won} * {subtables_won_X} + \n\
lost_subtable:                  {coef_number_of_subtables_lost} * {subtables_lost_X} + \n\
subtable_to_be_played_is_over:  {subtable_to_be_played_is_over_X} + \n\
potential_win:                  {coef_number_of_potential_win_in_subtables} * {potential_win_in_subtables_X} + \n\
potential_lost:                 {coef_number_of_potential_loss_in_subtables} * {potential_loss_in_subtables_X} + \n\
potential_win_table:            {coef_potential_win_in_table} * {potential_win_in_table_X} + \n\
potential_lost_table:           {coef_potential_loss_in_table} * {potential_loss_in_table_X} \n\
                    ")         

    total_coef = coef_total_number_of_subtables_played * (subtables_over + 1)

    return total_coef * heuristic_X
