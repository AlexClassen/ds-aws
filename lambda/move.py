import math
import random
from common import *
import json
import numpy as np

def score(board, player):
    score = 0
    # Give more weight to center columns
    for col in range(2, 5):
        for row in range(ROWS):
            if board[row][col] == player:
                if col == 3:
                    score += 3
                else:
                    score+= 2
    # Horizontal pieces
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS):
            adjacent_pieces = [board[row][col], board[row][col+1],
                               board[row][col+2], board[row][col+3]]
            score += evaluate_adjacents(adjacent_pieces, player)
    # Vertical pieces
    for col in range(COLUMNS):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            adjacent_pieces = [board[row][col], board[row+1][col],
                               board[row+2][col], board[row+3][col]]
            score += evaluate_adjacents(adjacent_pieces, player)
    # Diagonal upwards pieces
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            adjacent_pieces = [board[row][col], board[row+1][col+1],
                               board[row+2][col+2], board[row+3][col+3]]
            score += evaluate_adjacents(adjacent_pieces, player)
    # Diagonal downwards pieces
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(MAX_SPACE_TO_WIN, ROWS):
            adjacent_pieces = [board[row][col], board[row-1][col+1],
                               board[row-2][col+2], board[row-3][col+3]]
            score += evaluate_adjacents(adjacent_pieces, player)
    return score

def evaluate_adjacents(adjacent_pieces, player):
    opponent = AI_1
    if player == AI_1:
        opponent = AI_2
    score = 0
    player_pieces = 0
    empty_spaces = 0
    opponent_pieces = 0
    for p in adjacent_pieces:
        if p == player:
            player_pieces += 1
        elif p == EMPTY:
            empty_spaces += 1
        elif p == opponent:
            opponent_pieces += 1
    if player_pieces == 4:
        score += 99999
    elif player_pieces == 3 and empty_spaces == 1:
        score += 100
    elif player_pieces == 2 and empty_spaces == 2:
        score += 10
    return score

# Returns a successor board
def clone_and_place_piece(board, player, column):
    new_board = board.copy()
    place_piece(new_board, player, column)
    return new_board

# Returns true if current board is a terminal board which happens when
# either player wins or no more spaces on the board are free
def is_terminal_board(board):
    return detect_win(board, AI_2) or detect_win(board, AI_1) or \
        len(valid_locations(board)) == 0

def minimax(board, ply, maxi_player, player):
    opponent = AI_1 if player == AI_2 else AI_2
    valid_cols = valid_locations(board)
    is_terminal = is_terminal_board(board)
    if ply == 0 or is_terminal:
        if is_terminal:
            if detect_win(board, opponent):
                return (None,-1000000000)
            elif detect_win(board, player):
                return (None,1000000000)
            else: # There is no winner
                return (None,0)
        else: # Ply == 0
            return (None,score(board, player))
    # If max player
    if maxi_player:
        value = -math.inf
        # If every choice has an equal score, choose randomly
        col = random.choice(valid_cols)
        # Expand current node/board
        for c in valid_cols:
            next_board = clone_and_place_piece(board, player, c)
            new_score = minimax(next_board, ply - 1, False, player)[1]
            if new_score > value:
                value = new_score
                col = c
        return col, value
    #if min player
    else:
        value = math.inf
        col = random.choice(valid_cols)
        for c in valid_cols:
            next_board = clone_and_place_piece(board, opponent, c)
            new_score = minimax(next_board, ply - 1, True, player)[1]
            if new_score < value:
                value = new_score
                col = c
        return col, value

def lambda_handler(event, context):
    # Parse input from event
    board = np.array(event.get("board"))
    player = event.get("player")
    depth = event.get("depth", 3)  # Default depth 3 if not provided

    # Run minimax to get the best move
    col, score = minimax(board, depth, True, player)

    # Return response as JSON
    return {
        "statusCode": 200,
        "body": json.dumps({
            "column": col,
            "score": score
        })
    }
