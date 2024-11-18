import argparse
import numpy as np
import random
from common import *
import boto3
import json
import asyncio
import nats
from nats.js.api import KeyValueConfig

import sys
sys.stdout.reconfigure(line_buffering=True)

lambda_client = boto3.client('lambda', region_name='us-east-1')

def create_board():
    return np.zeros((ROWS, COLUMNS), np.int8)

def draw_title():
    print("  ____                            _     _____                ")
    print(" / ___|___  _ __  _ __   ___  ___| |_  |  ___|__  _   _ _ __ ")
    print("| |   / _ \\| '_ \\| '_ \\ / _ \\/ __| __| | |_ / _ \\| | | | '__|")
    print("| |__| (_) | | | | | | |  __/ (__| |_  |  _| (_) | |_| | |   ")
    print(" \\____\\___/|_| |_|_| |_|\\___|\\___|\\__| |_|  \\___/ \\__,_|_|\\n")

def start_game(args):
    print("Initializing new game...")
    board = create_board()
    turn = random.choice([AI_1, AI_2])
    is_game_won = False
    draw_title()
    draw_game(board, turn, args=args)
    print(f"Game started. First move by: {'AI_1' if turn == AI_1 else 'AI_2'}")

    # Initial random move
    place_piece(board, turn, random.choice([i for i in range(1, COLUMNS + 1)]))
    turn = AI_1 if turn == AI_2 else AI_2
    draw_game(board, turn, args=args)
    is_draw = board_full(board)
    total_moves = 1

    while not is_game_won and not is_draw:
        total_moves += 1
        depthOfCurrentPlayer = args.player1Depth if turn == AI_1 else args.player2Depth
        print(f"Calculating move for {'AI_1' if turn == AI_1 else 'AI_2'} with depth {depthOfCurrentPlayer}...")
        AI_move, minimax_value = get_move_from_lambda(board, turn, depthOfCurrentPlayer)
        place_piece(board, turn, AI_move)
        is_game_won = detect_win(board, turn)
        is_draw = board_full(board)
        turn = AI_1 if turn == AI_2 else AI_2

        if is_game_won:
            print("Game won! Displaying final board...")
            draw_game(board, turn, game_over=True, args=args)
            break
        else:
            draw_game(board, turn, args=args)

    winner = args.player1 if turn == AI_2 else args.player2
    if is_draw:
        print("The game is a draw. Randomly selecting a winner.")
        winner = args.player1 if random.choice([AI_1, AI_2]) == AI_1 else args.player2
    print(f"Winner: {winner}. Total number of moves: {total_moves}")

    return {
        "winner": winner,
        "board": board.tolist(),
        "total_moves": total_moves
    }

def get_move_from_lambda(board, player, depth):
    print("Requesting move from Lambda function...")
    board_list = board.tolist()
    payload = {
        "board": board_list,
        "player": player,
        "depth": depth
    }
    response = lambda_client.invoke(
        FunctionName='game-move-function',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    response_payload = json.loads(response['Payload'].read())
    result = response_payload['body']
    print(f"Received move: {result['column']} with score {result['score']}")
    return result['column'], result['score']

async def run_game_with_nats(args):
    print("Connecting to NATS server at nats://nats-server:4222...")
    nc = await nats.connect("nats://nats-server:4222")
    print("Connected to NATS server.")

    # Set up JetStream for KV storage
    js = nc.jetstream()
    kv = await js.create_key_value(KeyValueConfig(bucket="game_results"))

    async def e_start_handler(msg):
        print("Received e_start event in game. Starting game...")
        result = start_game(args)

        # Store the game result in KV store with the key 'latest_game'
        await kv.put("latest_game", json.dumps(result).encode())
        print("Stored game result in KV store under key 'latest_game'")

        # Publish result to e_end topic
        print("Publishing e_end event with game result...")
        await nc.publish("e_end", json.dumps(result).encode())
        print("Published e_end event.")

    # Subscribe to the e_start event
    print("Subscribing to e_start event...")
    await nc.subscribe("e_start", cb=e_start_handler)
    print("Subscription to e_start event successful.")

    while True:
        await asyncio.sleep(1)

async def main():
    parser = argparse.ArgumentParser(description='connect_four')
    parser.add_argument('--player1', type=str, required=False, default='Player 1', help='name of player 1')
    parser.add_argument('--player2', type=str, required=False, default='Player 2', help='name of player 2')
    parser.add_argument('--player1Depth', type=int, required=False, default=4, help='depth of player 1')
    parser.add_argument('--player2Depth', type=int, required=False, default=4, help='depth of player 2')
    args = parser.parse_args()

    await run_game_with_nats(args)

if __name__ == "__main__":
    print("Launching game manager...")
    asyncio.run(main())
    print("Game manager terminated.")
