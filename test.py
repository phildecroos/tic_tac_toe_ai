import random
from general import *
from network import *
from readwrite import *

class Test_Results:
    def __init__(self, games, wins, draws, losses):
        self.games = games
        self.wins = wins
        self.draws = draws
        self.losses = losses
    
    def print_results(self):
        print(str(self.games) + " games")
        print("wins: " + str(self.wins))
        print("losses: " + str(self.losses))
        print("draws: " + str(self.draws))

def random_move(board):
    move = -1
    while move not in avail_moves(board):
        move = random.randint(0, 9)
    return move

def play_random(nodes, games):
    wins = 0
    losses = 0
    draws = 0

    for i in range(games):
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        curr_player = random.randint(0, 1)
        if curr_player == 0:
            curr_player = -1
        
        while not check_end(board):
            if curr_player == 1:
                board[random_move(board)] = 1
                curr_player = -1
            else:
                board[find_move(nodes, board)] = -1
                curr_player = 1

        result = check_end(board)
        if result == 1:
            losses += 1
        elif result == -1:
            wins += 1
        elif result == 2:
            draws += 1
    
    return Test_Results(games, wins, draws, losses)

def main():
    nodes = generate()
    read_params(nodes, "params_new.txt")
    
    print("random")
    random_results = play_random(nodes, 1000)
    random_results.print_results()
    

main()