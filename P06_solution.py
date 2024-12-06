#!/usr/local/bin/python
from P06_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT
#from Pxx_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT

import sys
if len(sys.argv) > 1 and sys.argv[1].startswith('d'):
    INPUT1 = DEMO_INPUT1.strip()
    INPUT2 = DEMO_INPUT2.strip()
else:
    INPUT1 = PRODUCTION_INPUT.strip()
    INPUT2 = INPUT1


# Part 1

INPUT = INPUT1
DATA = INPUT.splitlines()
NUM_ROWS = len(DATA)
NUM_COLS = len(DATA[0])
GUARD_POS = None
GUARD_DIRECTION = None
for row, rowdata in enumerate(DATA):
    guard_col = rowdata.find('^')
    if guard_col != -1:
        GUARD_POS = (row, guard_col)
        GUARD_DIRECTION = (-1,0)
        break

assert GUARD_POS is not None


# Part 1

def replace_at_offset(d, row, col, c):
    d[row] = d[row][:col] + c + d[row][col+1:]

data = DATA.copy()
guard_pos = GUARD_POS
guard_direction = GUARD_DIRECTION

GRAPHICAL = False

def walk(data, guard_pos, guard_direction):
    already_visited = set()
    while True:
        if GRAPHICAL:
            print('\n'.join(data))
            input()
        newpos = (guard_pos[0] + guard_direction[0], guard_pos[1] + guard_direction[1])
        replace_at_offset(data, guard_pos[0], guard_pos[1], 'X')
        if newpos[0]<0 or newpos[0]>=NUM_ROWS or newpos[1]<0 or newpos[1]>=NUM_COLS:
            if GRAPHICAL:
                print('\n'.join(data))
            break
        if data[newpos[0]][newpos[1]] == '#':
            # Change direction
            guard_direction = {(-1,0):(0,1), (0,1):(1,0), (1,0):(0,-1), (0,-1):(-1,0)}[guard_direction]
            if GRAPHICAL:
                replace_at_offset(data, guard_pos[0], guard_pos[1], {(-1,0):'^', (0,1):'>', (1,0):'v', (0,-1):'<'}[guard_direction])
            continue
        guard_pos = newpos
        if GRAPHICAL:
            replace_at_offset(data, guard_pos[0], guard_pos[1], {(-1,0):'^', (0,1):'>', (1,0):'v', (0,-1):'<'}[guard_direction])
        if (*guard_pos, *guard_direction) in already_visited:
            return False
        already_visited.add((*guard_pos, *guard_direction))
    return True

exited = walk(data, guard_pos, guard_direction)
assert exited is True
num_visited = ''.join(data).count('X')
print(f'Part 1 - visited {num_visited} cells.\n')


# Part 2

num_loops = 0
for obst_row in range(NUM_ROWS):
    print(f'Part 2 - Testing obstacles on row {obst_row} of {NUM_ROWS}')
    for obst_col in range(NUM_COLS):
        data = DATA.copy()
        if GUARD_POS == (obst_row, obst_col):
            continue
        if data[obst_row][obst_col] == '#':
            continue
        replace_at_offset(data, obst_row, obst_col, '#')
        # Now walk around and try to detect a loop vs an exit
        exited = walk(data, GUARD_POS, GUARD_DIRECTION)
        if not exited:
            num_loops += 1
            continue

print(f'\nPart 2 - Found {num_loops} obstacle positions causing a loop.')
