# Ultimate tic-tac-toe using pygame

import pygame
import sys
from tables import uttt_table
from datetime import datetime
import heuristics
from ai import minimax_alphaBetaPrunning
import time
import sys

# Define the dimensions of the game board (3x3)
BOARD_SIZE = 9

# Define the size of the window and the size of each cell
BOARD_TABLE_SIZE = 900
CELL_SIZE = BOARD_TABLE_SIZE // BOARD_SIZE

# Define some colors
WHITE = (210, 210, 210)
BLACK = (20, 20, 20)
GRAY = (50, 50, 50)
RED = (255, 0 , 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (0, 255, 255)
LIGHT_GREEN = (100, 255, 100)
FIRST_PLAYER_COLOR = ORANGE
SECOND_PLAYER_COLOR = LIGHT_GREEN

def handle_click(pos):
    # return if the game is over
    if board.game_over == True:
        return

    global player_turn
    # return if the click is outside the board
    if pos[0] > BOARD_TABLE_SIZE or pos[1] > BOARD_TABLE_SIZE:
        return
    # calculating subtable_x and subtable_y
    subtable_x = pos[1] // 300
    subtable_y = pos[0] // 300
    # calculating cell_x and cell_y
    cell_x = (pos[1] % 300) // 100
    cell_y = (pos[0] % 300) // 100
    # log
    print(f"Clicked on {pos}: subtable {[subtable_x, subtable_y]}, cell {[cell_x, cell_y]}")

    # make the move
    try:
        board.make_move(subtable_x, subtable_y, cell_x, cell_y, player_turn) # move
        player_turn = 'O' if player_turn == 'X' else 'X'
        #print(f"heuristic: {heuristics.uttt_heuristic(board)}")
    except Exception as e:
        print(f"Illegal move in subtable {[subtable_x, subtable_y]}: {e}")

def draw_board(board_table):
    # change the background of the subtable to be played
    if board_table.subtable_to_be_played != [None, None]:
        pygame.draw.rect(screen, GRAY, (board_table.subtable_to_be_played[1] * 300, board_table.subtable_to_be_played[0] * 300, 300, 300))
    
    # draw borders
    for i in range(1, BOARD_SIZE):
        if i % 3 == 0:
            pygame.draw.line(screen, WHITE, (0, i * CELL_SIZE), (BOARD_TABLE_SIZE, i * CELL_SIZE), 10)
            pygame.draw.line(screen, WHITE, (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_TABLE_SIZE), 10)
        else:
            pygame.draw.line(screen, WHITE, (0, i * CELL_SIZE), (BOARD_TABLE_SIZE, i * CELL_SIZE), 3)
            pygame.draw.line(screen, WHITE, (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_TABLE_SIZE), 3)

    # draw subtables
    draw = 0
    for i in range(3):
        for j in range(3):
            if board_table.subtable[i][j].game_over == True:
                if board_table.subtable[i][j].winner == 'X':
                    color = FIRST_PLAYER_COLOR
                elif board_table.subtable[i][j].winner == 'O':
                    color = SECOND_PLAYER_COLOR
                else:
                    color = WHITE
                    draw = 1
                text = block_symbol_font.render(board_table.subtable[i][j].winner if not draw else 'Nobody', True, color)
                screen.blit(text, (j * 300 + 30, i * 300))
                
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    if board_table.subtable[i][k].table[j][l] != 0:
                        if board_table.subtable[i][k].game_over == False:
                            if board_table.subtable[i][k].table[j][l] == 'X':
                                color = FIRST_PLAYER_COLOR
                            else:
                                color = SECOND_PLAYER_COLOR
                            text = cell_symbol_font.render(board_table.subtable[i][k].table[j][l], True, color)
                            screen.blit(text, (k * 300 + l * 100 + 10, i * 300 + j * 100 + 5))
                        else:
                            text = cell_symbol_font.render(board_table.subtable[i][k].table[j][l], True, GRAY)
                            screen.blit(text, (k * 300 + l * 100 + 10, i * 300 + j * 100 + 5))

    # 
    if board_table.game_over == True:
        if board_table.winner == 'X':
            color = FIRST_PLAYER_COLOR
        elif board_table.winner == 'O':
            color = SECOND_PLAYER_COLOR
        text = text_font.render(f"{board_table.winner} wins!", True, color)
        screen.blit(text, (BOARD_TABLE_SIZE + 20, 20))

# write logs on the screen
def write_logs(player, move, time_elapsed, heuristic_value):
    
        # write the player
        text = text_font.render(f"Player: {player}", True, WHITE)
        screen.blit(text, (BOARD_TABLE_SIZE + 20, 100))
    
        # write the move
        text = text_font.render(f"Move: {move}", True, WHITE)
        screen.blit(text, (BOARD_TABLE_SIZE + 20, 150))
    
        # write the time elapsed
        text = text_font.render(f"Time elapsed: {time_elapsed}", True, WHITE)
        screen.blit(text, (BOARD_TABLE_SIZE + 20, 200))
    
        # write the heuristic value
        text = text_font.render(f"Heuristic value: {heuristic_value}", True, WHITE)
        screen.blit(text, (BOARD_TABLE_SIZE + 20, 250))

########################################################################################################
########################################################################################################

# Create the game board
board = uttt_table()
player_turn = 'X'

# Initialize Pygame
pygame.init()

# Create the window and the font for drawing text
screen = pygame.display.set_mode((BOARD_TABLE_SIZE + 400, BOARD_TABLE_SIZE))
pygame.display.set_caption("Ultimate Tic-Tac-Toe")
pygame.display.set_icon(pygame.image.load("icon.png"))

cell_symbol_font = pygame.font.Font(None, int(CELL_SIZE * 1.5))
block_symbol_font = pygame.font.Font(None, int(CELL_SIZE * 5))
text_font = pygame.font.SysFont("Arial", 30)

visualizing = 0

# enter visualizing mode if there is an argument
if len(sys.argv) > 1:
    visualizing = 1
    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
        for line in lines:
            log_to_be_visualized = eval(line)
            len_log_to_be_visualized = len(log_to_be_visualized)

    if len(sys.argv) == 3 and sys.argv[2] == '1':
        wait_for_key_flag = 1
    else:
        wait_for_key_flag = 0
    
    turn_num = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if turn_num < len_log_to_be_visualized:
            if log_to_be_visualized[turn_num][0] == 'X':
                player_turn = 'X'
            else:
                player_turn = 'O'
            handle_click((log_to_be_visualized[turn_num][1][1] * 300 + log_to_be_visualized[turn_num][1][3] * 100 + 50, log_to_be_visualized[turn_num][1][0] * 300 + log_to_be_visualized[turn_num][1][2] * 100 + 50))
            turn_num += 1

        if wait_for_key_flag:
            wait_for_key = True
            while wait_for_key:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        wait_for_key = False
                    else:
                        wait_for_key_flag = 0
        else:
            time.sleep(0.5)

        screen.fill(BLACK)
        draw_board(board)
        write_logs(log_to_be_visualized[turn_num - 1][0], 
        log_to_be_visualized[turn_num - 1][1], 
        log_to_be_visualized[turn_num - 1][2], 
        log_to_be_visualized[turn_num - 1][3] if log_to_be_visualized[turn_num - 1][0] == 'X' else log_to_be_visualized[turn_num - 1][4])
        pygame.display.update()

    exit(0)


log_saved = 0

player_1 = 0
player_2 = 0

AI_1_depth = 3
AI_2_depth = 4

if not player_1 and not player_2:
    AI_log = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if player_turn == 'X' and player_1:
                handle_click(pygame.mouse.get_pos())
            elif player_turn == 'O' and player_2:
                handle_click(pygame.mouse.get_pos())

    # save the log if the game is over
    if board.game_over == True and log_saved == 0:
        log_saved = 1
        if player_1 or player_2:
            current_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            file_name = f"log{current_time}.txt"
            with open(file_name, "a") as f:
                f.write(f"{board.moves_log}\n")
        else:
            current_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            file_name = f"AI_log_{current_time}_{AI_1_depth}vs{AI_2_depth}.txt"
            with open(file_name, "a") as f:
                f.write(f"{AI_log}\n")

    # AI
    if board.game_over == False:
        if player_turn == 'X':
            if not player_1:
                elapsed_time, best_move, alpha, beta = minimax_alphaBetaPrunning(board, player_turn, AI_1_depth)
                AI_log.append([player_turn, best_move, elapsed_time, alpha, beta])
                print(f"AI took {elapsed_time} seconds to make a move in subtable {best_move[0:2]} at cell {best_move[2:4]}")
                handle_click((best_move[1] * 300 + best_move[3] * 100 + 50, best_move[0] * 300 + best_move[2] * 100 + 50))
        elif player_turn == 'O':
            if not player_2:
                elapsed_time, best_move, alpha, beta = minimax_alphaBetaPrunning(board, player_turn, AI_2_depth)
                AI_log.append([player_turn, best_move, elapsed_time, alpha, beta])
                print(f"AI took {elapsed_time} seconds to make a move in subtable {best_move[0:2]} at cell {best_move[2:4]}")
                handle_click((best_move[1] * 300 + best_move[3] * 100 + 50, best_move[0] * 300 + best_move[2] * 100 + 50))

    #time.sleep(1)
    
    screen.fill(BLACK)
    draw_board(board)
    pygame.display.update()
