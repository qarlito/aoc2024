#!/usr/local/bin/python
from P13_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT
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


# 3 tokens to push A
# 1 token to push B


import re

INPUT += '\n\n'
lines = INPUT.splitlines()
assert len(lines) % 4 == 0
num_puzzles = len(lines) // 4
puzzles = list()
for puzzle_num in range(num_puzzles):
    line1 = lines[puzzle_num*4]
    line2 = lines[puzzle_num*4+1]
    line3 = lines[puzzle_num*4+2]
    line4 = lines[puzzle_num*4+3]
    m = re.match('Button A: X\\+(\\d+), Y\\+(\\d+)', line1)
    g = m.groups()
    ax, ay = int(g[0]), int(g[1])
    m = re.match('Button B: X\\+(\\d+), Y\\+(\\d+)', line2)
    g = m.groups()
    bx, by = int(g[0]), int(g[1])
    m = re.match('Prize: X=(\\d+), Y=(\\d+)', line3)
    g = m.groups()
    px, py = int(g[0]), int(g[1])
    assert line4 == ''
    puzzles.append((ax, ay, bx, by, px, py))

# a.94 + b.22 = 8400
# a.34 + b.67 = 5400
# Minimize 3.a + b

total = 0
for puzzle in puzzles:
    debug(puzzle, True)
    ax, ay, bx, by, px, py = puzzle
    det = bx * ay - by * ax
    if det == 0:
        raise Exception(f'det == 0 for puzzle {puzzle}')
    else:
        # Calculate rounded-down values and verify if they are exact
        a = (- px * by + py * bx) // det
        b = (px * ay - py * ax) // det
        if (ax*a + bx*b == px and ay*a + by*b == py):
            debug(f'solution a={a} b={b}')
            total += 3*a + b
        else:
            debug('No solution in integers')

print(f'Part 1 - total = {total}')

total = 0
for puzzle in puzzles:
    debug(puzzle, True)
    ax, ay, bx, by, px, py = puzzle
    px += 10000000000000
    py += 10000000000000
    det = bx * ay - by * ax
    if det == 0:
        raise Exception(f'det == 0 for puzzle {puzzle}')
    else:
        # Calculate rounded-down values and verify if they are exact
        a = (- px * by + py * bx) // det
        b = (px * ay - py * ax) // det
        if (ax*a + bx*b == px and ay*a + by*b == py):
            debug(f'solution a={a} b={b}')
            total += 3*a + b
        else:
            debug('No solution in integers')

print(f'Part 2 - total = {total}')
