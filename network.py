import math
from general import *
from readwrite import *

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

# generate network objects and read in parameters
def generate():
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

    return nodes

# computer the network outputs for a given board
def get_outputs(nodes, board):
    outputs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    for i in range(9):
        input = 0
        for j in range(9):
            input += nodes[j][0].get_output(i, board[j])
        input = nodes[i][1].get_input([input])
        outputs[i] = nodes[i][1].get_output(0, input)

    return outputs

# get the network's preferred move for a given board
def find_move(nodes, board):
    outputs = get_outputs(nodes, board)

    for i in range(9):
        max_index = outputs.index(max(outputs))
        if max_index in avail_moves(board):
            return max_index
        else:
            outputs[max_index] = 0.0

