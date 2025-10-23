import math
from typing import List, Optional, Tuple

# Constants matching the original implementation
PLAYER = 0
AI = 1
PLAYER_NUMBER = 1
AI_NUMBER = 2
EMPTY = 0
ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4

Board = List[List[int]]


def create_board() -> Board:
    return [[0 for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]


def drop_piece(board: Board, row: int, col: int, piece: int) -> None:
    board[row][col] = piece


def is_valid_location(board: Board, col: int) -> bool:
    return board[ROW_COUNT - 1][col] == EMPTY


def get_next_open_row(board: Board, col: int) -> Optional[int]:
    for r in range(ROW_COUNT):
        if board[r][col] == EMPTY:
            return r
    return None


def get_valid_locations(board: Board) -> List[int]:
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]


def winning_move(board: Board, piece: int) -> bool:
    # Horizontal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Positive diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Negative diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True

    return False


def evaluate_window(window: List[int], piece: int) -> int:
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


def score_position(board: Board, piece: int) -> int:
    score = 0

    # Center score
    center_col = COLUMN_COUNT // 2
    center_array = [board[r][center_col] for r in range(ROW_COUNT)]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Horizontal
    for r in range(ROW_COUNT):
        row_array = [board[r][c] for c in range(COLUMN_COUNT)]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c : c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Vertical
    for c in range(COLUMN_COUNT):
        col_array = [board[r][c] for r in range(ROW_COUNT)]
        for r in range(ROW_COUNT - 3):
            window = col_array[r : r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Positive diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Negative diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board: Board) -> bool:
    return (
        winning_move(board, PLAYER_NUMBER)
        or winning_move(board, AI_NUMBER)
        or len(get_valid_locations(board)) == 0
    )


def minimax(board: Board, depth: int, alpha: float, beta: float, maximizingPlayer: bool) -> Tuple[Optional[int], int]:
    valid_locations = get_valid_locations(board)
    terminal = is_terminal_node(board)
    if depth == 0 or terminal:
        if terminal:
            if winning_move(board, AI_NUMBER):
                return (None, 10**12)
            elif winning_move(board, PLAYER_NUMBER):
                return (None, -10**12)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_NUMBER))

    if maximizingPlayer:
        value = -math.inf
        best_col = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row is None:
                continue
            b_copy = [r.copy() for r in board]
            drop_piece(b_copy, row, col, AI_NUMBER)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, int(value)
    else:
        value = math.inf
        best_col = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row is None:
                continue
            b_copy = [r.copy() for r in board]
            drop_piece(b_copy, row, col, PLAYER_NUMBER)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, int(value)


def apply_player_move(board: Board, col: int, piece: int) -> Tuple[Board, Optional[str]]:
    """
    Returns updated board and winner string ("PLAYER"/"AI") or None
    Raises ValueError on invalid column
    """
    if col < 0 or col >= COLUMN_COUNT or not is_valid_location(board, col):
        raise ValueError("Invalid move")
    row = get_next_open_row(board, col)
    if row is None:
        raise ValueError("Column full")
    drop_piece(board, row, col, piece)
    winner = None
    if winning_move(board, piece):
        winner = 'PLAYER' if piece == PLAYER_NUMBER else 'AI'
    return board, winner
