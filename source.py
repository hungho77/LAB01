import math
import heapq


# command line

import sys

file_input_name = str(sys.argv[1])
file_output_name = str(sys.argv[2])


# class PriorityQueue


class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, item, priority):
        pair = (priority, item)
        heapq.heappush(self.heap, pair)

    def pop(self):
        return heapq.heappop(self.heap)

    def is_empty(self):
        return len(self.heap) == 0

    def clear(self):
        while not (self.is_empty()):
            self.heap.pop()

    def get_heap(self):
        return self.heap

    def get_len(self):
        return len(self.heap)

    def exists(self, item):
        return item in (x[1] for x in self.heap)

    def update_priority(self, item, new_priority):
        for index in range(0, self.get_len()):
            if self.heap[index][1] == item:
                self.heap[index] = (new_priority, item)
        heapq.heapify(self.heap)


# read file input


file_input = open(file_input_name, "r")
N = int(file_input.readline())
Sx = int(file_input.read(2))
Sy = int(file_input.read(2))
Gx = int(file_input.read(2))
Gy = int(file_input.read(2))
arr2D_state = []
for line in file_input:
    new = []
    for char in line.rstrip("\n").replace(" ", ""):
        new.append(int(char))
    arr2D_state.append(new)
file_input.close()

# end of read file input


# function heuristic


def h(x, y):
    return math.sqrt(abs((x*x - Gx*Gx)) + abs((y*y - Gy*Gy)))


# variable


PQ = PriorityQueue()
dict_back = {(Sx, Sy): -1}
dict_g = {(Sx, Sy): 0}
f1 = dict_g[(Sx, Sy)] + h(Sx, Sy)
dict_f = {(Sx, Sy): f1}
list_vicinity = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]  # order expand


# push S into PQ
PQ.push((Sx, Sy), f1)

# loop


while True:
    if not PQ:
        break
    else:
        n = PQ.pop()[0]
        node = list(dict_f.keys())[list(dict_f.values()).index(n)]
        Nx = node[0]
        Ny = node[1]
        if h(Nx, Ny) == 0:
            break
        else:
            # open n
            arr2D_state[Nx][Ny] = -1
            # expand()
            for d in list_vicinity:
                N1x = Nx + d[0]  # n'x
                N1y = Ny + d[1]  # n'y
                if N1x < 0 or N1y < 0 or N1x >= N or N1y >= N or arr2D_state[N1x][N1y] == 1:
                    continue
                cost = 1
                g1 = dict_g[(Nx, Ny)] + cost
                dict_g.update({(N1x, N1y): g1})
                f1 = g1 + h(N1x, N1y)
                if arr2D_state[N1x][N1y] == 0 and not PQ.exists((N1x, N1y)):
                    PQ.push((N1x, N1y), f1)
                    dict_back.update({(N1x, N1y): (Nx, Ny)})
                    dict_f.update({(N1x, N1y): f1})
                elif (arr2D_state == -1 and f1 < dict_f[(N1x, N1y)]) \
                        or (f1 < dict_f[(N1x, N1y)] and PQ.exists((N1x, N1y))):
                    PQ.push((N1x, N1y), f1)
                    dict_back[(N1x, N1y)] = (Nx, Ny)
                    dict_f[(N1x, N1y)] = f1

# Write into file

file_output = open(file_output_name, "w")
m = Gx
n = Gy
K = 1 + (int(dict_f[(Gx, Gy)]))  # the number of min step
file_output.write(str(K) + '\n')
file_output.write('(%d, %d) ' % (m, n))
while dict_back[(m, n)] != -1:
    file_output.write(str(dict_back[(m, n)]) + ' ')
    arr2D_state[m][n] = 'x'
    (m, n) = dict_back[(m, n)]
file_output.write('\n')
for i in range(N):
    for j in range(N):
        if i == Sx and j == Sy:
            file_output.write('S ')
        elif i == Gx and j == Gy:
            file_output.write('G ')
        elif arr2D_state[i][j] == 1:
            file_output.write('o ')
        elif arr2D_state[i][j] == 'x':
            file_output.write(str(arr2D_state[i][j]) + ' ')
        else:
            file_output.write('- ')
    file_output.write('\n')
