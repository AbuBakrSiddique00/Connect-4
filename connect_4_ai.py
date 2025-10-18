import numpy as np 
import pygame 
import sys, math, random

PLAYER = 0 
AI = 1
PLAYER_NUMBER = 1
AI_NUMBER = 2
EMPTY = 0

BOARD_COLOR = (43, 155, 251)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

WINDOW_LENGTH = 4


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


def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_NUMBER
	if piece == PLAYER_NUMBER:
		opp_piece = AI_NUMBER

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2
	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 80

	return score

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, piece):

	valid_locations = get_valid_locations(board)
	best_score = -1000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_peice(temp_board, row, col, piece)
		score = scoring_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

# Scoring 
def scoring_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score




# Pygame board
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in  range(ROW_COUNT):
            pygame.draw.rect(screen, BOARD_COLOR, (c * SQUARE, r * SQUARE + SQUARE, SQUARE, SQUARE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, WHITE, (int((c * SQUARE + SQUARE / 2)), (int(r * SQUARE + SQUARE + SQUARE / 2))), RADIUS )
            elif board[r][c] == PLAYER_NUMBER:
                pygame.draw.circle(screen, YELLOW, (int((c * SQUARE + SQUARE / 2)), (int(r * SQUARE + SQUARE + SQUARE / 2))), RADIUS )
            else:
                pygame.draw.circle(screen, RED, (int((c * SQUARE + SQUARE / 2)), (int(r * SQUARE + SQUARE + SQUARE / 2))), RADIUS)
    pygame.display.update()


# Terminal Node
def is_terminal_node(board):
	return winning_move(board, PLAYER_NUMBER) or winning_move(board, AI_NUMBER) or len(get_valid_locations(board)) == 0

# Minimax algorithm
def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_NUMBER):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_NUMBER):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, scoring_position(board, AI_NUMBER))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_peice(b_copy, row, col, AI_NUMBER)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_peice(b_copy, row, col, PLAYER_NUMBER)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

board = create_board()
game_over = False
# turn = random.randint(0, 1)
turn = 1

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
            pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE / 2)), RADIUS)
            # else:
            #     pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARE))

            # Player 1 nput
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_peice(board, row, col, PLAYER_NUMBER)

                    if winning_move(board, PLAYER_NUMBER):
                        message = font.render("Player  Wins!!", 1, BLACK)
                        screen.blit(message, (80, 10))
                        print("Player Wins!!")
                        game_over = True
                    print_board(board)
                    draw_board(np.flip(board, 0))
                    turn += 1
                    turn %= 2


    # AI input
    if  turn == AI and not game_over:
        # col = random.randint(0, COLUMN_COUNT - 1)
        # col = pick_best_move(board, AI_NUMBER)
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_peice(board, row, col, AI_NUMBER)
            
            if winning_move(board, AI_NUMBER):
                message = font.render("AI Wins!!", 1, BLACK)
                screen.blit(message, (80, 10))
                print("AI Wins!!")
                game_over = True
            
            print_board(board)
            draw_board(np.flip(board, 0))
            turn += 1
            turn %= 2
    if game_over:
        pygame.time.wait(3000)

