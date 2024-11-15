DEPTH = 4
ROWS = 6
COLUMNS = 7
EMPTY = 0
AI_2 = 1
AI_1 = 2
MAX_SPACE_TO_WIN = 3 # Farthest space where a winning connection may start

def place_piece(board, player, column):
    index = column - 1
    for row in reversed(range(ROWS)):
        if board[row][index] == EMPTY:
            board[row][index] = player
            return
        
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
            print(f"Waiting for {args.player1} to make a move...")
        else:
            print(f"Waiting for {args.player2} to make a move...")

# Checks if the player won the given board
def detect_win(board, player):
    # Horizontal win
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS):
            if board[row][col] == player and board[row][col+1] == player and \
                    board[row][col+2] == player and board[row][col+3] == player:
                return True
    # Vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            if board[row][col] == player and board[row+1][col] == player and \
                    board[row+2][col] == player and board[row+3][col] == player:
                return True
    # Diagonal upwards win
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            if board[row][col] == player and board[row+1][col+1] == player and \
                    board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True
    # Diagonal downwards win
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(MAX_SPACE_TO_WIN, ROWS):
            if board[row][col] == player and board[row-1][col+1] == player and \
                    board[row-2][col+2] == player and board[row-3][col+3] == player:
                return True
    return False

# Checks if column is full or not
def is_valid_column(board, column):
    return board[0][column - 1] == EMPTY

# Returns list of columns that are still not full
def valid_locations(board):
    valid_locations = []
    for i in range(1,8):
        if is_valid_column(board, i):
            valid_locations.append(i)
    return valid_locations

def board_full(board):
    return len(valid_locations(board)) == 0
