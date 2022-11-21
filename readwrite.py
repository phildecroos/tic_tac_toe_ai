# read parameters from txt file
def read_params(nodes, file):
    readings = []

    with open(file, "r") as doc:
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
def write_params(nodes, file):
    with open(file, "w") as doc:
        for i in range(9):
            for j in range(2):
                for k in range(nodes[i][j].outputs):
                    doc.write(str(nodes[i][j].weights[k]) + "\n")
                    doc.write(str(nodes[i][j].biases[k]) + "\n")