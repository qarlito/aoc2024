#!./venv/bin/python3
from P16_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT
#from Pxx_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT

import sys
if len(sys.argv) > 1 and sys.argv[1].startswith('d'):
    INPUT1 = DEMO_INPUT1.strip()
    INPUT2 = DEMO_INPUT2.strip()
    DEMO = True
else:
    INPUT1 = PRODUCTION_INPUT.strip()
    INPUT2 = INPUT1
    DEMO = False


def debug(s, new_line_before=False, new_line_after=False):
    if DEBUG:
        if new_line_before:
            print()
        print(s)
        if new_line_after:
            print()

DEBUG = DEMO
INPUT = INPUT1

import networkx as nx

# Define direction order as rotation order (we arbitrarily choose clockwise)
UNDEFINED = -1
EAST = 0
SOUTH = 1
WEST = 2
NORTH = 3
DIRECTIONS = {WEST:(0,-1), EAST:(0,1), NORTH:(-1,0), SOUTH:(1,0)}
DIRECTION_NAME = {EAST:'east', SOUTH:'south', WEST:'west', NORTH:'north', UNDEFINED:'-'}

STARTROW = None
STARTCOL = None
ENDROW = None
ENDCOL = None

DATA = INPUT.splitlines()
node_positions = set()
for rownum, row in enumerate(DATA):
    for colnum, c in enumerate(row):
        if c == '#':
            continue
        is_node = False
        if c == '.':
            # Need to be a T or + to be a node, i.e. have at most 1 neighbor #
            neighbors = (row[colnum-1], row[colnum+1], DATA[rownum-1][colnum], DATA[rownum+1][colnum])
            num_bad_neighbors = neighbors.count('#')
            if num_bad_neighbors in (0, 1):
                is_node = True
            # Note that we don't consider a dead end street as a node since these can never be part of a solution
        elif c == 'S':
            is_node = True
            STARTROW, STARTCOL = rownum, colnum
        elif c == 'E':
            is_node = True
            ENDROW, ENDCOL = rownum, colnum
        if is_node:
            node_positions.add((rownum, colnum))

assert STARTROW is not None
assert STARTCOL is not None
assert ENDROW is not None
assert ENDCOL is not None



import networkx as nx
G = nx.DiGraph()  # Directed graph

# Nodes are defined lazily, as endpoints of edges

for rownum, colnum in node_positions:
    for direction in range(4):
        G.add_edge((rownum, colnum, direction), (rownum, colnum, (direction+1)%4), cost=1000, positions=set())
        G.add_edge((rownum, colnum, direction), (rownum, colnum, (direction-1)%4), cost=1000, positions=set())

def move_straight(rownum, colnum, direction):
    newdirection = direction
    newrownum = rownum + DIRECTIONS[newdirection][0]
    newcolnum = colnum + DIRECTIONS[newdirection][1]
    if DATA[newrownum][newcolnum] != '#':
        return newrownum, newcolnum, newdirection, 1
    else:
        return None

def move_right(rownum, colnum, direction):
    newdirection = (direction + 1) % 4
    newrownum = rownum + DIRECTIONS[newdirection][0]
    newcolnum = colnum + DIRECTIONS[newdirection][1]
    if DATA[newrownum][newcolnum] != '#':
        return newrownum, newcolnum, newdirection, 1001
    else:
        return None

def move_left(rownum, colnum, direction):
    newdirection = (direction - 1) % 4
    newrownum = rownum + DIRECTIONS[newdirection][0]
    newcolnum = colnum + DIRECTIONS[newdirection][1]
    if DATA[newrownum][newcolnum] != '#':
        return newrownum, newcolnum, newdirection, 1001
    else:
        return None

debug(INPUT)

# Calculate cost of edge, and set of positions (including endpoints) on edge
for src_rownum, src_colnum, src_direction in G.nodes:
    debug(f'Starting path at {(src_rownum, src_colnum, DIRECTION_NAME[src_direction])}')
    total_cost = 0
    dead_end = False

    positions = set()
    positions.add((src_rownum, src_colnum))

    # First move must be a straight move
    result = move_straight(src_rownum, src_colnum, src_direction)
    if result is None:
        debug(f'  Cannot make first move.')
        continue
    rownum, colnum, direction, cost = result
    total_cost += cost
    positions.add((rownum, colnum))

    while (rownum, colnum) not in node_positions:
        result = move_straight(rownum, colnum, direction)
        if result is None:
            result = move_right(rownum, colnum, direction)
            if result is None:
                result = move_left(rownum, colnum, direction)
        if result is None:
            # We are in a dead end. Abort this path since there are always ways to avoid dead ends.
            dead_end = True
            break
        rownum, colnum, direction, cost = result
        total_cost += cost
        positions.add((rownum, colnum))
  
    if dead_end:
        debug(f'  Dead end at {(rownum, colnum, DIRECTION_NAME[direction])}')
        continue

    debug(f'  Found an edge from {(src_rownum, src_colnum, DIRECTION_NAME[src_direction])} -> {(rownum, colnum, DIRECTION_NAME[direction])} of cost {total_cost} and length {len(positions)}')
    G.add_edge((src_rownum, src_colnum, src_direction), (rownum, colnum, direction), cost=total_cost, positions=positions)

# Add additional nodes for the start and end point. They do not add cost or positions, but unify the logical start node, and logical end nodes
START = 'START', None, UNDEFINED
G.add_edge(START, (STARTROW, STARTCOL, EAST), cost=0, positions=set())
END = 'END', None, UNDEFINED
for direction in (NORTH, EAST, SOUTH, WEST):
    G.add_edge((ENDROW, ENDCOL, direction), END, cost=0, positions=set())

shortest_path_cost = nx.shortest_path_length(G, source=START, target=END, weight='cost')
print(f'\nPart 1 - shortest path cost = {shortest_path_cost}\n')

#l = nx.shortest_path_length(G, source=None, target=END, weight='cost')
#last_nodes = set([START])
#visited_positions = set()
#while len(last_nodes) > 0:
#    debug(f'Extending from: {[(rownum, colnum, DIRECTION_NAME[direction]) for (rownum, colnum, direction) in last_nodes]}')
#    new_last_nodes = set()
#    for last_node in last_nodes:
#        for neighbor in G.neighbors(last_node):
#            edge = G.edges[last_node, neighbor]
#            if edge['cost'] + l[neighbor] == l[last_node]:
#                new_last_nodes.add(neighbor)
#                visited_positions.update(edge['positions'])
#    last_nodes = new_last_nodes
#
#print(f'\nPart 2 - Number of positions on shortest paths = {len(visited_positions)}')

shortest_paths = nx.all_shortest_paths(G, source=START, target=END, weight='cost')
nodes = set()
for path in shortest_paths:
    for i in range(len(path)-1):
        edge = G.edges[path[i], path[i+1]]
        nodes.update(edge['positions'])
print(f'\nPart 2 - Number of positions on shortest paths = {len(nodes)}')
