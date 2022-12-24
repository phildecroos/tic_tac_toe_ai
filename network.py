import math
import random
from general import *
from readwrite import *

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
    nodes = [[] for i in range(18)]

    # this is the only way of initializing the list of node objects that i've 
    # found that doesn't link them to the same object in memory
    nodes[0].append(Node(9))
    nodes[1].append(Node(9))
    nodes[2].append(Node(9))
    nodes[3].append(Node(9))
    nodes[4].append(Node(9))
    nodes[5].append(Node(9))
    nodes[6].append(Node(9))
    nodes[7].append(Node(9))
    nodes[8].append(Node(9))
    nodes[9].append(Node(9))
    nodes[10].append(Node(9))
    nodes[11].append(Node(9))
    nodes[12].append(Node(9))
    nodes[13].append(Node(9))
    nodes[14].append(Node(9))
    nodes[15].append(Node(9))
    nodes[16].append(Node(9))
    nodes[17].append(Node(9))

    nodes[0].append(Node(9))
    nodes[1].append(Node(9))
    nodes[2].append(Node(9))
    nodes[3].append(Node(9))
    nodes[4].append(Node(9))
    nodes[5].append(Node(9))
    nodes[6].append(Node(9))
    nodes[7].append(Node(9))
    nodes[8].append(Node(9))
    
    nodes[0].append(Node(1))
    nodes[1].append(Node(1))
    nodes[2].append(Node(1))
    nodes[3].append(Node(1))
    nodes[4].append(Node(1))
    nodes[5].append(Node(1))
    nodes[6].append(Node(1))
    nodes[7].append(Node(1))
    nodes[8].append(Node(1))
    
    return nodes

def print_network(nodes):
    for i in range(len(nodes)):
        print("row: " + str(i))
        for j in range(len(nodes[i])):
            print(nodes[i][j].weights)

# computer the network outputs for a given board
def get_outputs(nodes, board):
    # a different board representation is needed here, but the old one is still
    # used everywhere else
    local_board = [0 for i in range(18)]
    for i in range(9):
        if board[i] == 1:
            local_board[i] = 1
        elif board[i] == -1:
            local_board[i + 9] = 1

    outputs = [0 for i in range(9)]
    
    for i in range(9):
        inputs2 = [0 for i in range(9)]
        for j in range(9):
            inputs1 = [0 for i in range(18)]
            for k in range(18):
                # input layer
                inputs1[k] = nodes[k][0].get_output(j, local_board[k])
            # hidden layer
            input1 = nodes[j][1].get_input(inputs1)
            inputs2[j] += nodes[j][1].get_output(i, input1)
        # output layer
        input2 = nodes[i][2].get_input(inputs2)
        outputs[i] = nodes[i][2].get_output(0, input2)
    
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
