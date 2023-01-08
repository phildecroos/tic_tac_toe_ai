import math
from general import *
from readwrite import *

hidden_nodes = 12

# represent each node of the network as an object
class Node:
    outputs = 0
    weights = []
    
    def __init__(self, outputs):
        self.outputs = outputs
        self.weights = [0 for i in range(outputs)]
    
    def get_input(self, inputs):
        return 1.0 / (1.0 + math.exp(round(-1 * sum(inputs), 5)))
        
    def get_output(self, out_i, input):
        return input * self.weights[out_i]

# generate network objects and read in parameters
def generate():
    nodes = [[] for i in range(27)]

    # input layer
    for i in range(27):
        nodes[i].append(Node(hidden_nodes))
    
    # hidden layers
    for i in range(hidden_nodes):
        nodes[i].append(Node(9))
    
    # output layer
    for i in range(9):
        nodes[i].append(Node(1))

    return nodes

def print_network(nodes):
    for i in range(len(nodes)):
        print("row: " + str(i))
        for j in range(len(nodes[i])):
            print(nodes[i][j].weights)

# computer the network outputs for a given board
def get_outputs(nodes, board):
    # a different board representation is needed here, but the old one is still used everywhere else
    local_board = [0 for i in range(27)]
    for i in range(9):
        if board[i] == 1:
            local_board[i] = 1
        elif board[i] == -1:
            local_board[i + 9] = 1
        elif board[i] == 0:
            local_board[i + 18] = 1

    outputs = [0 for i in range(9)]
    for i in range(9):
        inputs2 = [0 for i in range(hidden_nodes)]
        for j in range(hidden_nodes):
            inputs1 = [0 for i in range(27)]
            for k in range(27):
                # get input layer node output from board input
                inputs1[k] = nodes[k][0].get_output(j, local_board[k])
            # get hidden layer node output
            input1 = nodes[j][1].get_input(inputs1)
            inputs2[j] += nodes[j][1].get_output(i, input1)
        # get output layer node output
        input2 = nodes[i][len(nodes[i]) - 1].get_input(inputs2)
        outputs[i] = nodes[i][len(nodes[i]) - 1].get_output(0, input2)

    return outputs

# get the network's preferred move for a given board
def find_move(nodes, board):
    outputs = get_outputs(nodes, board)

    for i in range(9):
        max_index = outputs.index(max(outputs))
        if max_index in avail_moves(board):
            return max_index
        else:
            outputs[max_index] = -1.0
