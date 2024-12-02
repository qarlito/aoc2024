from P02_input import DEMO_INPUT, PRODUCTION_INPUT

import sys
if len(sys.argv) > 1 and sys.argv[1].startswith('d'):
    INPUT = DEMO_INPUT
else:
    INPUT = PRODUCTION_INPUT


def is_safe(numbers):
    if numbers[1] > numbers[0]:
        # assume increasing
        safe = all([1 <= b-a <= 3 for a,b in zip(numbers, numbers[1:])])
    else:
        # assume decreasing
        safe = all([1 <= a-b <= 3 for a,b in zip(numbers, numbers[1:])])
    return safe


numsafe = 0
for line in INPUT.strip().splitlines():
    numbers = [int(n) for n in line.split(' ')]
    if is_safe(numbers):
        numsafe += 1
print(f'Part 1: {numsafe} safe reports.')


numsafe = 0
for line in INPUT.strip().splitlines():
    numbers = [int(n) for n in line.split(' ')]
    safe = False
    for skip in range(len(numbers)):
        if is_safe(numbers[:skip] + numbers[skip+1:]):
            safe = True
            break 
    #print(f'{numbers} is safe: {safe}')
    if safe:
        numsafe += 1
print(f'Part 2: {numsafe} safe reports.')
