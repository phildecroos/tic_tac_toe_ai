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
    nodes = [[] for i in range(9)]

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
    
    nodes[0].append(Node(9))
    nodes[1].append(Node(9))
    nodes[2].append(Node(9))
    nodes[3].append(Node(9))
    nodes[4].append(Node(9))
    nodes[5].append(Node(9))
    nodes[6].append(Node(9))
    nodes[7].append(Node(9))
    nodes[8].append(Node(9))

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

# computer the network outputs for a given board
def get_outputs(nodes, board):
    outputs = [0 for i in range(9)]
    
    for i in range(9):
        inputs3 = [0 for i in range(9)]
        for j in range(9):
            inputs2 = [0 for i in range(9)]
            for k in range(9):
                inputs1 = [0 for i in range(9)]
                for l in range(9):
                    # input layer
                    inputs1[k] = nodes[k][0].get_output(j, board[k])
                # hidden layer
                input1 = nodes[j][1].get_input(inputs1)
                inputs2[j] += nodes[j][1].get_output(i, input1)
            # hidden layer
            input2 = nodes[j][1].get_input(inputs2)
            inputs3[j] += nodes[j][2].get_output(i, input2)
        # output layer
        input3 = nodes[i][2].get_input(inputs3)
        outputs[i] = nodes[i][3].get_output(0, input3)
    
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




# def rand_params(nodes):
#     for i in range(len(nodes)):
#         for j in range(len(nodes[0]) - 1):
#             for k in range(nodes[i][j].outputs):
#                 nodes[i][j].weights[k] = random.random() + random.randint(-1, 1)

# nodes = generate()
# for i in range(9):
#     nodes[i][len(nodes[0]) - 1].weights[0] = 1.0
# situations = read_situations("situations.txt")

# gradient = []
# for i in range(len(nodes)):
#     gradient.append([])
#     for j in range(len(nodes[0]) - 1):
#         gradient[i].append([])
#         for k in range(nodes[i][j].outputs):
#             gradient[i][j].append(1)

# rand_params(nodes)

# board = [0,0,0,0,0,0,0,0,0]

# print("\nboard" + str(board))
# print("network outputs: " + str(get_outputs(nodes, board)))
# print("chosen move: " + str(find_move(nodes, board)))