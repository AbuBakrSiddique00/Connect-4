from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .logic import (
    create_board,
    apply_player_move,
    minimax,
    AI_NUMBER,
    PLAYER_NUMBER,
    is_terminal_node,
    winning_move,
)


@api_view(['GET'])
def api_root(request):
    return Response({
        'new_game': request.build_absolute_uri('new-game/'),
        'apply_move': request.build_absolute_uri('apply-move/'),
        'ai_move': request.build_absolute_uri('ai-move/'),
    })


@api_view(['GET'])
def new_game(request):
    board = create_board()
    return Response({
        'board': board,
        'player': PLAYER_NUMBER,
        'ai': AI_NUMBER,
        'game_over': False,
        'winner': None,
    })


@api_view(['POST'])
def apply_move(request):
    data = request.data
    board = data.get('board')
    col = data.get('column')
    piece = data.get('piece', PLAYER_NUMBER)

    if not isinstance(board, list) or not isinstance(col, int):
        return Response({'detail': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        updated, winner = apply_player_move(board, col, piece)
    except ValueError as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    game_over = winner is not None or is_terminal_node(updated)
    return Response({
        'board': updated,
        'game_over': game_over,
        'winner': winner,
    })


@api_view(['POST'])
def ai_move(request):
    data = request.data
    board = data.get('board')
    depth = int(data.get('depth', 5))

    if not isinstance(board, list):
        return Response({'detail': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)

    # If already over, just echo
    if is_terminal_node(board):
        winner = None
        if winning_move(board, AI_NUMBER):
            winner = 'AI'
        elif winning_move(board, PLAYER_NUMBER):
            winner = 'PLAYER'
        return Response({'board': board, 'game_over': True, 'winner': winner})

    col, _ = minimax(board, depth, float('-inf'), float('inf'), True)
    if col is None:
        return Response({'board': board, 'game_over': True, 'winner': None})

    try:
        updated, winner = apply_player_move(board, col, AI_NUMBER)
    except ValueError:
        # Should not happen; return as is
        return Response({'board': board, 'game_over': True, 'winner': None})

    game_over = winner is not None or is_terminal_node(updated)
    return Response({
        'board': updated,
        'column': col,
        'game_over': game_over,
        'winner': winner,
    })
