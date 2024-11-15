import nats
from common import *
import asyncio
import json
import sys

sys.stdout.reconfigure(line_buffering=True)

async def main():
    print("Starting Manager...")

    # Connect to NATS
    print("Attempting to connect to NATS server at nats://nats-server:4222...")
    try:
        nc = await nats.connect("nats://nats-server:4222")
        print("Successfully connected to NATS server.")
    except Exception as e:
        print(f"Failed to connect to NATS server: {e}")
        return

    # Function to handle the end of a game
    async def e_end_handler(msg):
        data = json.loads(msg.data.decode())
        print("Received e_end event in manager.")
        print(f"Game ended. Winner: {data['winner']}")
        print(f"Final board state:\n{data['board']}")
        draw_game(data['board'], None, game_over = True)

        # Publish a new e_start event to start the next game after a brief delay
        await asyncio.sleep(2)
        print("Publishing e_start event to start a new game...")
        await nc.publish("e_start", b"Start game")
        print("e_start event published successfully.")

    # Subscribe to the e_end event to listen for game completions
    print("Subscribing to e_end event to listen for game completions...")
    try:
        await nc.subscribe("e_end", cb=e_end_handler)
        print("Subscribed to e_end event successfully.")
    except Exception as e:
        print(f"Failed to subscribe to e_end event: {e}")
        return

    await asyncio.sleep(10)

    # Trigger the start of the first game
    print("Publishing initial e_start event to start the first game...")
    await nc.publish("e_start", b"Start game")
    print("Initial e_start event published successfully.")
    # Keep the script running to continue receiving events
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    print("Launching Manager script...")
    asyncio.run(main())
    print("Manager script terminated.")
