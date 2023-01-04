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
        print("draws: " + str(self.draws))
        print("losses: " + str(self.losses))

def random_move(board):
    move = -1
    while move not in avail_moves(board):
        move = random.randint(0, 8)
    return move

def play(player, nodes, games):
    wins = 0
    losses = 0
    draws = 0

    for i in range(games):
        board = [0 for i in range(9)]
        curr_player = random.randint(0, 1)
        if curr_player == 0:
            curr_player = -1
        
        while check_end(board) == 0:
            if curr_player == 1:
                board[random_move(board)] = 1
            else:
                if player == "nn":
                    board[find_move(nodes, board)] = -1
                elif player == "bm":
                    board[best_move(board.count(0), -1, board)] = -1
            curr_player *= -1

        result = check_end(board)
        if result == -1:
            wins += 1
        elif result == 2:
            draws += 1
        elif result == 1:
            losses += 1
    
    return Test_Results(games, wins, draws, losses)

def main():
    nodes = generate()
    read_params(nodes, "params_new.txt")
    
    # no need (and code doesnt currently allow) for the network to play against best_move
    # run accuracy() on the network to see how similarly it acts to best_move (ideally it's the same)
    # the point of the neural network is to be a more efficient way of getting those "best moves"
    # it runs significantly faster, and if it is trained properly it will generate the same results

    # print("\nnetwork vs random")
    # results = play("nn", nodes, 10000)
    # results.print_results()

    print("\nbest_move vs random")
    results = play("bm", nodes, 200)
    results.print_results()

main()