#!./venv/bin/python3
from P25_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT
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

locks = list()
keys = list()

lines = (INPUT.strip() + '\n\n').splitlines()
assert len(lines) % 8 == 0
num_entries = len(lines) // 8

for i in range(num_entries):
    assert lines[i*8 + 7] == ''
    if lines[i*8] == '#####':
        assert lines[i*8 + 6] == '.....'
        heights = [5,5,5,5,5]
        for y in range(5):
            for x in range(5):
                if lines[i*8 + 1 + y][x] == '.':
                    heights[x] = min(heights[x], y)
        locks.append(heights)
    elif lines[i*8] == '.....':
        assert lines[i*8 + 6] == '#####'
        heights = [0,0,0,0,0]
        for y in range(5):
            for x in range(5):
                if lines[i*8 + 1 + y][x] == '#':
                    heights[x] = max(heights[x], 5-y)
        keys.append(heights)
    else:
        raise Exception(f'Entry {i} is faulty')


debug('locks = ' + str(locks))
debug('keys  = ' + str(keys))
total = 0
for lock in locks:
    for key in keys:
        fits = True
        for i in range(5):
            if lock[i] + key[i] > 5:
                fits = False
        if fits:
            debug(f'key {key} fits in lock {lock}')
            total += 1

print(f'Part 1 - total {total}')
