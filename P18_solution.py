#!./venv/bin/python3
from P18_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT
#from Pxx_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT

import sys
if len(sys.argv) > 1 and sys.argv[1].startswith('d'):
    INPUT1 = DEMO_INPUT1.strip()
    INPUT2 = DEMO_INPUT2.strip()
    DEMO = True
    SIZE = 7
    NUM_ENTRIES = 12
else:
    INPUT1 = PRODUCTION_INPUT.strip()
    INPUT2 = INPUT1
    DEMO = False
    SIZE = 71
    NUM_ENTRIES = 1024


def debug(s, new_line_before=False, new_line_after=False):
    if DEBUG:
        if new_line_before:
            print()
        print(s)
        if new_line_after:
            print()

DEBUG = DEMO
INPUT = INPUT1

WALLS = list()
for line in INPUT.splitlines():
    colstr, rowstr = line.split(',')
    colnum = int(colstr)
    rownum = int(rowstr)
    WALLS.append((rownum, colnum))

data = [['.'] * SIZE for _ in range(SIZE)]
for rownum, colnum in WALLS[:NUM_ENTRIES]:
    data[rownum][colnum] = '#'

import networkx as nx
G = nx.Graph()
for rownum, row in enumerate(data):
    for colnum, c in enumerate(row):
        if data[rownum][colnum] == '#':
            continue
        # This is a non-directed graph. Only extend to east + south. No need for west + north.
        if colnum<SIZE-1 and data[rownum][colnum+1] == '.':
            G.add_edge((rownum,colnum), (rownum,colnum+1))
        if rownum<SIZE-1 and data[rownum+1][colnum] == '.':
            G.add_edge((rownum,colnum), (rownum+1,colnum))

START = (0, 0)
END = (SIZE-1, SIZE-1)

length = nx.shortest_path_length(G, source=START, target=END)
print(f'Part 1 - Shortest path length is {length}')

# Now gradually add walls until it breaks
wall_num = NUM_ENTRIES
while True:
    wall = WALLS[wall_num]
    debug(f'gonna remove {wall[1],wall[0]}')
    if G.has_node(wall):
        # If a node has no neighbours, it has no edges, hence it doesn't exist in the graph.
        # G.remove_node would give an error. That's why we first check if G.has_node
        G.remove_node(wall)
    if not nx.has_path(G, source=START, target=END):
        print(f'Part 2 - It breaks at wall {wall[1]},{wall[0]}')
        break
    wall_num += 1
