# Connect Four

The goal of this project is to let two Minimax artificial intelligence agents compete in a game of Connect Four. While the first move is selected randomly, the remaining moves are determined by the agents. 

Connect Four is a two-player game which consists of a vertical board of six rows by seven columns. Each player has twenty-one pieces of the same color and they take turns to drop a piece in one of the seven columns. The piece will drop down to the lowest unoccupied row. A player wins when they manage to get four consecutive pieces of the same color either horizontal, vertical or diagonally. Although the game is deterministic, it would require four terabytes of memory to keep all possible legal board combinations.

In order to build an artificial intelligence agent, an algorithm called Minimax can be used. The basic function of the algorithm is to look ahead (`DEPTH` variable in [common.py](common.py)) and choose the move that leads it to the best possible outcome. The Minimax algorithm will look ahead and choose the best move it can play. The more moves that it can look ahead, the better it will be at winning. However, this also increases the running time of the algorithm.

## Usage

```bash
python game.py
```

## Credits

Inspired by [https://github.com/bryanjsanchez/Parallel-Connect-Four](https://github.com/bryanjsanchez/Parallel-Connect-Four).
