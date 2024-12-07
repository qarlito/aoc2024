#!/usr/local/bin/python
from P07_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT
#from Pxx_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT

import sys
if len(sys.argv) > 1 and sys.argv[1].startswith('d'):
    INPUT1 = DEMO_INPUT1.strip()
    INPUT2 = DEMO_INPUT2.strip()
else:
    INPUT1 = PRODUCTION_INPUT.strip()
    INPUT2 = INPUT1


BACKTRACK_OPERATION = object()

def find_total(operations, raw_input):

    OPERATIONS = [*operations, BACKTRACK_OPERATION]
    FIRST_OPERATION_NUMBER = 0
    BACKTRACK_OPERATION_NUMBER = len(OPERATIONS)-1

    total = 0
    for line in raw_input.splitlines():

        goal, terms = line.strip().split(': ')
        goal = int(goal)
        terms = [int(term) for term in terms.split(' ')]
        state = [(FIRST_OPERATION_NUMBER, terms[0])]  # (intended next operation, intermediate value)

        while True:

            intended_operation, current_value = state[-1]

            if OPERATIONS[intended_operation] == BACKTRACK_OPERATION:
                # Need to backtrack
                # 1. Remove last entry
                state.pop()
                if len(state) == 0:
                    break
                # 2. Replace the last entry (of the shortened list) with the next operation
                s = state.pop()
                new_s = (s[0]+1, s[1])
                state.append(new_s)
                continue

            new_term = terms[len(state)]
            new_value = OPERATIONS[intended_operation](current_value, new_term)

            if len(state) == len(terms) - 1:
                # We reached full length
                if new_value == goal:
                    # Success
                    total += goal
                    break
                else:
                    new_operation_number = BACKTRACK_OPERATION_NUMBER
            else:
                new_operation_number = FIRST_OPERATION_NUMBER

            # Extend
            state.append((new_operation_number, new_value))

    return total


INPUT = INPUT1

part1_total = find_total([(lambda a,b: a+b), (lambda a,b: a*b)], INPUT)
print(f'Part 1 total = {part1_total}')

part2_total = find_total([(lambda a,b: a+b), (lambda a,b: a*b), (lambda a,b: int(str(a)+str(b)))], INPUT)
print(f'Part 2 total = {part2_total}')
