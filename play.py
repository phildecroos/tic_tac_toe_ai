import random
from general import *
from network import *
from readwrite import *

def player_move(board):
    move = -1
    while move not in avail_moves(board):
        move = input("\nenter your move (X): ")
        if move.isnumeric():
            move = int(move)
    return move

def main():
    clear()
    
    nodes = generate()
    read_params(nodes, "params_new.txt")

    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    curr_player = random.randint(1, 2)

    while not check_end(board):
        clear()
        print_board(board)
        if curr_player == 1:
            board[player_move(board)] = 1
            curr_player = 2
        else:
            board[find_move(nodes, board)] = 2
            curr_player = 1

    result = check_end(board)
    if result == 1:
        clear()
        print_board(board)
        print("\nyou won :)")
    elif result == 2:
        clear()
        print_board(board)
        print("\nyou lost :(")
    elif result == -1:
        clear()
        print_board(board)
        print("\ndraw :|")

main()