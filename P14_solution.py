#!/usr/local/bin/python
from P14_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT
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

import re
robots = list() # List of [ (y, x, vy, vx) ]
for line in INPUT.splitlines():
    m = re.match('p=(\\d+),(\\d+) v=(\\-?\\d+),(\\-?\\d+)', line)
    robot = [int(s) for s in m.groups()]
    robots.append(robot)

if DEMO:
    NUMROWS = 7
    NUMCOLS = 11
else:
    NUMROWS = 103
    NUMCOLS = 101
NUMMOVES = 100

# Part 1

counts = [0,0,0,0]
for x, y, vx, vy in robots:
    xx = (x + NUMMOVES*vx) % NUMCOLS
    yy = (y + NUMMOVES*vy) % NUMROWS
    region = None
    if 0 <= xx < NUMCOLS//2:
        region = 0
    elif NUMCOLS//2 + 1 <= xx:
        region = 2
    else:
        region = None
    if region is not None:
        if 0 <= yy < NUMROWS//2:
            pass
        elif NUMROWS//2 + 1 <= yy:
            region += 1
        else:
            region = None
    debug(f'{x},{y} with v {vx},{vy} ends up in {xx},{yy} - region {region}')
    if region is not None:
        counts[region] += 1
mul = counts[0] * counts[1] * counts[2] * counts[3]
print(f'Part 1 - Counts {counts} -> total {mul}')


# Part 2 - assume there are many adjacent robot positions in the display...

import math
MAX_ATTEMPTS = math.lcm(NUMROWS, NUMCOLS)
i = 0
while True:
    if i > MAX_ATTEMPTS:
        print('Finished')
        break
    picture = list()
    for rownum in range(NUMROWS):
        picture.append(['.'] * NUMCOLS)
    for robot in robots:
        picture[robot[1]][robot[0]] = 'X'

    # Check if enough horizontally adjacent X'es
    score = 0
    for line in picture:
        for colnum in range(1, len(line)):
            if line[colnum-1] == 'X' and line[colnum] == 'X':
                score += 1
    if score > 60:
        # If more than 50 adjacent X'es: show picture and let user decide...
        for line in picture:
            print(''.join(line))
        # Wait for input
        input(f'nummoves {i} score {score}:')

    # Move robots
    for robot in robots:
        robot[0] = (robot[0] + robot[2]) % NUMCOLS
        robot[1] = (robot[1] + robot[3]) % NUMROWS
    i += 1
