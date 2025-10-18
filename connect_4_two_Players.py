import numpy as np 
import pygame 
import sys
import math

BOARD_COLOR = (43, 155, 251)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((6, 7))
    return board

def drop_peice(board, row, col, peice):
    board[row][col] = peice 

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

# Check the winning Move
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True

# Pygame board
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in  range(ROW_COUNT):
            pygame.draw.rect(screen, BOARD_COLOR, (c * SQUARE, r * SQUARE + SQUARE, SQUARE, SQUARE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (int((c * SQUARE + SQUARE / 2)), (int(r * SQUARE + SQUARE + SQUARE / 2))), RADIUS )
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int((c * SQUARE + SQUARE / 2)), (int(r * SQUARE + SQUARE + SQUARE / 2))), RADIUS )
            else:
                pygame.draw.circle(screen, YELLOW, (int((c * SQUARE + SQUARE / 2)), (int(r * SQUARE + SQUARE + SQUARE / 2))), RADIUS)
    pygame.display.update()

board = create_board()
game_over = False
turn = 0

pygame.init()
SQUARE = 100
width = COLUMN_COUNT * SQUARE
height = (ROW_COUNT + 1) * SQUARE

size = (width, height)

RADIUS = int(SQUARE / 2 - 2)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

font = pygame.font.SysFont("Times New Roman", 75, True)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE))

            # Player 1 nput
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_peice(board, row, col, 1)

                    if winning_move(board, 1):
                        message = font.render("Player 1 Wins!!", 1, WHITE)
                        screen.blit(message, (80, 10))
                        print("Player 1 Wins!!")
                        game_over = True


            # Player 2 input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_peice(board, row, col, 2)
                    
                    if winning_move(board, 2):
                        message = font.render("Player 2 Wins!!", 1, WHITE)
                        screen.blit(message, (80, 10))
                        print("Player 2 Wins!!")
                        game_over = True
            
            print_board(board)
            draw_board(np.flip(board, 0))
            turn += 1
            turn %= 2
            if game_over:
                pygame.time.wait(3000)
