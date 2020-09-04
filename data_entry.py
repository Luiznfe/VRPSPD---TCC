from client import Client

def data_read(path):

    data = list()
    f = open(path, "r")
    if f.mode == 'r':
        data = f.readlines()
    f.close()
    cap = float(data[0])
    n = b = int(data[1]) + 1
    linha = list()
    adjMatrix = list()
    del data[0]
    del data[0]

    for i in range(0, n):
        for j in range(0, b):
            linha.append(float(data[j]))
        adjMatrix.append(linha[:])
        linha.clear()
        for j in range(0, b):
            data.pop(0)

    clientList = []
    i = 1
    for k in range(0, len(data), 2):
        c = Client(i, float(data[k]), float(data[k + 1]))
        clientList.append(c)
        i += 1

    return cap, adjMatrix, clientList

# CHAMADA DA FUNÇÃO


if __name__ == '__main__':
    data_read()
