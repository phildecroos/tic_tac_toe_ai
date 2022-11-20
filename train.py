import math
import random
from general import *
from network import *
from readwrite import *

# calculate the error of the network's outputs in a given situation
def network_cost(nodes, board, good_move):
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

def train_random(nodes, learn_rate, situations):
    prev_cost = 0
    for situation in situations:
        board = situation[0]
        good_move = situation[1]
        prev_cost += network_cost(nodes, board, good_move)

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
    
    new_cost = 0
    for situation in situations:
        board = situation[0]
        good_move = situation[1]
        new_cost += network_cost(nodes, board, good_move)

    if new_cost > prev_cost:
        if r_type == 0:
            nodes[r_node][r_layer].weights[r_value] -= change
        else:
            nodes[r_node][r_layer].biases[r_value] -= change
    
    return new_cost - prev_cost

def main():
    nodes = generate()

    read_params(nodes, "params_init.txt")

    # dataset to train network to (situation-move pairs)
    situations = [[[0, 0, 0, 0, 0, 0, 0, 0, 0], 4], [[2, 2, 0, 1, 1, 0, 0, 0, 0], 2]]
    print_board(situations[0][0])
    learn_rate = 0.1
    for i in range(100):
        train_random(nodes, learn_rate, situations)

    write_params(nodes, "params_new.txt")

main()
