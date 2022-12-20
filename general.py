import os

# clear the console
def clear():
    os.system("cls")
    print("")
    os.system("cls")

# print a readable tic tac toe board
def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("")

        if board[i] == 0:
            print("[ ]", end="")
        elif board[i] == 1:
            print("[X]", end="")
        elif board[i] == -1:
            print("[O]", end="")

# find available moves on a given board
def avail_moves(board):
    output = []
    for i in range(9):
        if board[i] == 0:
            output.append(i)
    return output

# check a given board to see if the game is over
def check_end(board):
    winner = 0

    if board[0] == board[1] and board[1] == board[2] and board[2] != 0:
        winner = board[0]
    if board[3] == board[4] and board[4] == board[5] and board[5] != 0:
        winner = board[3]
    if board[6] == board[7] and board[7] == board[8] and board[8] != 0:
        winner = board[6]
    if board[0] == board[3] and board[3] == board[6] and board[6] != 0:
        winner = board[0]
    if board[1] == board[4] and board[4] == board[7] and board[7] != 0:
        winner = board[1]
    if board[2] == board[5] and board[5] == board[8] and board[8] != 0:
        winner = board[2]
    if board[0] == board[4] and board[4] == board[8] and board[8] != 0:
        winner = board[0]
    if board[2] == board[4] and board[4] == board[6] and board[6] != 0:
        winner = board[2]

    # winner
    if winner != 0:
        return winner
    # game is not over
    if board.count(0) > 0:
        return 0
    # draw
    return 2

# return the opposite player of the input
def change_turn(mover):
    return -1 * mover

# get the number of possible games from a certain starting board
def possibilities(depth, board):
    count = 0
    for i in range(9):
        if board[i] == 0:
            count += 1
    cases = count
    for i in range(count):
        if i < depth - 1:
            count -= 1
            cases *= count
    return cases

# get the # of non-losing outcomes for the ai from a certain starting board
# if the starting board is won/drawn, put the check_end output in gameover
def good_outcomes(depth, mover, board, gameover):
    wins = 0
    save_board = board.copy()

    if depth > 0:
        for move in avail_moves(board):
            board[move] = mover
            newmover = change_turn(mover)
            if gameover == -1 or (gameover == 0 and check_end(board) == -1):
                if depth > 1:
                    wins += good_outcomes(depth - 1, newmover, board, 2)
                else:
                    wins += 1
            elif gameover == 2 or (gameover == 0 and check_end(board) == 2):
                wins += 1
            elif check_end(board) == 0 and depth > 1:
                wins += good_outcomes(depth - 1, newmover, board, 0)
            board = save_board.copy()
    return wins

# find which move has the highest number of non-losing outcomes for the ai
def best_move(depth, mover, board):
    wins = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    save_board = board.copy()
    local_board = save_board.copy()

    if mover == -1:
        # if the ai can win the game in 1 move it will choose that
        for move in avail_moves(local_board):
            local_board[move] = -1
            if check_end(local_board) == -1:
                return move
            local_board = save_board.copy()

        # if the ai can lose the game in 1 move the ai will take that square
        for move in avail_moves(local_board):
            local_board[move] = 1
            if check_end(local_board) == 1:
                return move
            local_board = save_board.copy()

    for move in avail_moves(local_board):
        local_board[move] = mover
        newmover = change_turn(mover)
        wins[move] += good_outcomes(depth - 1, newmover, local_board, check_end(local_board))
        local_board = save_board.copy()

    for i in range(9):
        max_index = wins.index(max(wins))
        if max_index in avail_moves(local_board):
            return max_index
        else:
            wins[max_index] = 0.0
    return -1