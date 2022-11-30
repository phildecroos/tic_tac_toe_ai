import math
import random
from general import *
from network import *
from readwrite import *

# calculate the error of the network's outputs for a given data point
def cost(nodes, board, good_move):
    cost = 0
    outputs = get_outputs(nodes, board)

    for i in range(9):
        if i == good_move:
            good_output = 1
        else:
            good_output = 0
        cost += (good_output - outputs[i])**2

    return cost

# calculate the average cost of the network for a series of data points
def average_cost(nodes, situations):
    total_cost = 0
    for situation in situations:
        board = situation[0]
        good_move = situation[1]
        total_cost += cost(nodes, board, good_move)
    total_cost /= len(situations)
    return total_cost

# the fraction of moves in the dataset that the network gets right
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

# train the network by randomly making a change and keeping it if cost decreases
def train_random(nodes, learn_rate, situations):
    prev_cost = average_cost(nodes, situations)

    r_type = random.randint(0, 1)
    r_node = random.randint(0, 8)
    r_layer = random.randint(0, len(nodes[0]) - 2) # do not change output layer values
    r_value = random.randint(0, 8)
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

# a way to see progress while training
def print_status(i, nodes, situations):
    print("iterations: " + str(i) + ", cost: " + str(average_cost(nodes, situations)) + ", accuracy: " + str(accuracy(nodes, situations)))

def main():
    nodes = generate()
    read_params(nodes, "params_init.txt")
    for i in range(9):
        nodes[i][len(nodes[0]) - 1].weights[0] = 1.0
        nodes[i][len(nodes[0]) - 1].biases[0] = 0.0
    situations = read_situations()

    learn_rate = 0.5
    print_status(0, nodes, situations)
    i = 0
    while accuracy(nodes, situations) != 1.0:
        i += 1
        if i % 100 == 0:
            print_status(i, nodes, situations)
        train_random(nodes, learn_rate, situations)
    print_status(i, nodes, situations)

    write_params(nodes, "params_new.txt")

main()
