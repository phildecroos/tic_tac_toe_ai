import os
import random
from general import *
from network import *
from readwrite import *

clear = lambda: os.system('cls')

nodes = generate()
read_params(nodes, "params_new.txt")

board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
curr_player = random.randint(1, 2)

while not check_end(board):
    clear()
    print_board(board)
    if curr_player == 1:
        player_move = -1
        while player_move not in avail_moves(board):
            player_move = input("\nenter your move (X): ")
            if player_move.isnumeric():
                player_move = int(player_move)
        board[player_move] = 1
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