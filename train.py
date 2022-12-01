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
    for i in range(len(nodes)):
        for j in range(len(nodes[0]) - 1):
            prev_cost = average_cost(nodes, situations)

            r_type = random.randint(0, 1)
            r_value = random.randint(0, 8)
            r_sign = random.randint(0, 1)
            if not r_sign:
                r_sign = -1

            if r_type == 0:
                change = learn_rate * r_sign * nodes[i][j].weights[r_value]
                nodes[i][j].weights[r_value] += change
            else:
                change = learn_rate * r_sign * nodes[i][j].biases[r_value]
                nodes[i][j].biases[r_value] += change
            
            new_cost = average_cost(nodes, situations)

            if new_cost > prev_cost:
                if r_type == 0:
                    nodes[i][j].weights[r_value] -= change
                else:
                    nodes[i][j].biases[r_value] -= change

# calculate approximation of the partial derivative of cost wrt a parameter
def calc_gradient(nodes, i, j, k, situations):
    changes = [0, 0]
    for l in range(2):
        prev_cost = average_cost(nodes, situations)
        if l == 0:
            change = 0.5 * nodes[i][j].weights[k]
            nodes[i][j].weights[k] += change
            new_cost = average_cost(nodes, situations)
            nodes[i][j].weights[k] -= change
        else:
            change = 0.5 * nodes[i][j].biases[k]
            nodes[i][j].biases[k] += change
            new_cost = average_cost(nodes, situations)
            nodes[i][j].biases[k] -= change
        if new_cost > prev_cost:
            change *= -1
        changes[l] = change
    return changes

# train the network by changing all parameters along the negative gradient of cost
def train_gradient(nodes, learn_rate, gradient, situations):
    prev_cost = average_cost(nodes, situations)

    for i in range(len(nodes)):
        for j in range(len(nodes[0]) - 1):
            for k in range(nodes[i][j].outputs):
                gradient[i][j][k] = calc_gradient(nodes, i, j, k, situations)
                nodes[i][j].weights[k] += learn_rate * gradient[i][j][k][0]
                nodes[i][j].biases[k] += learn_rate * gradient[i][j][k][1]

    new_cost = average_cost(nodes, situations)
    return new_cost - prev_cost

# randomize parameters
def rand_params(nodes):
    for i in range(len(nodes)):
        for j in range(len(nodes[0]) - 1):
            for k in range(nodes[i][j].outputs):
                nodes[i][j].weights[k] = random.random() + random.randint(0, 1)
                nodes[i][j].biases[k] = random.random() + random.randint(0, 1)

# a way to see progress while training
def print_status(i, nodes, situations):
    print("iterations: " + str(i) + ", cost: " + str(average_cost(nodes, situations)) + ", accuracy: " + str(accuracy(nodes, situations)))

def main():
    # set up network
    nodes = generate()
    read_params(nodes, "params_init.txt") # not needed if randomizing start point
    for i in range(9):
        nodes[i][len(nodes[0]) - 1].weights[0] = 1.0
        nodes[i][len(nodes[0]) - 1].biases[0] = 0.0
    situations = read_situations()

    gradient = []
    for i in range(len(nodes)):
        gradient.append([])
        for j in range(len(nodes[0]) - 1):
            gradient[i].append([])
            for k in range(nodes[i][j].outputs):
                gradient[i][j].append([1, 1])
    training = True
    lowest_cost = 9
    learn_rate = 1
    i = 0
    while (training):
        i += 1
        rand_params(nodes)
        curr_cost = average_cost(nodes, situations)
        if curr_cost < lowest_cost:
            lowest_cost = curr_cost
            write_params(nodes, "params_init.txt")
        print("attempt: " + str(i) + ", cost: " + str(curr_cost) + ", lowest: " + str(lowest_cost))
        if curr_cost < 2.25:
            print("FOUND A GOOD STARTING POINT!!!")
            write_params(nodes, "params_init.txt")
            i = 0
            training = False
            cost_change = -1
            while accuracy(nodes, situations) != 1.0 and cost_change < 0:
                i += 1
                cost_change = train_gradient(nodes, learn_rate, gradient, situations)
                write_params(nodes, "params_new.txt")
                print_status(i, nodes, situations)

    print_status("finished", nodes, situations)
    write_params(nodes, "params_new.txt")

main()
