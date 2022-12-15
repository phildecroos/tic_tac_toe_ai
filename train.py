import random
from general import *
from network import *
from readwrite import *

MAX_VALUE = 25

# calculate the error of the network's outputs for a given data point
def cost(nodes, board, good_move):
    cost = 0
    outputs = get_outputs(nodes, board)

    for i in range(len(outputs)):
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

    for situation in situations:
        board = situation[0]
        good_move = situation[1]
        if find_move(nodes, board) == good_move:
            right += 1

    return right / len(situations)

# return a subset of the situations that the network doesn't clearly get right
def incorrect_points(nodes, situations):
    subset = []

    for situation in situations:
        board = situation[0]
        good_move = situation[1]
        if (find_move(nodes, board) != good_move) or (cost(nodes, board, good_move) > 1):
            subset.append(situation)

    return subset

# print what the network does for a dataset
def print_accuracy(nodes, situations):
    for situation in situations:
        board = situation[0]
        good_move = situation[1]
        print("")
        print("board" + str(board))
        print("good move: " + str(good_move))
        print("network outputs: " + str(get_outputs(nodes, board)))
        print("chosen move: " + str(find_move(nodes, board)))

# train the network by randomly making a change and keeping it if cost decreases
def train_random(nodes, learn_rate, situations):
    for i in range(len(nodes)):
        for j in range(len(nodes[0]) - 1):
            prev_cost = average_cost(nodes, situations)

            r_type = random.randint(0, 1)
            r_value = random.randint(0, 8)
            r_sign = random.randint(0, 1)
            if r_sign == 0:
                r_sign = -1

            if r_type == 0:
                change = learn_rate * r_sign * nodes[i][j].weights[r_value]
                nodes[i][j].weights[r_value] += change
                if abs(nodes[i][j].weights[r_value]) < 0.1:
                    nodes[i][j].weights[r_value] = -1 * nodes[i][j].weights[r_value]
                    change = 2 * nodes[i][j].weights[r_value]
                elif nodes[i][j].weights[r_value] > MAX_VALUE:
                    nodes[i][j].weights[r_value] = MAX_VALUE
                    change = 0
                elif nodes[i][j].weights[r_value] < -1 * MAX_VALUE:
                    nodes[i][j].weights[r_value] = -1 * MAX_VALUE
                    change = 0
            else:
                change = learn_rate * r_sign * nodes[i][j].biases[r_value]
                nodes[i][j].biases[r_value] += change
                if abs(nodes[i][j].biases[r_value]) < 0.1:
                    nodes[i][j].biases[r_value] = -1 * nodes[i][j].biases[r_value]
                    change = 2 * nodes[i][j].biases[r_value]
                elif nodes[i][j].biases[r_value] > MAX_VALUE:
                    nodes[i][j].biases[r_value] = MAX_VALUE
                    change = 0
                elif nodes[i][j].biases[r_value] < -1 * MAX_VALUE:
                    nodes[i][j].biases[r_value] = -1 * MAX_VALUE
                    change = 0
            
            new_cost = average_cost(nodes, situations)

            if new_cost > prev_cost:
                if r_type == 0:
                    nodes[i][j].weights[r_value] -= change
                else:
                    nodes[i][j].biases[r_value] -= change

# approximate the partial derivative of cost wrt a node's weight and bias
def calc_gradient(nodes, i, j, k, situations):
    changes = [0, 0]
    for l in range(2):
        prev_cost = average_cost(nodes, situations)
        if l == 0:
            change = 0.01 * nodes[i][j].weights[k]
            nodes[i][j].weights[k] += change
            new_cost = average_cost(nodes, situations)
            nodes[i][j].weights[k] -= change
        else:
            change = 0.01 * nodes[i][j].biases[k]
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
                if abs(nodes[i][j].weights[k]) < 0.1:
                    nodes[i][j].weights[k] = -1 * nodes[i][j].weights[k]
                elif nodes[i][j].weights[k] > MAX_VALUE:
                    nodes[i][j].weights[k] = MAX_VALUE
                elif nodes[i][j].weights[k] < -1 * MAX_VALUE:
                    nodes[i][j].weights[k] = -1 * MAX_VALUE

                nodes[i][j].biases[k] += learn_rate * gradient[i][j][k][1]
                if abs(nodes[i][j].biases[k]) < 0.1:
                    nodes[i][j].biases[k] = -1 * nodes[i][j].biases[k]
                elif nodes[i][j].biases[k] > MAX_VALUE:
                    nodes[i][j].biases[k] = MAX_VALUE
                elif nodes[i][j].biases[k] < -1 * MAX_VALUE:
                    nodes[i][j].biases[k] = -1 * MAX_VALUE

    new_cost = average_cost(nodes, situations)
    return new_cost - prev_cost

# randomize parameters
def rand_params(nodes):
    for i in range(len(nodes)):
        for j in range(len(nodes[0]) - 1):
            for k in range(nodes[i][j].outputs):
                nodes[i][j].weights[k] = random.random() + random.randint(-1, 1)
                nodes[i][j].biases[k] = random.random() + random.randint(-1, 1)

# a way to see progress while training
def print_status(i, nodes, situations):
    print("iterations: " + str(i) + ", cost: " + str(average_cost(nodes, situations)) + ", accuracy: " + str(accuracy(nodes, situations)) + ", bad points: " + str(len(incorrect_points(nodes, situations))))

def main():
    nodes = generate()
    for i in range(9):
        nodes[i][len(nodes[0]) - 1].weights[0] = 1.0
        nodes[i][len(nodes[0]) - 1].biases[0] = 0.0
    situations = read_situations("situations.txt")

    gradient = []
    for i in range(len(nodes)):
        gradient.append([])
        for j in range(len(nodes[0]) - 1):
            gradient[i].append([])
            for k in range(nodes[i][j].outputs):
                gradient[i][j].append([1, 1])

    rand_params(nodes)
    #read_params(nodes, "params_new.txt")
    write_params(nodes, "params_init.txt")

    i = 0
    '''
    # train to whole dataset
    while (accuracy(nodes, situations) != 1.0):
        print_status(i, nodes, situations)
        i += 1
        #train_random(nodes, 0.2, situations)
        train_gradient(nodes, 10, gradient, situations)
        write_params(nodes, "params_new.txt")
    '''
    
    # train to the subset of the data that the network gets the most wrong
    # more of an 
    while (accuracy(nodes, situations) != 1.0):
        print_status(i, nodes, situations)
        i += 1
        #train_random(nodes, 0.2, incorrect_points(nodes, situations))
        train_gradient(nodes, 10, gradient, incorrect_points(nodes, situations))
        write_params(nodes, "params_new.txt")
    
    if accuracy(nodes, situations) == 1.0:
        write_params(nodes, "params_best.txt")
        print("found a solution! cost: " + str(average_cost(nodes, situations)) + ", accuracy: " + str(accuracy(nodes, situations)))

main()
