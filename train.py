import random
from general import *
from network import *
from readwrite import *

MAX_VALUE = 25

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

    return total_cost / len(situations)

# the fraction of moves in the dataset that the network gets right
def accuracy(nodes, situations):
    correct = 0.0

    for situation in situations:
        board = situation[0]
        good_move = situation[1]
        if find_move(nodes, board) == good_move:
            correct += 1

    return correct / len(situations)

# return a subset of the situations that the network doesn't clearly get right
def incorrect_points(nodes, situations):
    subset = []

    for situation in situations:
        board = situation[0]
        good_move = situation[1]
        if find_move(nodes, board) != good_move:
            subset.append(situation)
        else:
            outputs = get_outputs(nodes, board)
            first_choice = max(outputs)
            outputs[outputs.index(max(outputs))] = -1.0
            second_choice = max(outputs)
            if (first_choice - second_choice) < 0.5:
                subset.append(situation)

    return subset

# print what the network does for a dataset
def print_accuracy(nodes, situations):
    for situation in situations:
        board = situation[0]
        good_move = situation[1]
        print("\nboard" + str(board))
        print("good move: " + str(good_move))
        print("network outputs: " + str(get_outputs(nodes, board)))
        print("chosen move: " + str(find_move(nodes, board)))

# approximate the partial derivatives of cost wrt a node's weight
def calc_gradient(nodes, i, j, k, situations):
    derivative = 0
    change = 0.001

    prev_cost = average_cost(nodes, situations)
    nodes[i][j].weights[k] += change
    new_cost = average_cost(nodes, situations)
    nodes[i][j].weights[k] -= change

    derivative = ((new_cost - prev_cost) / change)
    return derivative

# train the network by moving all parameters along the negative cost gradient
def train_gradient(nodes, learn_rate, gradient, situations):
    for i in range(len(nodes)):
        for j in range(len(nodes[0]) - 1):
            for k in range(nodes[i][j].outputs):
                gradient[i][j][k] = calc_gradient(nodes, i, j, k, situations)

                # if the value is too small and the gradient wants it to get smaller, change its sign
                # otherwise keep applying fractional changes
                # this lets values cross zero if the other side is where their ideal value is
                if (abs(nodes[i][j].weights[k]) < 0.1) and (abs(nodes[i][j].weights[k] - 0.01 * gradient[i][j][k]) < abs(nodes[i][j].weights[k])):
                    nodes[i][j].weights[k] = -1 * nodes[i][j].weights[k]
                else:
                    nodes[i][j].weights[k] -= learn_rate * gradient[i][j][k]
                
                # cap the values at upper and lower bounds
                if nodes[i][j].weights[k] > MAX_VALUE:
                    nodes[i][j].weights[k] = MAX_VALUE
                elif nodes[i][j].weights[k] < -1 * MAX_VALUE:
                    nodes[i][j].weights[k] = -1 * MAX_VALUE

# randomize parameters
def rand_params(nodes):
    for i in range(len(nodes)):
        for j in range(len(nodes[0]) - 1):
            for k in range(nodes[i][j].outputs):
                nodes[i][j].weights[k] = random.random() + random.randint(-1, 1)

# a way to see progress while training
def print_status(i, nodes, situations):
    print("iteration: " + str(i) + 
          ", cost: " + str(average_cost(nodes, situations)) + 
          ", accuracy: " + str(accuracy(nodes, situations)) +
          ", bad points: " + str(len(incorrect_points(nodes, situations))))

def main():
    nodes = generate()
    for i in range(9):
        nodes[i][len(nodes[0]) - 1].weights[0] = 1.0
    situations = read_situations("situations.txt")

    gradient = []
    for i in range(len(nodes)):
        gradient.append([])
        for j in range(len(nodes[0]) - 1):
            gradient[i].append([])
            for k in range(nodes[i][j].outputs):
                gradient[i][j].append(1)

    rand_params(nodes)
    write_params(nodes, "params_init.txt")

    i = 0
    
    while (accuracy(nodes, situations) < 1.0):
        i += 1
        print_status(i, nodes, situations)
        train_gradient(nodes, 100, gradient, situations)
        write_params(nodes, "params_new.txt")
    
    write_params(nodes, "params_best.txt")
    print_status(i, nodes, situations)
    print("found a solution!")

main()