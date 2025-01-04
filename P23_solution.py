#!./venv/bin/python3
from P23_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT
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

from collections import defaultdict

import networkx as nx

G = nx.Graph()
for line in INPUT.splitlines():
    assert len(line) == 5
    left, right = line.split('-')
    G.add_edge(left, right)

cliques = [c for c in nx.algorithms.enumerate_all_cliques(G) if len(c)==3 and any([n.startswith('t') for n in c])]
print('Part 1:', len(cliques))

for clique in nx.algorithms.enumerate_all_cliques(G):
    pass
print('Part 2:', ','.join(sorted(clique)))
