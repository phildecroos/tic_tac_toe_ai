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
    #clear()
    
    nodes = generate()
    read_params(nodes, "params_new.txt")

    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    curr_player = random.randint(0, 1)
    if not curr_player:
        curr_player = -1

    while not check_end(board):
        #clear()
        print_board(board)
        if curr_player == 1:
            board[player_move(board)] = 1
            curr_player = -1
        else:
            board[find_move(nodes, board)] = -1
            curr_player = 1

    result = check_end(board)
    if result == 1:
        #clear()
        print_board(board)
        print("\nyou won :)")
    elif result == -1:
        #clear()
        print_board(board)
        print("\nyou lost :(")
    elif result == 2:
        #clear()
        print_board(board)
        print("\ndraw :|")

main()