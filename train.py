import math
import random
from general import *
from network import *
from readwrite import *

# calculate the error of the network's outputs in a given situation
def cost(nodes, board, good_move):
    cost = 0

    # output layer cost
    for i in range(9):
        if i == good_move:
            good_output = 1
        else:
            good_output = 0
        input = 0
        for j in range(9):
            input += nodes[j][0].get_output(i, board[j])
        input = nodes[i][1].get_input([input])
        cost += nodes[i][1].node_cost(0, input, good_output)

    return cost

# calculate the average cost of the network for a series of situations
def average_cost(nodes, situations):
    total_cost = 0
    for situation in situations:
        board = situation[0]
        good_move = situation[1]
        total_cost += cost(nodes, board, good_move)
    total_cost /= len(situations)
    return total_cost

def accuracy(nodes, situations):
    right = 0.0
    wrong = 0.0
    for situation in situations:
        board = situation[0]
        good_move = situation[1]
        if find_move(nodes, board) == good_move:
            right += 1
        else:
            wrong += 1
    return right / (right + wrong)

def convergence(nodes, situations):
    converged = True
    for i in range(10): # 10 isnt actually enough to ensure it will consistently pick the moves in the dataset
        if accuracy(nodes, situations) != 1:
            converged = False
    return converged

# train the network by randomly making a change and keeping it if cost decreases
def train_random(nodes, learn_rate, situations):
    prev_cost = average_cost(nodes, situations)

    r_type = random.randint(0, 1)
    r_node = random.randint(0, 8)
    r_layer = random.randint(0, 1)
    if r_layer == 0:
        r_value = random.randint(0, 8)
    else:
        r_value = 0
    r_sign = random.randint(0, 1)
    if not r_sign:
        r_sign = -1

    if r_type == 0:
        change = learn_rate * r_sign * nodes[r_node][r_layer].weights[r_value]
        nodes[r_node][r_layer].weights[r_value] += change
    else:
        change = learn_rate * r_sign * nodes[r_node][r_layer].biases[r_value]
        nodes[r_node][r_layer].biases[r_value] += change
    
    new_cost = average_cost(nodes, situations)

    if new_cost > prev_cost:
        if r_type == 0:
            nodes[r_node][r_layer].weights[r_value] -= change
        else:
            nodes[r_node][r_layer].biases[r_value] -= change
    
    return new_cost - prev_cost

# train the network by changing all parameters along the negative gradient of cost
def train_gradient(nodes, learn_rate, situations):
    prev_cost = average_cost(nodes, situations)

    # calculate gradient of cost function
    # apply the respective changes to each parameter

    new_cost = average_cost(nodes, situations)

    return new_cost - prev_cost

def main():
    nodes = generate()

    read_params(nodes, "params_init.txt")

    # dataset to train network to (situation-move pairs)
    situations = read_situations()
    learn_rate = 0.5
    print(average_cost(nodes, situations))
    print(accuracy(nodes, situations))
    while not convergence(nodes, situations):
        train_random(nodes, learn_rate, situations)
    print(average_cost(nodes, situations))
    print(accuracy(nodes, situations))

    write_params(nodes, "params_new.txt")

main()
