#!./venv/bin/python3
from P20_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT
#from Pxx_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT

import sys
if len(sys.argv) > 1 and sys.argv[1].startswith('d'):
    INPUT1 = DEMO_INPUT1.strip()
    INPUT2 = DEMO_INPUT2.strip()
    DEMO = True
    DELTA1 = 1
    DELTA2 = 50
else:
    INPUT1 = PRODUCTION_INPUT.strip()
    INPUT2 = INPUT1
    DEMO = False
    DELTA1 = 100
    DELTA2 = 100


def debug(s, new_line_before=False, new_line_after=False):
    if DEBUG:
        if new_line_before:
            print()
        print(s)
        if new_line_after:
            print()

DEBUG = DEMO
INPUT = INPUT1

from collections import defaultdict
import networkx as nx

G = nx.Graph()

STARTROW = None
STARTCOL = None
ENDROW = None
ENDCOL = None

DATA = INPUT.splitlines()
NUMROWS = len(DATA)
NUMCOLS = len(DATA[0])
walls = set()
for rownum, row in enumerate(DATA):
    assert len(row) == NUMCOLS
    for colnum, c in enumerate(row):
        if c == '#':
            if rownum > 0 and colnum > 0 and rownum < NUMROWS-1 and colnum < NUMCOLS-1:
                walls.add((rownum, colnum))
            continue
        if c == 'S':
            assert STARTROW is None
            assert STARTCOL is None
            STARTROW, STARTCOL = rownum, colnum
        if c == 'E':
            assert ENDROW is None
            assert ENDROW is None
            ENDROW, ENDCOL = rownum, colnum
        if DATA[rownum][colnum+1] != '#':
            G.add_edge((rownum,colnum), (rownum,colnum+1))
        if DATA[rownum+1][colnum] != '#':
            G.add_edge((rownum,colnum), (rownum+1,colnum))

assert STARTROW is not None
assert STARTCOL is not None
assert ENDROW is not None
assert ENDCOL is not None

START = (STARTROW, STARTCOL)
END = (ENDROW, ENDCOL)

# Calculate distances from start to every node, and from every node to end
from_start = nx.shortest_path_length(G, source=START)
to_end = nx.shortest_path_length(G, target=END)

# Algorithm:
#
#   Calculate cheat at any cell '.', 'S', 'E'
#   Allow teleporting to any other cell within distance 2 (for part 1) and 20 (for part 2) or less (= Manhattan distance)
#   This gives a path start -> self -> teleported location -> end
#   Cost is always Manhatten distance of teleportation

# Generate a function which returns all cells within Manhattan distance of at most max_radius
def generate_get_neighbors(max_radius):
    def get_neighbors(rownum, colnum):
        neighbors = set()
        for rowdelta in range(-max_radius, max_radius+1):
            max_coldelta = max_radius - abs(rowdelta)
            for coldelta in range(-max_coldelta, max_coldelta+1):
                nrow = rownum + rowdelta
                ncol = colnum + coldelta
                if 0 < nrow < NUMROWS-1 and 0 < ncol < NUMCOLS -1:
                    neighbors.add((nrow, ncol))
        return neighbors
    return get_neighbors

def calculate_solution(baseline, goal, teleportation_cost, get_neighbors):
    solutions = defaultdict(lambda: 0)
    for rownum, colnum in G.nodes:
        start_to_self = from_start.get((rownum, colnum), -1)
        if start_to_self == -1:
            continue
        neighbors = get_neighbors(rownum, colnum)
        cheapest_path_cost = goal + 1  # Any value larger than goal will do
        for nrow, ncol in neighbors:
            neighbor_to_end = to_end.get((nrow, ncol), -1)
            if neighbor_to_end == -1:
                continue
            cost = start_to_self + abs(nrow-rownum) + abs(ncol-colnum) + neighbor_to_end
            if cost <= goal:
                solutions[baseline-cost] += 1
    return solutions

baseline = from_start[END]

goal = baseline - DELTA1
teleportation_cost = 2
solution_counters = calculate_solution(baseline, goal, teleportation_cost, generate_get_neighbors(teleportation_cost))
total = sum(solution_counters.values())
for savings, count in sorted(solution_counters.items()):
    debug(f'    There are {count} cheats that save {savings} picoseconds.')
print(f'Part 1 - baseline {baseline} goal {goal} saving at least {DELTA1}; teleportation_cost {teleportation_cost} - {total} solutions\n')

goal = baseline - DELTA2
teleportation_cost = 20
solution_counters = calculate_solution(baseline, goal, teleportation_cost, generate_get_neighbors(teleportation_cost))
total = sum(solution_counters.values())
for savings, count in sorted(solution_counters.items()):
    debug(f'    There are {count} cheats that save {savings} picoseconds.')
print(f'Part 2 - baseline {baseline} goal {goal} saving at least {DELTA2}; teleportation_cost {teleportation_cost} - {total} solutions')
