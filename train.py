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

    def calculate(self, out_i, inputs):
        output = 0
        for i in inputs:
            output += i * self.weights[out_i] + self.biases[out_i]
        output = 1.0 / (1.0 + math.exp(-1 * output))
        return output
    
    def node_cost(self, out_i, inputs, good_output):
        output = self.calculate(out_i, inputs)
        return (good_output - output)**2

# compute the network outputs from a given board
def find_move(nodes, board):
    outputs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    for i in range(9):
        inputs = []
        for j in range(9):
            inputs.append(nodes[j][0].calculate(i, [board[j]]))
        outputs[i] = nodes[i][1].calculate(0, inputs)

    for i in range(9):
        max_index = outputs.index(max(outputs))
        if max_index in avail_moves(board):
            return max_index
        else:
            outputs[max_index] = -1.0

def network_cost(nodes, board, good_move):
    total_cost = 0
    good_output = 0
    inputs = [[], [], [], [], [], [], [], [], []]

    # output layer cost
    for i in range(9):
        # this assumes 1 is the desired output of the best move & 0 is desired for the rest
        if i == good_move:
            good_output = 1
        else:
            good_output = 0
        for j in range(9):
            inputs[i].append(nodes[j][0].calculate(i, [board[j]]))
        total_cost += nodes[i][1].node_cost(0, inputs[i], good_output)

    return total_cost

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

    read_params(nodes)

    # dataset to train network to (situation-move pairs)
    situations = [[[0, 0, 0, 0, 0, 0, 0, 0, 0], 4]]

    for situation in situations:
        board = situation[0]
        good_move = situation[1]
        cost = network_cost(nodes, board, good_move)
        print(cost)

    write_params(nodes)

main()
