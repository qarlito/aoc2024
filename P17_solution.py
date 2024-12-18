#!/usr/local/bin/python
from P17_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT
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
lines = INPUT.splitlines()
REG_A = int(re.match('Register A: (\\d+)', lines[0]).groups()[0])
REG_B = int(re.match('Register B: (\\d+)', lines[1]).groups()[0])
REG_C = int(re.match('Register C: (\\d+)', lines[2]).groups()[0])
assert lines[3] == ''
PROGRAM = [int(i) for i in re.match('Program: (.+)', lines[4]).groups()[0].split(',')]
PROGRAM_LEN = len(PROGRAM)
assert PROGRAM_LEN % 2 == 0

def get_combo_value(operand, state):
    if operand < 4:
        return operand
    return state[operand-4] # Should error if operand == 7

def run(program, regA, regB, regC):
    debug(f'START program={program} - registers {regA, regB, regC}')
    program_len = len(program)
    state = [regA, regB, regC]
    ip = 0
    output = list()
    while True:
        if ip >= program_len:
            break
        instruction = program[ip]
        operand = program[ip+1]
        ip += 2
        if instruction == 0:   # adv
            state[0] >>= get_combo_value(operand, state)
        elif instruction == 1: # bxl
            state[1] ^= operand
        elif instruction == 2: # bst
            state[1] = get_combo_value(operand, state) & 0x7
        elif instruction == 3: # jnz
            if state[0] != 0:
                ip = operand
        elif instruction == 4: # bxc
            state[1] ^= state[2]
        elif instruction == 5: # out
            output.append(get_combo_value(operand, state) & 0x7)
        elif instruction == 6: # bdv
            state[1] = state[0] >> get_combo_value(operand, state)
        elif instruction == 7: # cdv
            state[2] = state[0] >> get_combo_value(operand, state)
        debug(f'registers={state}, output={output}')
    return state, output

state, output = run(PROGRAM, REG_A, REG_B, REG_C)
print(f'Program  : {PROGRAM}')
print(f'Registers: {REG_A, REG_B, REG_C}')
part1_output = f'{",".join([str(i) for i in output])}'

'''
2,4,  1,3,  7,5,  4,0,  1,3,  0,3,  5,5,  3,0

<< TBD INITIAL VALUE OF A >>
B1 := A & 7
B2 := B1 ^ 3
C  := A >> B2
B3 := B2 ^ C
B4 := B3 ^ 3
    = (B2 ^ C) ^ 3 = (B2 ^ 3) ^ C
    = B1 ^ (A >> (B1 ^ 3))
    = (A & 7) ^ (A >> ((A & 7) ^ 3))
B4 & 7 = (A & 7) ^ ((A >> ((A & 7) ^ 3)) & 7)

A = A >> 3
OUT(B4 & 7)
IF A != 0:
    jump to beginning of program
'''


def show(abits):
    s = ''
    for bitnum in range(max(abits),-1,-1):
        if bitnum in abits:
            s += str(abits[bitnum])
        else:
            s += '.'
    return s

OUT = [2,4,1,3,7,5,4,0,1,3,0,3,5,5,3,0]

candidate_solutions = set()
def search_solution(abits, iteration):
    offset = iteration * 3
    # need offset, offset+1, offset+2
    for i in range(3):
        if offset+2-i not in abits:
            abits_copy = abits.copy()
            abits_copy[offset+2-i] = 0
            search_solution(abits_copy, iteration)
            abits_copy = abits.copy()
            abits_copy[offset+2-i] = 1
            search_solution(abits_copy, iteration)
            return
   
    last3 = (abits[offset]) + (abits[offset+1]<<1) + (abits[offset+2]<<2)
    goal = OUT[iteration] ^ last3
    shift = (last3 ^ 3) + (iteration * 3)

    print('  '*iteration + f'Iteration {iteration} - choose abits[{offset}:{offset+2}] == {last3}')
    print('  '*iteration + f'  A is {show(abits)}')
    print('  '*iteration + f'  Shift is {shift}. I want bits {shift}:{shift+2} to be equal to {OUT[iteration]} ^ {last3} = {goal}')
    conflict = False

    if shift in abits:
        if abits[shift] != goal & 1:
            print('  '*iteration + f'    Conflict for bit {shift} - is {abits[shift]} want {goal&1}')
            return
    else:
        abits[shift] = goal & 1

    if shift+1 in abits:
        if abits[shift+1] != (goal & 2) >> 1:
            print('  '*iteration + f'    Conflict for bit {shift+1} - is {abits[shift+1]} want {(goal&2)>>1}')
            return
    else:
        abits[shift+1] = (goal & 2) >> 1

    if shift+2 in abits:
        if abits[shift+2] != (goal & 4) >> 2:
            print('  '*iteration + f'    Conflict for bit {shift+2} - is {abits[shift+2]} want {(goal&4)>>2}')
            return
    else:
        abits[shift+2] = (goal & 4) >> 2

    print('  '*iteration + f'  A is now {show(abits)}')

    if iteration < len(OUT) - 1:
        return search_solution(abits, iteration+1)
    else:
        candidate_solution = 0
        for bitnum, bitvalue in abits.items():
            candidate_solution += bitvalue << bitnum
        print('  '*iteration + f'  Candidate: {candidate_solution}')
        candidate_solutions.add(candidate_solution)

search_solution({}, 0)
real_solutions = set()
for candidate_solution in sorted(candidate_solutions):
    #     111 =        results in 1 output
    #    1000 = (1<<3) results in 2 outputs
    # 1000000 = (1<<6) results in 3 outputs
    # ...
    if candidate_solution < (1 << (3*15)):
        print(f'Solution {candidate_solution} is too small. Would exit prematurely.')
    if candidate_solution >= (1 << (3*16)):
        print(f'Solution {candidate_solution} is too long. Would result in too much output')
    state, output = run(PROGRAM, candidate_solution, 0, 0)
    if output == OUT:
        print(f'REAL SOLUTION: {candidate_solution}') 
        real_solutions.add(candidate_solution)

best_solution = min(real_solutions)
print('\n' + ('-' * 40))
print(f'\nPart 1: Output is {part1_output}')
print(f'\nPart 2: Solution is {best_solution}')

