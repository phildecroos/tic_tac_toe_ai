'''
In this implementation of a machine learning bot, I did not know how to make a 
neural network.
This was designed to learn by recording every situation the bot had been in 
before and whether or not it won the game after making the move it chose.
This approach is very slow, as every time the bot wants to refer back to it's 
previous experience it has to parse a list of every situation it has ever
encountered.
In theory it would work, but I encountered numerous bugs that I couldn't figure
out how to fix, so I decided to learn how to make a neural network instead.
'''

import os
import random
import csv

# number of games to play
games = 100000

def placed(game_state, check, val):
    return (game_state.find(val) != -1 and game_state.find(val) % 2 == check)

def game_over(game_state):
    check = (len(game_state) - 1) % 2

    if placed(game_state, check, "0") and placed(game_state, check, "1") and placed(game_state, check, "2"):
        return True
    if placed(game_state, check, "0") and placed(game_state, check, "3") and placed(game_state, check, "6"):
        return True
    if placed(game_state, check, "0") and placed(game_state, check, "4") and placed(game_state, check, "8"):
        return True
    if placed(game_state, check, "1") and placed(game_state, check, "4") and placed(game_state, check, "7"):
        return True
    if placed(game_state, check, "2") and placed(game_state, check, "4") and placed(game_state, check, "6"):
        return True
    if placed(game_state, check, "2") and placed(game_state, check, "5") and placed(game_state, check, "8"):
        return True
    if placed(game_state, check, "3") and placed(game_state, check, "4") and placed(game_state, check, "5"):
        return True
    if placed(game_state, check, "6") and placed(game_state, check, "7") and placed(game_state, check, "8"):
        return True
    
    if len(game_state) == 10:
        return True
    
    return False

def random_move(free_moves):
    new_move = random.randint(0, 8)
    while not new_move in free_moves:
        new_move = random.randint(0, 8)
    free_moves.remove(new_move)
    return str(new_move)

def outcome(game):
    return 1

for i in range(games):
    curr_game = ""
    free_moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    situations = []
    repeat_sits = []
    
    first_player = random.randint(0, 1)
    if first_player:
        curr_game += "x"
        turn = "x"
    else:
        curr_game += "o"
        turn = "o"
    
    
    while not game_over(curr_game):
        if turn == "o":
            curr_game += random_move(free_moves)
            turn = "x"
        else:
            with open("experience.txt", "r") as exp:
                for line in exp:
                    if (curr_game + ":") in line:
                        repeat_sits.append(line)
                        ranks = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                        for i in range(9):
                            if line[-1 * (i + 2)] != "-":
                                ranks[8 - i] += int(line[-1 * (i + 2)])
                        # change this to randomly select from all moves with the max score and not just use max()
                        curr_game += str(ranks.index(max(ranks)))
                        turn = "o"
                        break
                if turn == "x":
                    curr_game += random_move(free_moves)
                    turn = "o"
                situations.append(curr_game)

    for i in situations:
        # make code for the outcome() function
        if outcome(curr_game) == 1:
            score_change = 1
        elif outcome(curr_game) == 0:
            score_change = 0
        else:
            score_change = -5
        
        # need to find a way to start above zero so that bad moves can be ranked lower
        scores = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        scores[int(i[-1])] += score_change
        
        sit = ""
        for j in range(len(i) - 1):
            sit += i[j]

        with open("experience.txt", "r+") as exp:
            for line in exp:
                if (sit + ":") in line:
                    for j in range(9):
                        if line[j + len(i)] != "-":
                            scores[j] += int(line[j + len(i)])
                    break

            for j in range(len(i) - 1):
                exp.write(i[j])
            
            exp.write(":")
            
            for j in range(9):
                if str(j) in i and str(j) != i[-1]:
                    exp.write("-")
                else:
                    if scores[j] > 9:
                        exp.write("9")
                    elif scores[j] < 0:
                        exp.write("0")
                    else:
                        exp.write(str(scores[j]))

            exp.write("\n")
            # still have to add code that deletes the old row for that situation
            
