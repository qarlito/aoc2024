#!/usr/local/bin/python
from P10_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT
#from Pxx_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT

import sys
if len(sys.argv) > 1 and sys.argv[1].startswith('d'):
    INPUT1 = DEMO_INPUT1.strip()
    INPUT2 = DEMO_INPUT2.strip()
    DEBUG = True
else:
    INPUT1 = PRODUCTION_INPUT.strip()
    INPUT2 = INPUT1
    DEBUG = False


def debug(s, new_line_before=False, new_line_after=False):
    if DEBUG:
        if new_line_before:
            print()
        print(s)
        if new_line_after:
            print()


INPUT = INPUT1

data = list()
for line in INPUT.splitlines():
    data.append([int(i) if i!='.' else -1 for i in line])

assert len(data) == len(data[0])
size = len(data)

trailheads = list()
for rownum, row in enumerate(data):
    for colnum, value in enumerate(row):
        if value == 0:
            trailheads.append((rownum, colnum))

def find_neighbours(data, size, position, height):
    # Find positions which are a neighbour of `position` and have height `height`
    rownum, colnum = position
    result = set()
    if rownum > 0 and data[rownum-1][colnum] == height:
        result.add((rownum-1, colnum))
    if colnum > 0 and data[rownum][colnum-1] == height:
        result.add((rownum, colnum-1))
    if rownum < size-1 and data[rownum+1][colnum] == height:
        result.add((rownum+1, colnum))
    if colnum < size-1 and data[rownum][colnum+1] == height:
        result.add((rownum, colnum+1))
    return result


# Part 1

total = 0
for trailhead in trailheads:
    heads = {trailhead}
    height = 0
    while height < 9:
        # Find all adjacent positions from a head to the next height
        height += 1
        new_heads = set()
        for head in heads:
            new_heads.update(find_neighbours(data, size, head, height))
        heads = new_heads
    debug(f'For trailhead {trailhead} I found heads {heads}')
    total += len(heads)

print(f'Part 1 - total = {total}\n')


# Part 2

from collections import defaultdict

total = 0
heads = dict(zip(trailheads, [1]*len(trailheads)))   # Scores for each head or reachable position of a certain height
height = 0
while height < 9:
    height += 1
    new_heads = defaultdict(lambda: 0)
    for head, head_score in heads.items():
        reachable_new_heads = find_neighbours(data, size, head, height)
        for reachable_new_head in reachable_new_heads:
            new_heads[reachable_new_head] += head_score
    heads = new_heads
score = sum(heads.values())
debug(f'For trailhead {trailhead} I found heads {score}')
total += score

print(f'Part 2 - total score = {total}')
