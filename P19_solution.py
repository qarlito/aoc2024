#!./venv/bin/python3
from P19_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT
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


lines = INPUT.splitlines()
PATTERNS = lines[0].split(', ')
DESIGNS = lines[2:]

def count_possibilities(design, offset, counters):
    if offset in counters:
        return counters[offset]
    result = 0
    for pattern in PATTERNS:
        if design.startswith(pattern, offset):
            result += count_possibilities(design, offset + len(pattern), counters)
    counters[offset] = result
    return result

from collections import defaultdict
total_part1 = 0
total_part2 = 0
for design in DESIGNS:
    debug(f'Trying design {design}')

    # counters[offset] represents the number of ways we can construct design[offset:]
    counters = defaultdict(lambda: 0)
    counters[len(design)] = 1

    num_possibilities = count_possibilities(design, 0, counters)
    total_part1 += min(num_possibilities, 1)
    total_part2 += num_possibilities
    if num_possibilities > 0:
        debug(f'  Created in {num_possibilities} ways')
    else:
        debug(f'  Impossible')

print(f'Part 1 - total = {total_part1}')
print(f'Part 2 - total = {total_part2}')



