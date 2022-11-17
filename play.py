# def function that prints a readable tic tac toe board
def print_board(board):
    for i in range(9):
        if i % 3 == 0:
            print("")

        if board[i] == 0:
            print("[ ]", end="")
        elif board[i] == -1:
            print("[O]", end="")
        elif board[i] == 1:
            print("[X]", end="")