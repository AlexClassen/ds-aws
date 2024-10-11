# This code was inspired by the project found at:
# https://github.com/bryanjsanchez/Parallel-Connect-Four
import argparse
import numpy as np
import random
import move
from common import *

def create_board():
    return np.zeros((ROWS, COLUMNS), np.int8)

def draw_title():
    print("  ____                            _     _____                ")
    print(" / ___|___  _ __  _ __   ___  ___| |_  |  ___|__  _   _ _ __ ")
    print("| |   / _ \| '_ \| '_ \ / _ \/ __| __| | |_ / _ \| | | | '__|")
    print("| |__| (_) | | | | | | |  __/ (__| |_  |  _| (_) | |_| | |   ")
    print(" \____\___/|_| |_|_| |_|\___|\___|\__| |_|  \___/ \__,_|_|\n")

def draw_game(board, turn, game_over=False, args=None):
    print("                     ╔═════════════════╗")
    for row in board:
        line = "\033[4;30;47m|\033[0m"
        for col, piece in enumerate(row):
            if piece == AI_2:
                line += "\033[4;34;47m●\033[0m"
            elif piece == AI_1:
                line += "\033[4;31;47m●\033[0m"
            else:
                line += "\033[4;30;47m \033[0m"
            line += "\033[4;30;47m|\033[0m"
        print("                     ║ " + line + " ║")
    print("                     ║  1 2 3 4 5 6 7  ║")
    print("                     ╚═════════════════╝\n")
    if not game_over:
        if turn == AI_1:
            print(f"Waiting for {args.player1}...")
        else:
            print(f"Waiting for {args.player2}...")

def start_game(args):
    board = create_board()
    turn = random.choice([AI_1, AI_2])
    is_game_won = False
    draw_title()
    draw_game(board, turn, args=args)

    # Do a random move
    place_piece(board, turn, random.choice([i for i in range(1, COLUMNS + 1)]))
    turn = AI_1 if turn == AI_2 else AI_2
    draw_game(board, turn, args=args)
    is_draw = board_full(board)
    total_moves = 1

    while not is_game_won and not is_draw:
        total_moves += 1
        depthOfCurrentPlayer = args.player1Depth if turn == AI_1 else args.player2Depth
        AI_move, minimax_value = move.minimax(board, depthOfCurrentPlayer, True, turn)
        place_piece(board, turn, AI_move)
        is_game_won = detect_win(board, turn)
        is_draw = board_full(board)
        turn = AI_1 if turn == AI_2 else AI_2
        if is_game_won:
            draw_game(board, turn, game_over=True, args=args)
            break
        else:
            draw_game(board, turn, args=args)

    winner = args.player1 if turn == AI_2 else args.player2
    if is_draw:
        print("Draw! Randomly selecting winner.")
        winner = args.player1 if random.choice([AI_1, AI_2]) == AI_1 else args.player2
    print(f"Winner: {winner}.")
    print("Total number of moves: %s" % total_moves)

def main():
    # Parse parameters
    parser = argparse.ArgumentParser(description='connect_four')
    parser.add_argument('--player1', type=str, required=False, default='Player 1', help='name of player 1')
    parser.add_argument('--player2', type=str, required=False, default='Player 2', help='name of player 2')
    parser.add_argument('--player1Depth', type=int, required=False, default=4, help='depth of player 1')
    parser.add_argument('--player2Depth', type=int, required=False, default=4, help='depth of player 2')
    args = parser.parse_args()

    start_game(args)

if __name__ == "__main__":
    main()
