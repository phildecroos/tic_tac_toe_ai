# read parameters from file
def read_params(nodes, file):
    readings = []

    with open(file, "r") as doc:
        for line in doc:
            readings.append(line[0:-1])

    l = 0
    for i in range(len(nodes)):
        for j in range(len(nodes[0])):
            for k in range(nodes[i][j].outputs):
                nodes[i][j].weights[k] = float(readings[l])
                l += 1
                nodes[i][j].biases[k] = float(readings[l])
                l += 1

# write parameters to file
def write_params(nodes, file):
    with open(file, "w") as doc:
        for i in range(len(nodes)):
            for j in range(len(nodes[0])):
                for k in range(nodes[i][j].outputs):
                    doc.write(str(nodes[i][j].weights[k]) + "\n")
                    doc.write(str(nodes[i][j].biases[k]) + "\n")

# read situations from file
def read_situations(file):
    situations = []
    with open(file, "r") as doc:
        count = 0
        for line in doc:
            situations.append([["0", "0", "0", "0", "0", "0", "0", "0", "0"], 0])
            i = 0
            for j in range(9):
                if line[i] == "-":
                    i += 1
                    situations[count][0][j] = -1 * int(line[i])
                else:
                    situations[count][0][j] = int(line[i])
                i += 1
            situations[count][1] = int(line[i])
            count += 1
    return situations

# write situations to file
def write_situations(situations, file):
    with open(file, "w") as doc:
        for situation in situations:
            doc.write(situation + "\n")