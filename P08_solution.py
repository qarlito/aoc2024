#!/usr/local/bin/python
from P08_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT

import sys
if len(sys.argv) > 1 and sys.argv[1].startswith('d'):
    INPUT1 = DEMO_INPUT1.strip()
    INPUT2 = DEMO_INPUT2.strip()
else:
    INPUT1 = PRODUCTION_INPUT.strip()
    INPUT2 = INPUT1


from collections import defaultdict

INPUT = INPUT1

data = INPUT.splitlines()
size = len(data)
assert size == len(data[0])
antennas = defaultdict(lambda: list())
for rownum, line in enumerate(data):
    for colnum, c in enumerate(line.strip()):
        if c != '.':
            antennas[c].append((rownum, colnum))

def is_legal(position, size):
    return 0 <= position[0] < size and 0 <= position[1] < size

def try_jump(position1, position2, jump, size):
    candidate_antinode = (position1[0] + jump * (position2[0]-position1[0]),
                          position1[1] + jump * (position2[1]-position1[1]))
    if is_legal(candidate_antinode, size):
        return candidate_antinode
    else:
        return None



# Part 1

# A + (-1) * (B-A) = next to A
# A +   0  * (B-A) = A
# A +   1  * (B-A) = B
# A +   2  * (B-A) = next to B

antinodes = set()
for _, positions in antennas.items():
    for i in range(len(positions)-1):
        first = positions[i]
        for j in range(i+1, len(positions)):
            second = positions[j]
            for jump in [-1, 2]:
                candidate_antinode = try_jump(positions[i], positions[j], jump, size)
                if candidate_antinode is not None:
                    antinodes.add(candidate_antinode)

print(f'Part 1 - {len(antinodes)}')



# Part 2

antinodes = set()
for _, positions in antennas.items():
    for i in range(len(positions)-1):
        first = positions[i]
        for j in range(i+1, len(positions)):
            second = positions[j]

            # Try 0, 1, 2, ...
            jump = 0
            while True:
                candidate_antinode = try_jump(positions[i], positions[j], jump, size)
                if candidate_antinode is None:
                    # We went off-grid
                    break
                antinodes.add(candidate_antinode)
                jump += 1

            # Try -1, -2, ...
            jump = -1
            while True:
                candidate_antinode = try_jump(positions[i], positions[j], jump, size)
                if candidate_antinode is None:
                    # We went off-grid
                    break
                antinodes.add(candidate_antinode)
                jump -= 1

print(f'Part 2 - {len(antinodes)}')
