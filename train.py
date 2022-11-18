import math
import os

clear = lambda: os.system('cls')

# read parameters from txt file
def read_params(nodes):
    readings = []

    with open("params.txt", "r") as doc:
        for line in doc:
            readings.append(line[0:-1])

    l = 0
    for i in range(9):
        for j in range(2):
            for k in range(nodes[i][j].outputs):
                nodes[i][j].weights[k] = float(readings[l])
                l += 1
                nodes[i][j].biases[k] = float(readings[l])
                l += 1

# write parameters to txt file
def write_params(nodes):
    with open("params.txt", "w") as doc:
        for i in range(9):
            for j in range(2):
                for k in range(nodes[i][j].outputs):
                    doc.write(str(nodes[i][j].weights[k]) + "\n")
                    doc.write(str(nodes[i][j].biases[k]) + "\n")

# find available moves on a given board
def avail_moves(board):
    output = []
    for i in range(9):
        if board[i] == 0:
            output.append(i)
    return output

# represent each node of the network as an object
class Node:
    outputs = 0
    weights = []
    biases = []
    
    def __init__(self, outputs):
        self.outputs = outputs
        self.weights = [0 for i in range(outputs)]
        self.biases = [0 for i in range(outputs)]
    
    def get_input(self, inputs):
        input = 0
        for i in inputs:
            input += i
        input = 1.0 / (1.0 + math.exp(-1 * input))
        return input
        
    def get_output(self, out_i, input):
        output = input * self.weights[out_i] + self.biases[out_i]
        return output
    
    def node_cost(self, out_i, input, good_output):
        output = self.get_output(out_i, input)
        return (good_output - output)**2

# compute the network outputs from a given board
def find_move(nodes, board):
    outputs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    for i in range(9):
        input = 0
        for j in range(9):
            input += nodes[j][0].get_output(i, board[j])
        input = nodes[i][1].get_input([input])
        outputs[i] = nodes[i][1].get_output(0, input)

    for i in range(9):
        max_index = outputs.index(max(outputs))
        if max_index in avail_moves(board):
            return max_index
        else:
            outputs[max_index] = 0.0

def network_cost(nodes, board, good_move):
    cost = 0

    # output layer cost
    for i in range(9):
        # this assumes 1 is the desired output of the best move & 0 is desired for the rest
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

def main():
    nodes = [[], [], [], [], [], [], [], [], []]

    # this is the only way of initializing the list of node objects that i've found that doesn't link them all together
    nodes[0].append(Node(9))
    nodes[0].append(Node(1))
    nodes[1].append(Node(9))
    nodes[1].append(Node(1))
    nodes[2].append(Node(9))
    nodes[2].append(Node(1))
    nodes[3].append(Node(9))
    nodes[3].append(Node(1))
    nodes[4].append(Node(9))
    nodes[4].append(Node(1))
    nodes[5].append(Node(9))
    nodes[5].append(Node(1))
    nodes[6].append(Node(9))
    nodes[6].append(Node(1))
    nodes[7].append(Node(9))
    nodes[7].append(Node(1))
    nodes[8].append(Node(9))
    nodes[8].append(Node(1))

    # get parameters from text file and correct output layer
    read_params(nodes)
    for i in range(9):
        nodes[i][1].weights = [1]
        nodes[i][1].biases = [0]

    # dataset to train network to (situation-move pairs)
    situations = [[[0, 0, 0, 0, 0, 0, 0, 0, 0], 4]]

    for situation in situations:
        board = situation[0]
        good_move = situation[1]
        cost = network_cost(nodes, board, good_move)
        print(cost)

    write_params(nodes)

main()
