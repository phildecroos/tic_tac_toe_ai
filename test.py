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


def play(player, games, nodes, situations):
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
                elif player == "ds":
                    board[search_move(board, situations)] = -1
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
    read_params(nodes, "good_params/12nodes_97percent_params.txt")
    situations = read_situations("situations.txt")

    print("\nnetwork vs random")
    results = play("nn", 10000, nodes, situations)
    results.print_results()

    print("\ndataset searcher vs random")
    results = play("ds", 10000, nodes, situations)
    results.print_results()

    print("\nbest_move vs random")
    results = play("bm", 10000, nodes, situations)
    results.print_results()


main()
