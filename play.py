import random
from general import *
from network import *
from readwrite import *

# get a move from the user
def player_move(board):
    move = -1
    while move not in avail_moves(board):
        move = input("\nenter your move (X): ")
        if move.isnumeric():
            move = int(move)
    return move

def main():
    clear()

    # give the user the option to test the best move function instead
    opponent = ""
    while opponent != "nn" and opponent != "bm":
        opponent = input("choose an opponent ('nn' or 'bm'): ")
    
    nodes = generate()
    read_params(nodes, "good_params/11nodes_96percent_params.txt")

    board = [0 for i in range(9)]
    curr_player = random.randint(0, 1)
    if curr_player == 0:
        curr_player = -1

    result = 0
    while result == 0:
        clear()
        print_board(board)
        if curr_player == 1:
            board[player_move(board)] = 1
            curr_player = -1
        else:
            if opponent == "nn":
                board[find_move(nodes, board)] = -1
            elif opponent == "bm":
                board[best_move(board.count(0), -1, board)] = -1
            curr_player = 1
        result = check_end(board)

    clear()
    print_board(board)
    if result == 1:
        print("\nyou won :)")
    elif result == -1:
        print("\nyou lost :(")
    elif result == 2:
        print("\ndraw :|")

main()